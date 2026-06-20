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
HAVE_STAGE1_LIMIT = 6
HAVE_STAGE2_LIMIT = 4
BFS_TACTIC_LIMIT = 12


def goal_target(goal: str) -> str:
    """Extract the target line (without the leading turnstile) when present."""
    for line in reversed(goal.splitlines()):
        if "⊢" in line:
            return line.split("⊢", 1)[1].strip()
    return goal.strip()


def target_has_order_relation(target: str) -> bool:
    return any(token in target for token in [" ≤ ", " ≥ ", " < ", " > "])


def extract_try_this(resp: dict) -> str | None:
    for msg in resp.get("messages", []):
        data = msg.get("data", "")
        m = re.search(r"Try this:[ \t]*\n?[ \t]*(?:\[\w+\] )?(.+)", data)
        if m:
            return m.group(1).strip()
    return None


def goal_has_symmetric_target(goal: str) -> bool:
    target = goal_target(goal)
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


def extract_has_deriv_expr(goal: str) -> tuple[str, str, str] | None:
    target = goal_target(goal)
    m = re.search(r'HasDerivAt\s+\(fun\s+(\w+)\s*=>\s*(.+)\)\s+\((.+)\)\s+(.+)$', target)
    if not m:
        return None
    var = m.group(1).strip()
    expr = m.group(2).strip()
    deriv = m.group(3).strip()
    point = m.group(4).strip()
    return var, expr, point


def extract_tendsto_lambda(goal: str) -> tuple[str, str, str] | None:
    target = goal_target(goal)
    m = re.search(r'Tendsto\s+\(fun\s+(\w+)\s*=>\s*(.+)\)\s+\(𝓝\s+(.+?)\)\s+\(𝓝\s+(.+)\)', target)
    if not m:
        return None
    var = m.group(1).strip()
    expr = m.group(2).strip()
    point = m.group(3).strip()
    return var, expr, point


def extract_cos_ne_zero(goal: str) -> tuple[str, str] | None:
    m = re.search(r'(\w+)\s*:\s*cos\s+(.+?)\s*≠\s*0', goal)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


def extract_double_angle_arg(target: str) -> str | None:
    m = re.search(r'cos\s+\(2\s*\*\s*(.+?)\)', target)
    if not m:
        return None
    return m.group(1).strip()


def tendsto_templates(goal: str) -> list[str]:
    params = extract_tendsto_lambda(goal)
    if not params:
        return []
    var, expr, point = params
    fn = f"(fun {var} => {expr})"
    return [
        (
            f"have hcont : ContinuousAt {fn} {point} := by\n"
            f"    fun_prop\n"
            f"  simpa using hcont"
        ),
        f"simpa using (show ContinuousAt {fn} {point} from by fun_prop)",
    ]


def polynomial_deriv_templates(goal: str) -> list[str]:
    params = extract_has_deriv_expr(goal)
    if not params:
        return []
    var, expr, point = params
    m = re.fullmatch(
        rf'{re.escape(var)}\s*\^\s*(\d+)\s*\+\s*(.+?)\s*\*\s*{re.escape(var)}\s*\+\s*(.+)',
        expr,
    )
    if not m:
        return []
    power = m.group(1).strip()
    coeff = m.group(2).strip()
    const = m.group(3).strip()
    return [
        (
            f"have h1 : HasDerivAt (fun {var} => {var} ^ {power}) ({power} * {point} ^ ({power} - 1)) {point} := by\n"
            f"    simpa using hasDerivAt_pow {power} {point}\n"
            f"  have h2 : HasDerivAt (fun {var} => {coeff} * {var}) ({coeff} * 1) {point} :=\n"
            f"    (hasDerivAt_id {point}).const_mul {coeff}\n"
            f"  have h3 : HasDerivAt (fun _ => ({const})) 0 {point} := hasDerivAt_const {point} ({const})\n"
            f"  have h := h1.add h2\n"
            f"  have h' := h.add h3\n"
            f"  convert h' using 1\n"
            f"  ring"
        ),
    ]


