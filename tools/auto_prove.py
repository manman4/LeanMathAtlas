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
    # convert using 2 — allows deeper structural mismatches than using 1
    "have h := (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 2\n  ring",
    "have h := (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 2\n  ring",
    # ring_nf normalises the derivative expression before exact: absorbs mul_comm without convert
    "ring_nf\n  exact (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)",
    "ring_nf\n  exact (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)",
    # explicit two-have pattern (mirrors Derivatives.lean proof style)
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  convert h using 2\n  ring",
    # simp [Function.comp, id] unwraps ∘ notation; norm_num simplifies 2*1→2;
    # then convert + ring handles the remaining mul_comm mismatch.
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id] at h\n  norm_num at h\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id] at h\n  norm_num at h\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id, mul_one] at h\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id, mul_one] at h\n  convert h using 1\n  ring",
    # identity and constant
    "exact hasDerivAt_id _",
    "exact hasDerivAt_const _ _",
]

# Finset.card goals where the filter is an image of a simpler set.
# Generalizable: for filter(pred, range(k*n)).card = n, express as image(f, range n)
# then use card_image_of_injective + simp [Finset.card_range].
# omega handles the membership arithmetic after simp reduces it to linear facts.
FINSET_CARD_TEMPLATES = [
    # Even filter: {k < 2n | k%2=0}.card = n  ←  bijection k↦2k
    # rw [h, card_image_of_injective] leaves (range n).card = n, closed by simp.
    "have h : (Finset.range (2 * n)).filter (fun k => k % 2 = 0) = (Finset.range n).image (2 * ·) := by\n    ext k\n    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]\n    constructor\n    · intro ⟨hk, hmod⟩; exact ⟨k / 2, by omega, by omega⟩\n    · rintro ⟨m, hm, rfl⟩; exact ⟨by omega, by omega⟩\n  rw [h, Finset.card_image_of_injective _ (fun a b hab => by omega)]\n  simp",
    "have h : (Finset.range (2 * n)).filter (fun k => k % 2 = 0) = (Finset.range n).image (· * 2) := by\n    ext k\n    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]\n    constructor\n    · intro ⟨hk, hmod⟩; exact ⟨k / 2, by omega, by omega⟩\n    · rintro ⟨m, hm, rfl⟩; exact ⟨by omega, by omega⟩\n  rw [h, Finset.card_image_of_injective _ (fun a b hab => by omega)]\n  simp",
    # Odd filter: {k < 2n | k%2≠0}.card = n  ←  bijection k↦2k+1
    "have h : (Finset.range (2 * n)).filter (fun k => k % 2 ≠ 0) = (Finset.range n).image (2 * · + 1) := by\n    ext k\n    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]\n    constructor\n    · intro ⟨hk, hmod⟩; exact ⟨k / 2, by omega, by omega⟩\n    · rintro ⟨m, hm, rfl⟩; exact ⟨by omega, by omega⟩\n  rw [h, Finset.card_image_of_injective _ (fun a b hab => by omega)]\n  simp",
]

# Fintype / Pigeonhole templates (tried in cmd mode before BFS)
# Generalizable: Fintype.exists_ne_map_eq_of_card_lt is the standard Mathlib Pigeonhole lemma;
# simp [Fintype.card_fin] reduces Fintype.card (Fin n) → n; omega closes the card inequality.
FINTYPE_TEMPLATES = [
    "apply Fintype.exists_ne_map_eq_of_card_lt\n  simp [Fintype.card_fin, *]",
    "apply Fintype.exists_ne_map_eq_of_card_lt\n  simp [Fintype.card_fin]\n  omega",
    "apply Fintype.exists_ne_map_eq_of_card_lt\n  omega",
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
    # Fintype / Pigeonhole principle (standard Mathlib lemma for ∃-collision goals)
    "apply Fintype.exists_ne_map_eq_of_card_lt",
    # Fintype.card simp rules (reduces Fintype.card (Fin n) to n)
    "simp [Fintype.card_fin]", "simp [Fintype.card_fin, *]",
]

# Max seconds per theorem for iterative proof search
STEP_TIME_LIMIT = 10

