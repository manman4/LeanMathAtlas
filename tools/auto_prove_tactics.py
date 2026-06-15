from __future__ import annotations

import re
import time
from collections import deque

from auto_prove_repl import has_error

SIMPLE_TACTICS = [
    "rfl", "ring", "omega", "simp", "norm_num",
    "decide", "tauto", "linarith", "nlinarith", "aesop",
    "fun_prop",
    "simp [*]", "simp_all", "push_cast; ring", "push_cast; omega",
    "norm_cast", "norm_cast; ring", "norm_cast; omega",
    "linear_combination",
]

INNER_PRODUCT_TACTICS = [
    "exact real_inner_comm _ _",
    "exact (real_inner_comm _ _).symm",
    "exact inner_comm (𝕜 := ℝ) _ _",
    "simp only [inner_comm (𝕜 := ℝ)]",
    "exact inner_add_left _ _ _",
    "exact inner_add_right _ _ _",
    "exact inner_smul_left _ _ _",
    "exact inner_smul_right _ _ _",
    "exact real_inner_self_nonneg",
    "exact inner_self_eq_zero",
    "exact real_inner_self_eq_norm_sq _",
    "exact norm_smul _ _",
    "simp [inner_add_left, inner_add_right, inner_smul_left, inner_smul_right, inner_self_eq_zero, real_inner_self_eq_norm_sq, norm_smul]",
    "simp [inner_smul_left]",
    "simp [inner_smul_right]",
    "simp [real_inner_self_eq_norm_sq]",
    "simp [EuclideanSpace.inner_single_left, EuclideanSpace.inner_single_right]",
    "simp [EuclideanSpace.norm_single]",
    "have h := abs_real_inner_le_norm _ _\n  have hx := real_inner_self_eq_norm_sq _\n  have hy := real_inner_self_eq_norm_sq _\n  nlinarith [sq_abs (inner (𝕜 := ℝ) _ _), abs_nonneg (inner (𝕜 := ℝ) _ _), mul_pow ‖_‖ ‖_‖ 2]",
]

TRIG_DOUBLE_TACTICS = [
    "rw [cos_two_mul]; linarith [sin_sq_add_cos_sq _]",
    "rw [Real.cos_two_mul]; linarith [Real.sin_sq_add_cos_sq _]",
    "rw [cos_two_mul]; nlinarith [sin_sq_add_cos_sq _]",
    "rw [Real.cos_two_mul]; nlinarith [Real.sin_sq_add_cos_sq _]",
    "simp [cos_two_mul, sin_sq_add_cos_sq]",
    "simp [Real.cos_two_mul, Real.sin_sq_add_cos_sq]",
]

COMPLEX_TACTICS = [
    "simp [normSq_apply, sq]",
    "simp [Complex.normSq_apply, sq]",
    "rw [normSq_apply]; ring",
    "rw [← exp_nat_mul]; congr 1; ring",
    "rw [← Complex.exp_nat_mul]; congr 1; ring",
    "simp [← exp_nat_mul, mul_comm, mul_assoc]",
    "simp [exp_mul_I, exp_add]",
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
SEARCH_TACTICS = ["exact?", "simp?"]

DERIV_TEMPLATES = [
    "exact (Real.hasDerivAt_sin _).const_mul _",
    "exact (Real.hasDerivAt_cos _).const_mul _",
    "exact (Real.hasDerivAt_exp _).const_mul _",
    "exact (Real.hasDerivAt_sin _).neg",
    "exact (Real.hasDerivAt_cos _).neg",
    "exact (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)",
    "exact (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)",
    "have h := (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 1\n  ring",
    "have h := (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 1\n  ring",
    "have h := (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 2\n  ring",
    "have h := (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)\n  convert h using 2\n  ring",
    "ring_nf\n  exact (Real.hasDerivAt_sin _).comp _ ((hasDerivAt_id _).const_mul _)",
    "ring_nf\n  exact (Real.hasDerivAt_cos _).comp _ ((hasDerivAt_id _).const_mul _)",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  convert h using 2\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id_eq] at h\n  norm_num at h\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id_eq] at h\n  norm_num at h\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_sin _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id_eq, mul_one] at h\n  convert h using 1\n  ring",
    "have hf := (hasDerivAt_id _).const_mul _\n  have hg := Real.hasDerivAt_cos _\n  have h := hg.comp _ hf\n  simp only [Function.comp, id_eq, mul_one] at h\n  convert h using 1\n  ring",
    "exact hasDerivAt_id _",
    "exact hasDerivAt_const _ _",
]