def product_deriv_templates(goal: str) -> list[str]:
    params = extract_has_deriv_expr(goal)
    if not params:
        return []
    var, expr, point = params
    templates: list[str] = []

    m = re.fullmatch(rf'{re.escape(var)}\s*\*\s*\(\s*{re.escape(var)}\s*\+\s*(.+)\)', expr)
    if m:
        const = m.group(1).strip()
        templates.append(
            f"have hf := hasDerivAt_id {point}\n"
            f"  have hg : HasDerivAt (fun {var} => {var} + {const}) 1 {point} := by\n"
            f"    have h := hf.add (hasDerivAt_const {point} ({const}))\n"
            f"    convert h using 1\n"
            f"    norm_num\n"
            f"  have h := hf.mul hg\n"
            f"  convert h using 1\n"
            f"  simp\n"
            f"  ring"
        )

    m = re.fullmatch(rf'Real\.sin\s+{re.escape(var)}\s*\*\s*Real\.cos\s+{re.escape(var)}', expr)
    if m:
        templates.append(
            f"have hf := Real.hasDerivAt_sin {point}\n"
            f"  have hg := Real.hasDerivAt_cos {point}\n"
            f"  have h := hf.mul hg\n"
            f"  convert h using 1\n"
            f"  ring"
        )

    return templates


def trig_identity_templates(goal: str) -> list[str]:
    target = goal_target(goal)
    templates: list[str] = []

    cos_ne_zero = extract_cos_ne_zero(goal)
    if "tan" in target and "cos" in target and " = " in target and cos_ne_zero:
        hname, arg = cos_ne_zero
        templates.extend([
            (
                "simp only [Real.tan_eq_sin_div_cos, div_pow]\n"
                f"  have hx2 : cos {arg} ^ 2 ≠ 0 := pow_ne_zero 2 {hname}\n"
                "  field_simp [hx2]\n"
                f"  linarith [sin_sq_add_cos_sq {arg}]"
            ),
            (
                f"have hx2 : cos {arg} ^ 2 ≠ 0 := pow_ne_zero 2 {hname}\n"
                "  field_simp [Real.tan_eq_sin_div_cos, hx2]\n"
                f"  linarith [sin_sq_add_cos_sq {arg}]"
            ),
        ])

    double_arg = extract_double_angle_arg(target)
    if double_arg and "sin" in target and " = " in target:
        templates.extend([
            f"rw [cos_double]\n  linarith [sin_sq_add_cos_sq {double_arg}]",
            f"rw [Real.cos_two_mul]\n  linarith [Real.sin_sq_add_cos_sq {double_arg}]",
            f"rw [cos_two_mul]\n  linarith [sin_sq_add_cos_sq {double_arg}]",
        ])

    return templates


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
    target = goal_target(goal)

    if (re.search(r'\binner\b', target) and ("ℝ" in goal or "𝕜" in goal)) or "⟪" in target:
        return INNER_PRODUCT_TACTICS + SEARCH_TACTICS
    if "‖" in target and "•" in target:
        return ["exact norm_smul _ _", "simp [norm_smul]"] + INNER_PRODUCT_TACTICS + SEARCH_TACTICS
    if "normSq" in target:
        return COMPLEX_TACTICS + SEARCH_TACTICS
    if "exp" in target and re.search(r'\^\s*\w+', target) and ("Complex" in goal or "ℂ" in goal or re.search(r'\bI\b', target)):
        return COMPLEX_TACTICS + SEARCH_TACTICS
    if "Tendsto" in target:
        return tendsto_templates(goal) + ["fun_prop", "simp", "aesop"] + SEARCH_TACTICS
    if "HasDerivAt" in target or "HasFDerivAt" in target:
        chain_tactics = chain_rule_deriv_tactics(goal)
        structural_tactics = polynomial_deriv_templates(goal) + product_deriv_templates(goal)
        return structural_tactics + chain_tactics + DERIV_TEMPLATES + ["fun_prop", "simp"] + SEARCH_TACTICS
    if "Continuous" in target or "Differentiable" in target:
        return ["fun_prop", "simp", "aesop"] + SEARCH_TACTICS
    if "cos" in target and "sin" in target and ("≤" in target or re.search(r'(?<![<>=!])=(?![>=])', target)):
        return trig_identity_templates(goal) + TRIG_DOUBLE_TACTICS + SIMPLE_TACTICS + SEARCH_TACTICS
    if "∑" in target or "Finset" in target:
        if ".card" in target:
            return FINSET_CARD_TEMPLATES + INDUCTION_TACTICS + SEARCH_TACTICS
        return INDUCTION_TACTICS + SEARCH_TACTICS
    if "Irrational" in target:
        return SEARCH_TACTICS
    if "∃" in target and "Fin" in goal:
        return FINTYPE_TEMPLATES + SEARCH_TACTICS
    if "!" in goal and "Nat.Prime" in goal:
        match = re.search(r'(\w+)\s*:\s*Nat\.Prime\s+(\w+)', goal)
        if match:
            hname, pvar = match.group(1), match.group(2)
            return [
                f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩\n  exact ZMod.wilsons_lemma {pvar}",
                f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩\n  simp [ZMod.wilsons_lemma]",
            ] + SEARCH_TACTICS
    if "ZMod" in goal or "ZMod" in target:
        return ["norm_cast", "push_cast; ring", "simp"] + SEARCH_TACTICS
    if target_has_order_relation(target) and "^" in target:
        tactics: list[str] = []
        nonneg_tac = nlinarith_nonneg3_tactic(goal)
        pairwise_tac = nlinarith_pairwise_sq_tactic(goal)
        if nonneg_tac:
            tactics += [nonneg_tac, "field_simp\n  " + nonneg_tac]
        if pairwise_tac:
            tactics.append(pairwise_tac)
        if tactics:
            return tactics + ["ring", "nlinarith", "linarith"] + SEARCH_TACTICS
    if "^" in target:
        return ["ring", "nlinarith", "norm_num"] + SEARCH_TACTICS
    if "ℝ" in goal or "ℚ" in goal:
        return ["ring", "linarith", "norm_num", "nlinarith", "fun_prop"] + SEARCH_TACTICS
    if "ℕ" in goal or "ℤ" in goal:
        return ["omega", "simp", "rfl", "decide", "ring", "norm_num", "norm_cast"] + SEARCH_TACTICS
    return ALL_TACTICS + SEARCH_TACTICS