def select_tactics(goal: str) -> list:
    """Narrow the tactic list based on symbols in the goal string."""
    if "∑" in goal or "Finset" in goal:
        # card goals: try bijection-based templates before induction
        if ".card" in goal:
            return FINSET_CARD_TEMPLATES + INDUCTION_TACTICS + SEARCH_TACTICS
        return INDUCTION_TACTICS + SEARCH_TACTICS
    if "Continuous" in goal or "Differentiable" in goal:
        return ["fun_prop", "simp", "aesop"] + SEARCH_TACTICS
    if "HasDerivAt" in goal or "HasFDerivAt" in goal:
        chain_tactics = chain_rule_deriv_tactics(goal)
        return chain_tactics + DERIV_TEMPLATES + ["fun_prop", "simp"] + SEARCH_TACTICS
    if "Irrational" in goal:
        return SEARCH_TACTICS
    # ∃-collision goals over Fin types (e.g. Pigeonhole principle)
    if "∃" in goal and "Fin" in goal:
        return FINTYPE_TEMPLATES + SEARCH_TACTICS
    # Factorial + prime goals (Wilson's theorem pattern).
    # Detected by '!' in goal (open scoped Nat renders n! not Nat.factorial)
    # combined with Nat.Prime in context (avoids false positives on other ! uses).
    # Variable names are extracted dynamically so any naming convention works.
    if "!" in goal and "Nat.Prime" in goal:
        m = re.search(r'(\w+)\s*:\s*Nat\.Prime\s+(\w+)', goal)
        if m:
            hname, pvar = m.group(1), m.group(2)
            return [
                f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩\n  exact ZMod.wilsons_lemma {pvar}",
                f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩\n  simp [ZMod.wilsons_lemma]",
            ] + SEARCH_TACTICS
    # ZMod goals: skip simple tactics that can't possibly work and go to search.
    if "ZMod" in goal:
        return ["norm_cast", "push_cast; ring", "simp"] + SEARCH_TACTICS
    # Polynomial inequality goals (≤ or ≥ with ^): build dynamic nlinarith witnesses.
    # nonneg3: for 3-var non-neg goals (AM-GM3, cube AM-GM, …)
    # pairwise_sq: for goals without non-neg assumptions (Cauchy-Schwarz, sym-ineq, …)
    if ("≤" in goal or "≥" in goal) and "^" in goal:
        tactics: list[str] = []
        nonneg_tac = nlinarith_nonneg3_tactic(goal)
        pairwise_tac = nlinarith_pairwise_sq_tactic(goal)
        if nonneg_tac:
            tactics += [nonneg_tac, "field_simp\n  " + nonneg_tac]
        if pairwise_tac:
            tactics.append(pairwise_tac)
        if tactics:
            return tactics + ["ring", "nlinarith", "linarith"] + SEARCH_TACTICS
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

def extract_nonneg_triples(goal: str) -> list[tuple[str, str]]:
    """Extract (hypothesis, variable) pairs from '0 ≤ var' in the proof state.

    Used to build generalizable nlinarith witnesses for polynomial inequalities
    with non-negativity assumptions (AM-GM, Cauchy-Schwarz, etc.).
    Returns pairs in order of appearance, e.g. [('ha','a'), ('hb','b'), ('hc','c')].
    """
    return re.findall(r'(\w+)\s*:\s*0\s*≤\s*(\w+)', goal)

def extract_chain_rule_params(goal: str) -> tuple[str, str, str] | None:
    """Extract (trig_fn, coeff, point) from a HasDerivAt chain rule goal.

    Matches: HasDerivAt (fun x => Real.F (c * x)) (... Real.F' (c * pt)) pt
    Returns e.g. ('sin', '2', 'a') for the bench_hard_chain goal.
    Used to build fully explicit .comp templates that avoid implicit-arg inference errors.
    """
    m = re.search(r'HasDerivAt \(fun \w+ => Real\.(sin|cos|exp) \((\S+) \* \w+\)\)', goal)
    if not m:
        return None
    fn = m.group(1)
    coeff = m.group(2)
    # point is the last token on the ⊢ line
    goal_line = [l for l in goal.splitlines() if "⊢" in l]
    if not goal_line:
        return None
    pt = goal_line[0].split()[-1]
    return fn, coeff, pt

