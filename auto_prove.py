#!/usr/bin/env python3
"""
Lean 4 automated theorem prover.
- Accumulates proofs in ProvedTheorems.lean (correctness guaranteed by the Lean compiler)
- .proof_index.json for fast lookup (hash → theorem name)
- Interactive REPL: breaks immediately on the first successful tactic
- Rule-based tactic filtering: narrows candidates from the goal string
- Iterative proof search: BFS over tactic sequences via REPL tactic mode (time-limited)
"""

from __future__ import annotations
import subprocess, json, re, sys, time, os, hashlib
from collections import deque
from datetime import date
from pathlib import Path

WORKDIR        = Path(os.environ.get("LEAN_WORKDIR", Path(__file__).parent)).resolve()
REPL_CMD       = ["lake", "exe", "repl"]
SEP            = "\n\n"
LEAN_DB_FILE   = WORKDIR / "LeanMathAtlas" / "ProvedTheorems.lean"
INDEX_FILE     = WORKDIR / ".proof_index.json"

# ────────────────────────────────────────────────
# Index (fast lookup)
# ────────────────────────────────────────────────

def load_index() -> dict:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {}

def save_index(index: dict):
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2))

def cache_key(stmt: str) -> str:
    return hashlib.sha256(stmt.strip().encode()).hexdigest()[:16]

# ────────────────────────────────────────────────
# Writing to ProvedTheorems.lean
# ────────────────────────────────────────────────

def lean_name_from(stmt: str) -> str:
    """'theorem foo ...' → 'foo'; otherwise generate from hash."""
    m = re.match(r"^theorem\s+(\S+)", stmt.strip())
    return m.group(1) if m else f"proved_{cache_key(stmt)[:8]}"

def stmt_body(stmt: str) -> str:
    """'theorem foo (args) : T' → '(args) : T'"""
    return re.sub(r"^theorem\s+\S+", "", stmt.strip()).strip()

def tactic_block(tactic: str) -> str:
    """Indent a tactic string for use inside a `by` block."""
    lines = tactic.split("\n")
    if len(lines) == 1:
        return f"  {tactic}"
    # Multi-line tactics (induction, etc.) — indent every line
    return "\n".join(f"  {l}" for l in lines)

def append_to_lean_db(stmt: str, tactic: str, goal: str, lean_name: str):
    goal_commented = "\n".join(f"--   {line}" for line in goal.split("\n"))
    entry = (
        f"\n"
        f"-- stmt: {stmt}\n"
        f"-- goal:\n{goal_commented}\n"
        f"-- added: {date.today()}\n"
        f"theorem {lean_name} {stmt_body(stmt)} := by\n"
        f"{tactic_block(tactic)}\n"
    )
    content = LEAN_DB_FILE.read_text(encoding="utf-8")
    # Insert before the closing namespace marker
    marker = "\nend AutoProved\n"
    if marker in content:
        content = content.replace(marker, entry + marker)
    else:
        content += entry
    LEAN_DB_FILE.write_text(content, encoding="utf-8")

# ────────────────────────────────────────────────
# Interactive REPL session
# ────────────────────────────────────────────────