def extract_goal_text(goal_entry) -> str:
    if isinstance(goal_entry, str):
        return goal_entry
    if isinstance(goal_entry, dict):
        for key in ["goal", "type", "target"]:
            value = goal_entry.get(key)
            if isinstance(value, str):
                return value
    return ""


def step_tactics_for_goal(goal: str) -> list[str]:
    target = goal_target(goal)
    tactics: list[str] = []

    def add_many(items: list[str]):
        for item in items:
            if item not in tactics:
                tactics.append(item)

    add_many(["assumption", "constructor", "left", "right", "simp", "aesop"])

    if "→" in target or "∀" in target:
        add_many(["intro h", "intro hp hq", "intro hp hq hr"])
    if "∧" in target or "∃" in target:
        add_many(["constructor", "obtain ⟨a, b⟩ := h"])
    if "∨" in target:
        add_many(["left", "right", "rcases h with ha | hb"])
    if "HasDerivAt" in target or "HasFDerivAt" in target:
        add_many([
            "apply HasDerivAt.comp", "apply HasDerivAt.add",
            "apply HasDerivAt.const_mul", "apply HasDerivAt.neg",
            "exact Real.hasDerivAt_sin _", "exact Real.hasDerivAt_cos _",
            "exact hasDerivAt_id _", "fun_prop",
        ])
    if "∑" in target or "Finset" in target:
        add_many(["ring", "omega", "linarith"])
    if "inner" in target or "⟪" in target or "‖" in target:
        add_many([
            "exact real_inner_comm _ _", "exact inner_add_left _ _ _",
            "exact inner_self_eq_zero", "exact norm_smul _ _",
            "simp [inner_smul_left]", "simp [real_inner_self_eq_norm_sq]",
        ])
    if "normSq" in target or ("exp" in target and "ℂ" in goal):
        add_many(["simp [normSq_apply, sq]", "congr 1", "ring"])
    if "^" in target or any(tok in target for tok in [" + ", " - ", " * ", " / "]):
        add_many(["ring", "nlinarith", "linarith", "norm_num"])
    if "ℕ" in goal or "ℤ" in goal:
        add_many(["omega", "rfl", "decide", "norm_cast"])

    add_many(["tauto", "norm_num", "ring", "omega"])
    return tactics[:BFS_TACTIC_LIMIT]


def single_line_closers(goal: str) -> list[str]:
    target = goal_target(goal)
    closers: list[str] = []

    def add_many(items: list[str]):
        for item in items:
            if "\n" in item:
                continue
            if item in SEARCH_TACTICS:
                continue
            if item not in closers:
                closers.append(item)

    add_many(["simp", "simp [*]", "simp_all", "aesop"])

    if "HasDerivAt" in target or "HasFDerivAt" in target:
        add_many(["fun_prop", "ring", "norm_num", "linarith"])
    if "Tendsto" in target or "Continuous" in target or "Differentiable" in target:
        add_many(["fun_prop", "simpa", "simp"])
    if "∑" in target or "Finset" in target:
        add_many(["omega", "ring", "linarith", "nlinarith"])
    if "inner" in target or "⟪" in target or "‖" in target:
        add_many(["simp", "ring", "nlinarith"])
    if "ZMod" in goal or "↑" in goal:
        add_many(["norm_cast", "push_cast; ring", "norm_num"])
    if "^" in target or any(tok in target for tok in [" + ", " - ", " * ", " / "]):
        add_many(["ring", "nlinarith", "linarith", "norm_num"])
    if "ℕ" in goal or "ℤ" in goal:
        add_many(["omega", "rfl", "decide", "norm_num"])

    add_many(select_tactics(goal)[:8])
    add_many(["omega", "ring", "nlinarith", "linarith", "norm_num"])
    return closers[:12]