def chain_rule_deriv_tactics(goal: str) -> list[str]:
    """Build explicit HasDerivAt chain rule tactic strings.

    Returns [] if the goal doesn't match the linear-composition pattern.
    Generates templates with all arguments explicit to avoid .comp implicit-arg failures.
    Pattern: HasDerivAt (fun x => Real.F(c*x)) (c * Real.F'(c*pt)) pt
    """
    p = extract_chain_rule_params(goal)
    if not p:
        return []
    fn, coeff, pt = p
    inner = f"({coeff} * {pt})"
    base = f"(Real.hasDerivAt_{fn} {inner}).comp {pt} ((hasDerivAt_id {pt}).const_mul {coeff})"
    return [
        f"have h := {base}\n  convert h using 1\n  ring",
        f"have h := {base}\n  simp only [Function.comp, id, mul_one] at h\n  convert h using 1\n  ring",
    ]

def extract_real_vars(goal: str) -> list[str]:
    """Extract variable names declared as ℝ or ℚ in the proof state context.

    e.g. 'a b : ℝ' → ['a', 'b']; 'a b c d : ℝ' → ['a', 'b', 'c', 'd']
    """
    result, seen = [], set()
    for m in re.finditer(r'(\b\w+(?:\s+\w+)*)\s*:\s*[ℝℚ]', goal):
        for name in m.group(1).split():
            if name not in seen:
                seen.add(name)
                result.append(name)
    return result

def nlinarith_pairwise_sq_tactic(goal: str) -> str | None:
    """Generate nlinarith witnesses from pairwise squared differences of ℝ variables.

    Handles polynomial inequalities WITHOUT explicit non-negativity assumptions.
    Witness pattern:
      - sq_nonneg (vi - vj)  for every pair  →  covers a²+b²+c² ≥ ab+bc+ca, (a+b+c)²≤3(a²+b²+c²)
      - sq_nonneg (vi*vk - vj*vl) for 4-var  →  covers 2D Cauchy-Schwarz (ad-bc)²≥0
    """
    vs = extract_real_vars(goal)
    if len(vs) < 2:
        return None
    witnesses = [f"sq_nonneg ({vs[i]} - {vs[j]})"
                 for i in range(len(vs)) for j in range(i + 1, len(vs))]
    if len(vs) >= 4:
        a, b, c, d = vs[0], vs[1], vs[2], vs[3]
        witnesses.append(f"sq_nonneg ({a}*{d} - {b}*{c})")
    return "nlinarith [" + ", ".join(witnesses) + "]"

