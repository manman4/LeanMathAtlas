from __future__ import annotations

import json
import subprocess

from auto_prove_store import WORKDIR, build_proved_theorems, resolve_lake

SEP = "\n\n"
REPL_CMD = [resolve_lake(), "exe", "repl"]


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

    def send(self, cmd: dict) -> dict:
        payload = json.dumps(cmd) + SEP
        self.proc.stdin.write(payload.encode())
        self.proc.stdin.flush()
        return self._read_response()

    def _read_response(self) -> dict:
        lines = []
        while True:
            line = self.proc.stdout.readline().decode()
            if line in ("\n", ""):
                if lines:
                    block = "".join(lines).strip()
                    try:
                        return json.loads(block)
                    except json.JSONDecodeError:
                        lines = []
                if line == "":
                    return {}
            else:
                lines.append(line)

    def close(self):
        try:
            self.proc.stdin.close()
        except BrokenPipeError:
            pass
        self.proc.wait()


def prepare_proof_env(dry_run: bool = False, preamble: str = "", use_proved: bool = False) -> tuple[ReplSession, int]:
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
    print("  [repl] Loading Mathlib + ProvedTheorems (~80s)..." if load_proved else "  [repl] Loading Mathlib (~80s)...")
    imports = "import Mathlib\nimport LeanMathAtlas.ProvedTheorems" if load_proved else "import Mathlib"
    resp = session.send({"cmd": imports})
    if has_error(resp):
        session.close()
        raise RuntimeError(
            "Failed to import the Lean environment for proof search.\n"
            f"{format_repl_errors(resp)}"
        )
    env0 = resp.get("env", 0)
    open_cmd = "open BigOperators AutoProved" if load_proved else "open BigOperators"
    resp = session.send({"cmd": open_cmd, "env": env0})
    if has_error(resp):
        session.close()
        raise RuntimeError(
            "Failed to open the Lean proof environment.\n"
            f"{format_repl_errors(resp)}"
        )
    env1 = resp.get("env", env0)
    resp = session.send({"cmd": "open scoped Nat", "env": env1})
    if has_error(resp):
        session.close()
        raise RuntimeError(
            "Failed to enable scoped Nat notations.\n"
            f"{format_repl_errors(resp)}"
        )
    env2 = resp.get("env", env0)
    if preamble:
        resp = session.send({"cmd": preamble, "env": env2})
        if has_error(resp):
            session.close()
            raise RuntimeError(
                "Failed to load the theorem preamble into the REPL.\n"
                f"{format_repl_errors(resp)}"
            )
    return session, resp.get("env", env2)