def probe_apply_subgoal(session, example: str, base_env: int,
                        prefix_lines: list[str], suggestion: str) -> str | None:
    prefix = "\n  ".join(line for line in prefix_lines if line)
    body = f"{prefix}\n  {suggestion}\n  sorry" if prefix else f"{suggestion}\n  sorry"
    probe = session.send({"cmd": f"{example} := by\n  {body}", "env": base_env})
    if has_error(probe):
        return None
    sorries = probe.get("sorries", [])
    if not sorries:
        return ""
    return sorries[0].get("goal", "")


def prove_iterative(session, example: str, base_env: int, time_limit: int = STEP_TIME_LIMIT,
                    deadline: float | None = None) -> str | None:
    resp = session.send({"cmd": f"{example} := by sorry", "env": base_env})
    sorries = resp.get("sorries", [])
    if not sorries:
        return None
    init_state = sorries[0].get("proofState")
    if init_state is None:
        return None
    init_goal = sorries[0].get("goal", "")

    phase_deadline = time.time() + time_limit
    if deadline is not None:
        phase_deadline = min(phase_deadline, deadline)
    queue: deque[tuple[int, list[str], str]] = deque([(init_state, [], init_goal)])
    visited: set[int] = set()

    while queue and time.time() < phase_deadline:
        state, applied, current_goal = queue.popleft()
        if len(applied) >= 6 or state in visited:
            continue
        visited.add(state)

        for tactic in step_tactics_for_goal(current_goal):
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
                next_goal = extract_goal_text(goals[0]) if goals else current_goal
                queue.append((new_state, new_applied, next_goal))

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


def limited_have_candidates(goal: str, limit: int, exclude: set[str] | None = None) -> list[str]:
    seen = set(exclude or set())
    result = []
    for candidate in have_candidates(goal):
        if candidate in seen:
            continue
        seen.add(candidate)
        result.append(candidate)
        if len(result) >= limit:
            break
    return result


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


def probe_have_prefix(session, example: str, base_env: int,
                      have_lines: list[str], deadline: float | None = None) -> str | None:
    if deadline is not None and time.monotonic() >= deadline:
        return None
    prefix = "\n  ".join(have_lines)
    probe = session.send({"cmd": f"{example} := by\n  {prefix}\n  sorry", "env": base_env})
    if has_error(probe):
        return None
    sorries = probe.get("sorries", [])
    if not sorries:
        return ""
    return sorries[0].get("goal", "")


def prove_with_have_chain(session, example: str, base_env: int,
                          have_lines: list[str], deadline: float | None = None) -> str | None:
    remaining_goal = probe_have_prefix(session, example, base_env, have_lines, deadline)
    if remaining_goal is None:
        return None
    prefix = "\n  ".join(have_lines)
    if remaining_goal == "":
        return prefix
    lead_have = have_lines[-1]
    for closer in have_closers(lead_have, remaining_goal):
        if deadline is not None and time.monotonic() >= deadline:
            return None
        resp = session.send({"cmd": f"{example} := by\n  {prefix}\n  {closer}", "env": base_env})
        if not has_error(resp):
            return f"{prefix}\n  {closer}"
    return None


def prove_with_have(session, example: str, base_env: int,
                    have_line: str, deadline: float | None = None) -> str | None:
    return prove_with_have_chain(session, example, base_env, [have_line], deadline)


def prove_with_two_haves(session, example: str, base_env: int,
                         first_have: str, deadline: float | None = None) -> str | None:
    remaining_goal = probe_have_prefix(session, example, base_env, [first_have], deadline)
    if remaining_goal is None or remaining_goal == "":
        return None
    second_haves = limited_have_candidates(
        remaining_goal,
        HAVE_STAGE2_LIMIT,
        exclude={first_have},
    )
    for second_have in second_haves:
        if deadline is not None and time.monotonic() >= deadline:
            return None
        proof = prove_with_have_chain(
            session, example, base_env, [first_have, second_have], deadline
        )
        if proof is not None:
            return proof
    return None


def fact_preamble(stmt: str) -> str:
    lines = []
    for m in re.finditer(r'\((\w+)\s*:\s*Nat\.Prime\s+(\w+)\)', stmt):
        hname, pvar = m.group(1), m.group(2)
        lines.append(f"haveI : Fact (Nat.Prime {pvar}) := ⟨{hname}⟩")
    return "\n  ".join(lines)