def nlinarith_nonneg3_tactic(goal: str) -> str | None:
    """Build a generalizable nlinarith witness tactic for 3-variable non-negative ℝ inequalities.

    For goals like 'a*b*c ≤ ((a+b+c)/3)^3' with 'ha:0≤a', 'hb:0≤b', 'hc:0≤c',
    generates witnesses: pairwise squared differences + their products with non-neg vars.
    This covers AM-GM (3-var) and related symmetric polynomial inequalities.
    Returns None if fewer than 3 non-neg hypotheses are found.
    """
    pairs = extract_nonneg_triples(goal)
    if len(pairs) < 3:
        return None
    (h1, v1), (h2, v2), (h3, v3) = pairs[0], pairs[1], pairs[2]
    witnesses = [
        f"sq_nonneg ({v1} - {v2})",
        f"sq_nonneg ({v2} - {v3})",
        f"sq_nonneg ({v1} - {v3})",
        f"mul_nonneg {h1} (sq_nonneg ({v2} - {v3}))",
        f"mul_nonneg {h2} (sq_nonneg ({v1} - {v3}))",
        f"mul_nonneg {h3} (sq_nonneg ({v1} - {v2}))",
        f"mul_nonneg (mul_nonneg {h1} {h2}) {h3}",
    ]
    return "nlinarith [" + ", ".join(witnesses) + "]"

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
            env1 = resp.get("env", env0)
            # open scoped Nat enables n! factorial notation (wilsons_lemma uses it)
            # Regular `open Nat` does NOT activate scoped notations like n!
            resp = session.send({"cmd": "open scoped Nat", "env": env1})
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

                # Phase 1.5: Fact typeclass preamble + tactics
                # Handles lemmas that require [Fact (Nat.Prime p)] typeclass.
                # Tries SIMPLE_TACTICS first (simp/norm_num may find the goal if the target
                # lemma is @[simp]), then SEARCH_TACTICS as fallback.
                # For search tactics (exact?/simp?), we extract the "Try this:" suggestion even
                # if the response has errors (exact? may report an error while still suggesting
                # the right lemma), then verify the suggestion in a separate REPL call.
                if proof is None:
                    preamble = fact_preamble(stmt)
                    if preamble:
                        # Preprocessing variants: try cast normalisation before search tactics.
                        # norm_cast / push_cast can reveal ZMod.wilsons_lemma and similar
                        # lemmas that exact? misses when the goal has coercion noise.
                        _cast_prefixes = ["", "norm_cast\n  ", "push_cast\n  "]
                        _phase15_tactics = SIMPLE_TACTICS + SEARCH_TACTICS
                        for _cast in _cast_prefixes:
                            if proof is not None:
                                break
                            for t in _phase15_tactics:
                                resp = session.send({
                                    "cmd": f"{example} := by\n  {preamble}\n  {_cast}{t}",
                                    "env": base_env
                                })
                                if t in SEARCH_TACTICS:
                                    # Extract suggestion regardless of errors, then verify separately
                                    extracted = extract_try_this(resp)
                                    if extracted:
                                        resp2 = session.send({
                                            "cmd": f"{example} := by\n  {preamble}\n  {_cast}{extracted}",
                                            "env": base_env
                                        })
                                        if not has_error(resp2):
                                            proof = f"{preamble}\n  {_cast}{extracted}"
                                            if not dry_run:
                                                lean_name = lean_name_from(stmt)
                                                append_to_lean_db(stmt, proof, goal, lean_name)
                                                index[cache_key(stmt)] = lean_name
                                            break
                                elif not has_error(resp):
                                    proof = f"{preamble}\n  {_cast}{t}"
                                    if not dry_run:
                                        lean_name = lean_name_from(stmt)
                                        append_to_lean_db(stmt, proof, goal, lean_name)
                                        index[cache_key(stmt)] = lean_name
                                    break

                # Phase 1.6: apply? + all_goals closer
                # apply? finds any Mathlib lemma that partially matches the goal,
                # then closes remaining subgoals with standard tactics.
                # More powerful than exact? for goals that need a lemma application
                # followed by a simple finishing step (e.g. Pigeonhole + card simp).
                if proof is None:
                    _closers = [
                        "simp", "simp [*]", "omega",
                        "simp [Fintype.card_fin, *]", "simp_all",
                    ]
                    # Try plain apply? first, then with Fact preamble if present
                    _preamble = fact_preamble(stmt)
                    _prefixes = [""]
                    if _preamble:
                        _prefixes.append(_preamble)
                    for _pre in _prefixes:
                        if proof is not None:
                            break
                        _pre_block = f"  {_pre}\n  " if _pre else "  "
                        _resp = session.send({
                            "cmd": f"{example} := by\n{_pre_block}apply?",
                            "env": base_env
                        })
                        _sug = extract_try_this(_resp)
                        if not _sug or not (_sug.startswith("apply ") or _sug.startswith("refine ")):
                            continue
                        for _closer in _closers:
                            _cmd = (
                                f"{example} := by\n  {_pre}\n  {_sug}\n  all_goals {_closer}"
                                if _pre else
                                f"{example} := by\n  {_sug}\n  all_goals {_closer}"
                            )
                            _resp2 = session.send({"cmd": _cmd, "env": base_env})
                            if not has_error(_resp2):
                                proof = (
                                    f"{_pre}\n  {_sug}\n  all_goals {_closer}"
                                    if _pre else
                                    f"{_sug}\n  all_goals {_closer}"
                                )
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