FINSET_CARD_TEMPLATES = [
    "have h : (Finset.range (2 * n)).filter (fun k => k % 2 = 0) = (Finset.range n).image (2 * ·) := by\n    ext k\n    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]\n    constructor\n    · intro ⟨hk, hmod⟩; exact ⟨k / 2, by omega, by omega⟩\n    · rintro ⟨m, hm, rfl⟩; exact ⟨by omega, by omega⟩\n  rw [h, Finset.card_image_of_injective _ (fun a b hab => by omega)]\n  simp",
    "have h : (Finset.range (2 * n)).filter (fun k => k % 2 = 0) = (Finset.range n).image (· * 2) := by\n    ext k\n    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]\n    constructor\n    · intro ⟨hk, hmod⟩; exact ⟨k / 2, by omega, by omega⟩\n    · rintro ⟨m, hm, rfl⟩; exact ⟨by omega, by omega⟩\n  rw [h, Finset.card_image_of_injective _ (fun a b hab => by omega)]\n  simp",
    "have h : (Finset.range (2 * n)).filter (fun k => k % 2 ≠ 0) = (Finset.range n).image (2 * · + 1) := by\n    ext k\n    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]\n    constructor\n    · intro ⟨hk, hmod⟩; exact ⟨k / 2, by omega, by omega⟩\n    · rintro ⟨m, hm, rfl⟩; exact ⟨by omega, by omega⟩\n  rw [h, Finset.card_image_of_injective _ (fun a b hab => by omega)]\n  simp",
]

FINTYPE_TEMPLATES = [
    "apply Fintype.exists_ne_map_eq_of_card_lt\n  simp [Fintype.card_fin, *]",
    "apply Fintype.exists_ne_map_eq_of_card_lt\n  simp [Fintype.card_fin]\n  omega",
    "apply Fintype.exists_ne_map_eq_of_card_lt\n  omega",
]

STEP_TACTICS = [
    "intro h", "intro hp hq", "intro hp hq hr",
    "exact h", "exact hp", "exact hq", "exact hr",
    "apply h", "apply hp", "apply hq",
    "assumption",
    "constructor", "left", "right",
    "rcases h with ha | hb",
    "obtain ⟨a, b⟩ := h",
    "tauto", "simp", "ring", "omega", "norm_num", "linarith", "aesop",
    "fun_prop", "norm_cast",
    "apply HasDerivAt.const_mul", "apply HasDerivAt.comp",
    "apply HasDerivAt.neg", "apply HasDerivAt.add",
    "exact Real.hasDerivAt_sin _", "exact Real.hasDerivAt_cos _",
    "exact hasDerivAt_id _",
    "exact real_inner_comm _ _", "exact inner_add_left _ _ _",
    "exact inner_self_eq_zero", "exact norm_smul _ _",
    "simp [inner_smul_left]", "simp [real_inner_self_eq_norm_sq]",
    "simp [EuclideanSpace.inner_single_left]", "simp [EuclideanSpace.norm_single]",
    "simp [normSq_apply, sq]", "congr 1",
    "apply Fintype.exists_ne_map_eq_of_card_lt",
    "simp [Fintype.card_fin]", "simp [Fintype.card_fin, *]",
]

STEP_TIME_LIMIT = 10
DEFAULT_THEOREM_TIMEOUT = 60


def extract_try_this(resp: dict) -> str | None:
    for msg in resp.get("messages", []):
        data = msg.get("data", "")
        m = re.search(r"Try this:[ \t]*\n?[ \t]*(?:\[\w+\] )?(.+)", data)
        if m:
            return m.group(1).strip()
    return None


def goal_has_symmetric_target(goal: str) -> bool:
    target_lines = [line for line in goal.splitlines() if "⊢" in line]
    if not target_lines:
        return False
    target = target_lines[-1]
    return " = " in target or " ↔ " in target