class ReplSession:
    def __init__(self):
        self.proc = subprocess.Popen(
            REPL_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, cwd=WORKDIR
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

# ────────────────────────────────────────────────
# Tactic candidates
# ────────────────────────────────────────────────

SIMPLE_TACTICS = [
    "rfl", "ring", "omega", "simp", "norm_num",
    "decide", "tauto", "linarith", "nlinarith", "aesop",
    "simp [*]", "simp_all", "push_cast; ring", "push_cast; omega",
]

INDUCTION_TACTICS = [
    "induction n with\n  | zero => simp\n  | succ m ih => omega",
    "induction n with\n  | zero => simp\n  | succ m ih => ring",
    "induction n with\n  | zero => simp\n  | succ m ih => linarith",
    "induction n with\n  | zero => simp\n  | succ m ih => nlinarith [ih]",
    "induction n with\n  | zero => simp\n  | succ m ih =>\n    rw [Finset.sum_range_succ]; omega",
    "induction n with\n  | zero => simp\n  | succ m ih =>\n    rw [Finset.sum_range_succ]; nlinarith [ih]",
    "induction n with\n  | zero => simp\n  | succ m ih =>\n    rw [Finset.sum_range_succ, mul_add, ih]; ring",
]

ALL_TACTICS = SIMPLE_TACTICS + INDUCTION_TACTICS

# Search tactics: tried last as fallback; proof is extracted from "Try this:" message
SEARCH_TACTICS = ["exact?", "simp?"]

# Step-by-step tactics used in iterative BFS search
STEP_TACTICS = [
    # Intro / elimination
    "intro h", "intro hp hq", "intro hp hq hr",
    "exact h", "exact hp", "exact hq", "exact hr",
    "apply h", "apply hp", "apply hq",
    "assumption",
    # Structural
    "constructor", "left", "right",
    "rcases h with ha | hb",
    "obtain ⟨a, b⟩ := h",
    # Auto closers
    "tauto", "simp", "ring", "omega", "norm_num", "linarith", "aesop",
]

# Max seconds per theorem for iterative proof search
STEP_TIME_LIMIT = 30

def select_tactics(goal: str) -> list:
    """Narrow the tactic list based on symbols in the goal string."""
    if "∑" in goal or "Finset" in goal:
        return INDUCTION_TACTICS + SEARCH_TACTICS
    if "^" in goal:
        return ["ring", "nlinarith", "norm_num"] + INDUCTION_TACTICS + SEARCH_TACTICS
    if "ℝ" in goal or "ℚ" in goal:
        return ["ring", "linarith", "norm_num", "nlinarith"] + SEARCH_TACTICS
    if "ℕ" in goal or "ℤ" in goal:
        return ["omega", "simp", "rfl", "decide", "ring", "norm_num"] + SEARCH_TACTICS
    return ALL_TACTICS + SEARCH_TACTICS

# ────────────────────────────────────────────────
# Utilities
# ────────────────────────────────────────────────

def has_error(resp: dict) -> bool:
    return any(m.get("severity") == "error" for m in resp.get("messages", []))

def prove_iterative(session, example: str, base_env: int, time_limit: int = STEP_TIME_LIMIT) -> str | None:
    """BFS proof search: apply one tactic at a time via REPL tactic mode.

    Sends {"tactic": t, "proofState": N} to step through a proof incrementally.
    Returns a newline-joined tactic sequence on success, or None on timeout/failure.
    """
    # Obtain initial proof state from sorry
    resp = session.send({"cmd": f"{example} := by sorry", "env": base_env})
    sorries = resp.get("sorries", [])
    if not sorries:
        return None
    init_state = sorries[0].get("proofState")
    if init_state is None:
        return None

    deadline = time.time() + time_limit
    # BFS: each entry is (proof_state_id, tactics_applied_so_far)
    queue: deque[tuple[int, list[str]]] = deque([(init_state, [])])
    visited: set[int] = set()

    while queue and time.time() < deadline:
        state, applied = queue.popleft()
        if len(applied) >= 6 or state in visited:
            continue
        visited.add(state)

        for t in STEP_TACTICS:
            if time.time() > deadline:
                return None
            resp = session.send({"tactic": t, "proofState": state})
            if has_error(resp):
                continue
            # Use get() without default: absent key → None (avoids {} false-positive)
            goals = resp.get("goals")
            new_state = resp.get("proofState")
            if goals is None and new_state is None:
                continue  # REPL returned empty / didn't recognise the command
            new_applied = applied + [t]
            if goals == []:          # all goals closed — proof complete
                return "\n".join(new_applied)
            if new_state is not None and goals is not None and len(goals) <= 4:
                queue.append((new_state, new_applied))

    return None

def extract_try_this(resp: dict) -> str | None:
    """Extract the concrete tactic from 'Try this:' messages (exact? / simp? output).

    Handles both single-line ('Try this: exact X') and multi-line formats
    ('Try this:\\n  [apply] exact X') produced by different Lean/Mathlib versions.
    """
    for msg in resp.get("messages", []):
        data = msg.get("data", "")
        # Try this: exact X  (single-line)
        # Try this:\n  [apply] exact X  (multi-line with optional tag)
        m = re.search(r"Try this:[ \t]*\n?[ \t]*(?:\[\w+\] )?(.+)", data)
        if m:
            return m.group(1).strip()
    return None

def to_example(stmt: str) -> str:
    return re.sub(r"^theorem\s+\S+", "example", stmt)

# ────────────────────────────────────────────────
# Automated proving
# ────────────────────────────────────────────────

def prove_all(theorems: list) -> list:
    index = load_index()
    uncached = [s for s in theorems if cache_key(s) not in index]

    new_results: dict[str, tuple] = {}

    if uncached:
        # Pre-build so previously proved theorems are available in the REPL
        subprocess.run(
            ["lake", "build", "LeanMathAtlas.ProvedTheorems"],
            cwd=WORKDIR, capture_output=True
        )
        session = ReplSession()
        try:
            print("  [repl] Loading Mathlib + ProvedTheorems (~80s)...")
            resp = session.send({"cmd": "import Mathlib.Tactic\nimport LeanMathAtlas.ProvedTheorems"})
            env0 = resp.get("env", 0)
            resp = session.send({"cmd": "open BigOperators AutoProved", "env": env0})
            base_env = resp.get("env", env0)

            for stmt in uncached:
                example = to_example(stmt)

                # Fetch the goal
                goal = ""
                resp = session.send({"cmd": f"{example} := by sorry", "env": base_env})
                sorries = resp.get("sorries", [])
                if sorries:
                    goal = sorries[0].get("goal", "")

                # Phase 1: try each filtered tactic in one shot
                proof = None
                for t in select_tactics(goal):
                    resp = session.send({"cmd": f"{example} := by\n  {t}", "env": base_env})
                    if not has_error(resp):
                        if t in SEARCH_TACTICS:
                            # exact? / simp? must report "Try this:" — skip if not found
                            extracted = extract_try_this(resp)
                            if extracted is None:
                                continue
                            proof = extracted
                        else:
                            proof = t
                        lean_name = lean_name_from(stmt)
                        append_to_lean_db(stmt, proof, goal, lean_name)
                        index[cache_key(stmt)] = lean_name
                        break

                # Phase 2: if one-shot failed, try iterative BFS (time-limited)
                if proof is None:
                    print(f"  [step] iterative search (up to {STEP_TIME_LIMIT}s)...")
                    step_proof = prove_iterative(session, example, base_env)
                    if step_proof:
                        proof = step_proof
                        lean_name = lean_name_from(stmt)
                        append_to_lean_db(stmt, proof, goal, lean_name)
                        index[cache_key(stmt)] = lean_name

                new_results[stmt] = (proof, goal)

        finally:
            session.close()
            save_index(index)

    # Collect results in the original order
    results = []
    for stmt in theorems:
        if stmt in new_results:
            proof, goal = new_results[stmt]
        else:
            lean_name = index.get(cache_key(stmt), "")
            proof = lean_name  # already proved — return the Lean name
            goal = ""
        results.append((stmt, proof, goal))
    return results

# ────────────────────────────────────────────────
# Test theorems
# ────────────────────────────────────────────────

TESTS = [
    "theorem t1 : (1:ℕ) + 1 = 2",
    "theorem t2 (n : ℕ) : n + 0 = n",
    "theorem t3 (a b : ℤ) : a + b = b + a",
    "theorem t4 (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2",
    "theorem t5 (a b c : ℕ) : (a + b) + c = a + (b + c)",
    "theorem t6 (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)",
    "theorem t7 (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1)",
]

def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else TESTS
    index = load_index()
    cached_count = sum(1 for s in targets if cache_key(s) in index)
    print(f"[run] {len(targets)} theorems ({cached_count} cached / {len(targets) - cached_count} uncached)")

    t0 = time.time()
    results = prove_all(targets)
    elapsed = time.time() - t0

    passed = failed = 0
    for stmt, proof, goal in results:
        print(f"\n{'─'*60}")
        print(f"target: {stmt}")
        if goal:
            print(f"  goal: {goal}")
        if proof:
            proof_display = "\n    ".join(proof.split("\n"))
            print(f"  ✓ by\n    {proof_display}")
            passed += 1
        else:
            print(f"  ✗ proof not found")
            failed += 1

    print(f"\n{'─'*60}")
    print(f"total: {passed} passed / {failed} failed / {elapsed:.1f}s")
    if passed > 0:
        print(f"  → saved to {LEAN_DB_FILE.relative_to(WORKDIR)}")

if __name__ == "__main__":
    main()
