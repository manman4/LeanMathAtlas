from __future__ import annotations

import json
import os
import selectors
import subprocess
import time

from auto_prove_store import WORKDIR, build_proved_theorems, resolve_lake

SEP = "\n\n"
REPL_CMD = [resolve_lake(), "exe", "repl"]
DEFAULT_REPL_STARTUP_TIMEOUT = float(os.environ.get("AUTO_PROVE_PREPARE_TIMEOUT_SEC", "240"))


def has_error(resp: dict) -> bool:
    return any(m.get("severity") == "error" for m in resp.get("messages", []))


def format_repl_errors(resp: dict) -> str:
    parts = []
    for msg in resp.get("messages", []):
        if msg.get("severity") == "error":
            data = msg.get("data", "").strip()
            if data:
                parts.append(data)
    return "\n".join(parts)


class ReplSession:
    def __init__(self):
        self.proc = subprocess.Popen(
            REPL_CMD,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=WORKDIR,
        )

    def send(self, cmd: dict, timeout_sec: float | None = None) -> dict:
        if self.proc.poll() is not None:
            raise RuntimeError("Lean REPL process is no longer running")
        payload = json.dumps(cmd) + SEP
        try:
            self.proc.stdin.write(payload.encode())
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise RuntimeError("Failed to send command to Lean REPL") from exc
        return self._read_response(timeout_sec=timeout_sec)

    def _read_response(self, timeout_sec: float | None = None) -> dict:
        lines = []
        selector = selectors.DefaultSelector()
        selector.register(self.proc.stdout, selectors.EVENT_READ)
        deadline = None if timeout_sec is None else time.monotonic() + timeout_sec
        try:
            while True:
                if deadline is not None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("Timed out waiting for Lean REPL response")
                else:
                    remaining = None
                events = selector.select(remaining)
                if not events:
                    raise TimeoutError("Timed out waiting for Lean REPL response")
                line = self.proc.stdout.readline().decode()
                if line == "":
                    if lines:
                        block = "".join(lines).strip()
                        if block:
                            return json.loads(block)
                    return {}
                if line.strip():
                    lines.append(line)
                    block = "".join(lines).strip()
                    try:
                        return json.loads(block)
                    except json.JSONDecodeError:
                        continue
        finally:
            selector.close()

    def close(self, wait_timeout_sec: float = 2.0, force: bool = False):
        try:
            if self.proc.stdin is not None and not self.proc.stdin.closed:
                self.proc.stdin.close()
        except (BrokenPipeError, OSError):
            pass
        if self.proc.poll() is not None:
            return
        if force:
            self.proc.terminate()
        try:
            self.proc.wait(timeout=wait_timeout_sec)
            return
        except subprocess.TimeoutExpired:
            pass
        self.proc.terminate()
        try:
            self.proc.wait(timeout=wait_timeout_sec)
            return
        except subprocess.TimeoutExpired:
            self.proc.kill()
            try:
                self.proc.wait(timeout=wait_timeout_sec)
            except subprocess.TimeoutExpired:
                pass


def prepare_proof_env(dry_run: bool = False, preamble: str = "", use_proved: bool = False,
                      startup_timeout: float | None = DEFAULT_REPL_STARTUP_TIMEOUT,
                      import_cmd: str | None = None) -> tuple[ReplSession, int]:
    """Create a REPL session and return (session, base_env) for theorem proving."""
    if use_proved and not dry_run:
        ok, details = build_proved_theorems()
        if not ok:
            raise RuntimeError(
                "LeanMathAtlas.ProvedTheorems failed to build before proof search.\n"
                f"{details}"
            )

    session = ReplSession()
    load_proved = use_proved and not dry_run
    imports = import_cmd
    if imports is None:
        imports = "import Mathlib\nimport LeanMathAtlas.ProvedTheorems" if load_proved else "import Mathlib"
    print(
        f"  [repl] Loading {'custom imports' if import_cmd else ('Mathlib + ProvedTheorems' if load_proved else 'Mathlib')} (~80s)..."
    )
    t0 = time.monotonic()
    try:
        resp = session.send({"cmd": imports}, timeout_sec=startup_timeout)
    except TimeoutError:
        session.close(force=True)
        raise RuntimeError(
            "Timed out while importing the Lean environment for proof search.\n"
            f"stage=import timeout_sec={startup_timeout}"
        )
    if has_error(resp):
        session.close(force=True)
        raise RuntimeError(
            "Failed to import the Lean environment for proof search.\n"
            f"{format_repl_errors(resp)}"
        )
    print(f"  [repl] import ready in {time.monotonic() - t0:.1f}s")
    env0 = resp.get("env", 0)
    open_cmd = "open BigOperators AutoProved" if load_proved else "open BigOperators"
    t1 = time.monotonic()
    try:
        resp = session.send({"cmd": open_cmd, "env": env0}, timeout_sec=startup_timeout)
    except TimeoutError:
        session.close(force=True)
        raise RuntimeError(
            "Timed out while opening the Lean proof environment.\n"
            f"stage=open timeout_sec={startup_timeout}"
        )
    if has_error(resp):
        session.close(force=True)
        raise RuntimeError(
            "Failed to open the Lean proof environment.\n"
            f"{format_repl_errors(resp)}"
        )
    print(f"  [repl] namespaces ready in {time.monotonic() - t1:.1f}s")
    env1 = resp.get("env", env0)
    t2 = time.monotonic()
    try:
        resp = session.send({"cmd": "open scoped Nat", "env": env1}, timeout_sec=startup_timeout)
    except TimeoutError:
        session.close(force=True)
        raise RuntimeError(
            "Timed out while enabling scoped Nat notations.\n"
            f"stage=open_scoped_nat timeout_sec={startup_timeout}"
        )
    if has_error(resp):
        session.close(force=True)
        raise RuntimeError(
            "Failed to enable scoped Nat notations.\n"
            f"{format_repl_errors(resp)}"
        )
    print(f"  [repl] scoped Nat ready in {time.monotonic() - t2:.1f}s")
    env2 = resp.get("env", env0)
    if preamble:
        t3 = time.monotonic()
        try:
            resp = session.send({"cmd": preamble, "env": env2}, timeout_sec=startup_timeout)
        except TimeoutError:
            session.close(force=True)
            raise RuntimeError(
                "Timed out while loading the theorem preamble into the REPL.\n"
                f"stage=preamble timeout_sec={startup_timeout}"
            )
        if has_error(resp):
            session.close(force=True)
            raise RuntimeError(
                "Failed to load the theorem preamble into the REPL.\n"
                f"{format_repl_errors(resp)}"
            )
        print(f"  [repl] preamble ready in {time.monotonic() - t3:.1f}s")
    return session, resp.get("env", env2)