def search_suggestion_variants(suggestion: str, goal: str) -> list[str]:
    variants: list[str] = []

    def add_variant(tactic: str):
        if tactic not in variants:
            variants.append(tactic)

    add_variant(suggestion)

    if suggestion.startswith("exact "):
        expr = suggestion[len("exact "):].strip()
        if expr:
            add_variant(f"simpa using {expr}")
            if goal_has_symmetric_target(goal):
                symm_expr = f"({expr}).symm"
                add_variant(f"exact {symm_expr}")
                add_variant(f"simpa using {symm_expr}")

    return variants


def search_normalization_prefixes(goal: str) -> list[str]:
    """Lightweight normalisation passes to run around search tactics.

    Keep this list short: these prefixes are reused around `exact?`, `simp?`,
    and `apply?`, so every extra branch has a real runtime cost.
    """
    prefixes = [""]

    def add_prefix(prefix: str):
        if prefix not in prefixes:
            prefixes.append(prefix)

    if "↑" in goal or "ZMod" in goal or "Nat.cast" in goal or "Int.cast" in goal:
        add_prefix("norm_cast\n  ")
        add_prefix("push_cast\n  ")

    if any(token in goal for token in [" + ", " - ", " * ", "^", " / "]):
        add_prefix("ring_nf\n  ")

    if re.search(r'\b\d+\b', goal):
        add_prefix("norm_num\n  ")

    if " = " in goal or " ≤ " in goal or " ≥ " in goal or " ↔ " in goal:
        add_prefix("simp\n  ")

    return prefixes


def verify_tactic_variants(session, example: str, base_env: int,
                           tactics: list[str], prefix: str = "",
                           normalization_prefixes: list[str] | None = None) -> str | None:
    prefixes = normalization_prefixes or [""]
    for norm_prefix in prefixes:
        for tactic in tactics:
            body = f"{prefix}{norm_prefix}{tactic}" if prefix or norm_prefix else tactic
            resp = session.send({"cmd": f"{example} := by\n  {body}", "env": base_env})
            if not has_error(resp):
                return body
    return None


def to_example(stmt: str) -> str:
    return re.sub(r"^theorem\s+\S+", "example", stmt)


def extract_nonneg_triples(goal: str) -> list[tuple[str, str]]:
    return re.findall(r'(\w+)\s*:\s*0\s*≤\s*(\w+)', goal)


def extract_chain_rule_params(goal: str) -> tuple[str, str, str] | None:
    m = re.search(r'HasDerivAt \(fun \w+ => Real\.(sin|cos|exp) \((\S+) \* \w+\)\)', goal)
    if not m:
        return None
    fn = m.group(1)
    coeff = m.group(2)
    goal_line = [line for line in goal.splitlines() if "⊢" in line]
    if not goal_line:
        return None
    pt = goal_line[0].split()[-1]
    return fn, coeff, pt


def chain_rule_deriv_tactics(goal: str) -> list[str]:
    params = extract_chain_rule_params(goal)
    if not params:
        return []
    fn, coeff, pt = params
    inner = f"({coeff} * {pt})"
    base = f"(Real.hasDerivAt_{fn} {inner}).comp {pt} ((hasDerivAt_id {pt}).const_mul {coeff})"
    deriv_map = {
        "sin": f"Real.cos {inner}",
        "cos": f"-Real.sin {inner}",
        "exp": f"Real.exp {inner}",
    }
    deriv = deriv_map[fn]
    return [
        (
            f"have hf : HasDerivAt (fun x => {coeff} * x) {coeff} {pt} := by\n"
            f"    simpa using (hasDerivAt_id {pt}).const_mul {coeff}\n"
            f"  have hg : HasDerivAt Real.{fn} ({deriv}) {inner} :=\n"
            f"    Real.hasDerivAt_{fn} {inner}\n"
            f"  have h := hg.comp {pt} hf\n"
            f"  convert h using 1\n"
            f"  ring"
        ),
        f"have h := {base}\n  simp only [Function.comp, id_eq, mul_one] at h\n  convert h using 1\n  ring",
        f"have h := {base}\n  simp only [Function.comp, id_eq, mul_one, mul_comm] at h\n  exact h",
        f"have h := {base}\n  convert h using 1\n  ring",
    ]


