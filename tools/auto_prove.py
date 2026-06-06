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

WORKDIR        = Path(os.environ.get("LEAN_WORKDIR", Path(__file__).parent.parent)).resolve()
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
    "fun_prop",
    "simp [*]", "simp_all", "push_cast; ring", "push_cast; omega",
    "norm_cast", "norm_cast; ring", "norm_cast; omega",
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

# HasDerivAt-specific one-shot templates (tried before BFS for derivative goals)
DERIV_TEMPLATES = [
    # scalar multiple: c * sin/cos/exp
    "exact (Real.hasDerivAt_sin _).const_mul _",
    "exact (Real.hasDerivAt_cos _).const_mul _",
    "exact (Real.hasDerivAt_exp _).const_mul _",
    # negation
    "exact (Real.hasDerivAt_sin _).neg",
    "exact (Real.hasDerivAt_cos _).neg",
    # chain rule: f(c * x) — comp gives g'*f', goal may have f'*g' (mul_comm)
    "exact (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)",
    "exact (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)",
    # convert absorbs both function-form and mul_comm mismatches
    "have h := (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 1\n  ring",
    "have h := (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 1\n  ring",
    # explicit two-have pattern (mirrors Derivatives.lean proof style)
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  convert h using 1\n  ring",
    # identity and constant
    "exact hasDerivAt_id _",
    "exact hasDerivAt_const _ _",
]

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
    "fun_prop", "norm_cast",
    # Derivative building blocks (for BFS multi-step)
    "apply HasDerivAt.const_mul", "apply HasDerivAt.comp",
    "apply HasDerivAt.neg", "apply HasDerivAt.add",
    "exact Real.hasDerivAt_sin _", "exact Real.hasDerivAt_cos _",
    "exact hasDerivAt_id _",
]

# Max seconds per theorem for iterative proof search
STEP_TIME_LIMIT = 10

def select_tactics(goal: str) -> list:
    """Narrow the tactic list based on symbols in the goal string."""
    if "∑" in goal or "Finset" in goal:
        return INDUCTION_TACTICS + SEARCH_TACTICS
    if "Continuous" in goal or "Differentiable" in goal:
        return ["fun_prop", "simp", "aesop"] + SEARCH_TACTICS
    if "HasDerivAt" in goal or "HasFDerivAt" in goal:
        return DERIV_TEMPLATES + ["fun_prop", "simp"] + SEARCH_TACTICS
    if "Irrational" in goal:
        return SEARCH_TACTICS
    if "^" in goal:
        return ["ring", "nlinarith", "norm_num"] + INDUCTION_TACTICS + SEARCH_TACTICS
    if "ℝ" in goal or "ℚ" in goal:
        return ["ring", "linarith", "norm_num", "nlinarith", "fun_prop"] + SEARCH_TACTICS
    if "ℕ" in goal or "ℤ" in goal:
        return ["omega", "simp", "rfl", "decide", "ring", "norm_num", "norm_cast"] + SEARCH_TACTICS
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

def fact_preamble(stmt: str) -> str:
    """Generate haveI lines for Nat.Prime hypotheses.

    e.g. '(hp : Nat.Prime p)' → 'haveI : Fact (Nat.Prime p) := ⟨hp⟩'
    Many Mathlib lemmas (ZMod.wilsons_lemma, ZMod.pow_card, …) require
    [Fact (Nat.Prime p)] as a typeclass, so this bridges the gap between
    a plain hypothesis and the typeclass the lemma expects.
    """
    lines = []
    for m in re.finditer(r'\((\w+)\s*:\s*Nat\.Prime\s+(\w+)\)', stmt):
        hname, pvar = m.group(1), m.group(2)
        lines.append(f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩")
    return "\n  ".join(lines)

# ────────────────────────────────────────────────
# Automated proving
# ────────────────────────────────────────────────

def prove_all(theorems: list, dry_run: bool = False) -> list:
    """Attempt to prove each theorem.

    dry_run=True: skip ProvedTheorems.lean writes and cache updates (used by benchmark.py
    so that one run cannot contaminate the next).
    """
    index = load_index()
    uncached = theorems if dry_run else [s for s in theorems if cache_key(s) not in index]

    new_results: dict[str, tuple] = {}

    if uncached:
        if not dry_run:
            subprocess.run(
                ["lake", "build", "LeanMathAtlas.ProvedTheorems"],
                cwd=WORKDIR, capture_output=True
            )
        session = ReplSession()
        try:
            print("  [repl] Loading Mathlib (~80s)..." if dry_run else "  [repl] Loading Mathlib + ProvedTheorems (~80s)...")
            # dry_run: import full Mathlib (no ProvedTheorems) so all lemmas are available
            # but our previously proved theorems don't contaminate the results
            imports = "import Mathlib" if dry_run else "import Mathlib.Tactic\nimport LeanMathAtlas.ProvedTheorems"
            resp = session.send({"cmd": imports})
            env0 = resp.get("env", 0)
            resp = session.send({"cmd": "open BigOperators AutoProved", "env": env0})
            base_env = resp.get("env", env0)

            for stmt in uncached:
                example = to_example(stmt)
                t_stmt = time.monotonic()

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
                            extracted = extract_try_this(resp)
                            if extracted is None:
                                continue
                            proof = extracted
                        else:
                            proof = t
                        if not dry_run:
                            lean_name = lean_name_from(stmt)
                            append_to_lean_db(stmt, proof, goal, lean_name)
                            index[cache_key(stmt)] = lean_name
                        break

                # Phase 1.5: Fact typeclass preamble + search tactics
                # Handles lemmas that require [Fact (Nat.Prime p)] typeclass
                if proof is None:
                    preamble = fact_preamble(stmt)
                    if preamble:
                        for t in SEARCH_TACTICS:
                            resp = session.send({
                                "cmd": f"{example} := by\n  {preamble}\n  {t}",
                                "env": base_env
                            })
                            if not has_error(resp):
                                extracted = extract_try_this(resp)
                                if extracted:
                                    proof = f"{preamble}\n  {extracted}"
                                    if not dry_run:
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
                        if not dry_run:
                            lean_name = lean_name_from(stmt)
                            append_to_lean_db(stmt, proof, goal, lean_name)
                            index[cache_key(stmt)] = lean_name

                new_results[stmt] = (proof, goal, time.monotonic() - t_stmt)

        finally:
            session.close()
            if not dry_run:
                save_index(index)

    # Collect results in the original order
    results = []
    for stmt in theorems:
        if stmt in new_results:
            proof, goal, solve_time = new_results[stmt]
        else:
            lean_name = index.get(cache_key(stmt), "")
            proof = lean_name  # already proved — return the Lean name
            goal = ""
            solve_time = 0.0
        results.append((stmt, proof, goal, solve_time))
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