def extract_real_vars(goal: str) -> list[str]:
    result, seen = [], set()
    for m in re.finditer(r'(\b\w+(?:\s+\w+)*)\s*:\s*[ℝℚ]', goal):
        for name in m.group(1).split():
            if name not in seen:
                seen.add(name)
                result.append(name)
    return result


def nlinarith_pairwise_sq_tactic(goal: str) -> str | None:
    vars_ = extract_real_vars(goal)
    if len(vars_) < 2:
        return None
    witnesses = [
        f"sq_nonneg ({vars_[i]} - {vars_[j]})"
        for i in range(len(vars_))
        for j in range(i + 1, len(vars_))
    ]
    if len(vars_) >= 4:
        a, b, c, d = vars_[0], vars_[1], vars_[2], vars_[3]
        witnesses.append(f"sq_nonneg ({a}*{d} - {b}*{c})")
    return "nlinarith [" + ", ".join(witnesses) + "]"


def nlinarith_nonneg3_tactic(goal: str) -> str | None:
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


def select_tactics(goal: str) -> list[str]:
    if (re.search(r'\binner\b', goal) and ("ℝ" in goal or "𝕜" in goal)) or "⟪" in goal:
        return INNER_PRODUCT_TACTICS + SEARCH_TACTICS
    if "‖" in goal and "•" in goal:
        return ["exact norm_smul _ _", "simp [norm_smul]"] + INNER_PRODUCT_TACTICS + SEARCH_TACTICS
    if "normSq" in goal:
        return COMPLEX_TACTICS + SEARCH_TACTICS
    if "exp" in goal and re.search(r'\^\s*\w+', goal) and ("Complex" in goal or "ℂ" in goal or re.search(r'\bI\b', goal)):
        return COMPLEX_TACTICS + SEARCH_TACTICS
    if "HasDerivAt" in goal or "HasFDerivAt" in goal:
        chain_tactics = chain_rule_deriv_tactics(goal)
        return chain_tactics + DERIV_TEMPLATES + ["fun_prop", "simp"] + SEARCH_TACTICS
    if "Continuous" in goal or "Differentiable" in goal:
        return ["fun_prop", "simp", "aesop"] + SEARCH_TACTICS
    if "cos" in goal and "sin" in goal and ("≤" in goal or re.search(r'⊢[^\n]*(?<!=)=(?![>=])', goal)):
        return TRIG_DOUBLE_TACTICS + SIMPLE_TACTICS + SEARCH_TACTICS
    if "∑" in goal or "Finset" in goal:
        if ".card" in goal:
            return FINSET_CARD_TEMPLATES + INDUCTION_TACTICS + SEARCH_TACTICS
        return INDUCTION_TACTICS + SEARCH_TACTICS
    if "Irrational" in goal:
        return SEARCH_TACTICS
    if "∃" in goal and "Fin" in goal:
        return FINTYPE_TEMPLATES + SEARCH_TACTICS
    if "!" in goal and "Nat.Prime" in goal:
        match = re.search(r'(\w+)\s*:\s*Nat\.Prime\s+(\w+)', goal)
        if match:
            hname, pvar = match.group(1), match.group(2)
            return [
                f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩\n  exact ZMod.wilsons_lemma {pvar}",
                f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩\n  simp [ZMod.wilsons_lemma]",
            ] + SEARCH_TACTICS
    if "ZMod" in goal:
        return ["norm_cast", "push_cast; ring", "simp"] + SEARCH_TACTICS
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


def prove_iterative(session, example: str, base_env: int, time_limit: int = STEP_TIME_LIMIT,
                    deadline: float | None = None) -> str | None:
    resp = session.send({"cmd": f"{example} := by sorry", "env": base_env})
    sorries = resp.get("sorries", [])
    if not sorries:
        return None
    init_state = sorries[0].get("proofState")
    if init_state is None:
        return None

    phase_deadline = time.time() + time_limit
    if deadline is not None:
        phase_deadline = min(phase_deadline, deadline)
    queue: deque[tuple[int, list[str]]] = deque([(init_state, [])])
    visited: set[int] = set()

    while queue and time.time() < phase_deadline:
        state, applied = queue.popleft()
        if len(applied) >= 6 or state in visited:
            continue
        visited.add(state)

        for tactic in STEP_TACTICS:
            if time.time() > phase_deadline:
                return None
            resp = session.send({"tactic": tactic, "proofState": state})
            if has_error(resp):
                continue
            goals = resp.get("goals")
            new_state = resp.get("proofState")
            if goals is None and new_state is None:
                continue
            new_applied = applied + [tactic]
            if goals == []:
                return "\n".join(new_applied)
            if new_state is not None and goals is not None and len(goals) <= 4:
                queue.append((new_state, new_applied))

    return None


def have_candidates(goal: str) -> list[str]:
    candidates = []

    for m in re.finditer(r'(\w+)\s*:\s*(\w+(?:\s+\w+)?)\s*≠\s*0', goal):
        hname = m.group(1)
        expr = m.group(2).strip()
        expr_lean = f"({expr})" if " " in expr else expr
        candidates.append(f"have {hname}2 : {expr_lean} ^ 2 ≠ 0 := pow_ne_zero 2 {hname}")

    if "sin" in goal or "cos" in goal:
        seen: set[str] = set()
        for m in re.finditer(r'(?:sin|cos)\s+(\w+)', goal):
            var = m.group(1)
            if var not in seen:
                seen.add(var)
                candidates.append(f"have hsc_{var} := sin_sq_add_cos_sq {var}")
                candidates.append(f"have hsc_{var} := Real.sin_sq_add_cos_sq {var}")

    for m in re.finditer(r'(\w+)\s*:\s*0\s*<\s*(\w+)', goal):
        hname, var = m.group(1), m.group(2)
        candidates.append(f"have {hname}' : 0 ≤ {var} := le_of_lt {hname}")

    if "≤" in goal or "≥" in goal or "<" in goal or ">" in goal:
        vars_ = extract_real_vars(goal)
        for i in range(min(len(vars_), 3)):
            for j in range(i + 1, min(len(vars_), 3)):
                candidates.append(f"have hnn_{i}{j} := sq_nonneg ({vars_[i]} - {vars_[j]})")

    return candidates


def have_closers(have_line: str, remaining_goal: str) -> list[str]:
    match = re.match(r'have\s+(\w+)\b', have_line)
    name = match.group(1) if match else None
    closers = [
        "ring", "linarith", "nlinarith", "simp", "omega",
        "field_simp; ring", "field_simp; linarith",
        "field_simp; nlinarith", "simp_all",
    ]
    if name:
        closers = [
            f"field_simp [{name}]; ring",
            f"field_simp [{name}]; linarith",
            f"field_simp [{name}]; nlinarith",
            f"simp [{name}]",
            f"linarith [{name}]",
            f"nlinarith [{name}]",
            f"nlinarith [{name}, sq_nonneg _]",
        ] + closers
    closers += select_tactics(remaining_goal)[:8]
    return closers


def prove_with_have(session, example: str, base_env: int,
                    have_line: str, deadline: float | None = None) -> str | None:
    if deadline is not None and time.monotonic() >= deadline:
        return None
    probe = session.send({"cmd": f"{example} := by\n  {have_line}\n  sorry", "env": base_env})
    if has_error(probe):
        return None
    sorries = probe.get("sorries", [])
    if not sorries:
        return have_line
    remaining_goal = sorries[0].get("goal", "")
    for closer in have_closers(have_line, remaining_goal):
        if deadline is not None and time.monotonic() >= deadline:
            return None
        resp = session.send({"cmd": f"{example} := by\n  {have_line}\n  {closer}", "env": base_env})
        if not has_error(resp):
            return f"{have_line}\n  {closer}"
    return None


def fact_preamble(stmt: str) -> str:
    lines = []
    for m in re.finditer(r'\((\w+)\s*:\s*Nat\.Prime\s+(\w+)\)', stmt):
        hname, pvar = m.group(1), m.group(2)
        lines.append(f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩")
    return "\n  ".join(lines)
