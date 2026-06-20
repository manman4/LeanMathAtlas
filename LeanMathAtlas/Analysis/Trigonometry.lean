import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# Trigonometry

Fundamental identities for `Real.sin` and `Real.cos`:
Pythagorean identity, addition formulas, and double-angle formulas.

**Requires**: `ℝ`, `Real.sin`, `Real.cos`, `Real.tan`
**Tags**: Analysis, Trigonometry
-/

open Real

-- ============================================================
-- 1. 基本公式 (数I)
-- ============================================================

-- sin²x + cos²x = 1
theorem pythagorean (x : ℝ) : sin x ^ 2 + cos x ^ 2 = 1 :=
  sin_sq_add_cos_sq x

-- cos²x = 1 - sin²x
theorem cos_sq_eq (x : ℝ) : cos x ^ 2 = 1 - sin x ^ 2 := by
  linarith [sin_sq_add_cos_sq x]

-- sin²x = 1 - cos²x
theorem sin_sq_eq (x : ℝ) : sin x ^ 2 = 1 - cos x ^ 2 := by
  linarith [sin_sq_add_cos_sq x]

-- tan x = sin x / cos x（cos x ≠ 0 のとき）
theorem tan_def (x : ℝ) : tan x = sin x / cos x := by
  simp only [Real.tan_eq_sin_div_cos]

-- 1 + tan²x = 1/cos²x（cos x ≠ 0 のとき）
theorem one_add_tan_sq (x : ℝ) (hx : cos x ≠ 0) :
    1 + tan x ^ 2 = 1 / cos x ^ 2 := by
  simp only [Real.tan_eq_sin_div_cos, div_pow]
  have hx2 : cos x ^ 2 ≠ 0 := pow_ne_zero 2 hx
  field_simp [hx2]
  linarith [sin_sq_add_cos_sq x]

-- ============================================================
-- 2. 加法定理 (数II)
-- ============================================================

theorem sin_add_formula (x y : ℝ) :
    sin (x + y) = sin x * cos y + cos x * sin y :=
  Real.sin_add x y

theorem cos_add_formula (x y : ℝ) :
    cos (x + y) = cos x * cos y - sin x * sin y :=
  Real.cos_add x y

theorem sin_sub_formula (x y : ℝ) :
    sin (x - y) = sin x * cos y - cos x * sin y :=
  Real.sin_sub x y

theorem cos_sub_formula (x y : ℝ) :
    cos (x - y) = cos x * cos y + sin x * sin y :=
  Real.cos_sub x y

-- ============================================================
-- 3. 2倍角公式 (数II)
-- ============================================================

theorem sin_double (x : ℝ) : sin (2 * x) = 2 * sin x * cos x := by
  rw [two_mul, Real.sin_add]; ring

theorem cos_double (x : ℝ) : cos (2 * x) = cos x ^ 2 - sin x ^ 2 := by
  rw [two_mul, Real.cos_add]; ring

-- cos の 2倍角（sin で表す）
theorem cos_double_sin (x : ℝ) : cos (2 * x) = 1 - 2 * sin x ^ 2 := by
  rw [cos_double]; linarith [sin_sq_add_cos_sq x]

-- cos の 2倍角（cos で表す）
theorem cos_double_cos (x : ℝ) : cos (2 * x) = 2 * cos x ^ 2 - 1 := by
  rw [cos_double]; linarith [sin_sq_add_cos_sq x]

-- sin²x ≤ 1
theorem sin_sq_le_one (x : ℝ) : sin x ^ 2 ≤ 1 := by
  have hsc := sin_sq_add_cos_sq x
  nlinarith [hsc, sq_nonneg (cos x)]

-- 2sin²x ≤ 2
theorem two_mul_sin_sq_le_two (x : ℝ) : 2 * sin x ^ 2 ≤ 2 := by
  nlinarith [sin_sq_add_cos_sq x, sq_nonneg (cos x)]

-- ============================================================
-- 4. 特殊値 (数I)
-- ============================================================

theorem sin_zero : sin 0 = 0 := Real.sin_zero

theorem cos_zero : cos 0 = 1 := Real.cos_zero

theorem sin_pi_div_two : sin (π / 2) = 1 := Real.sin_pi_div_two

theorem cos_pi_div_two : cos (π / 2) = 0 := Real.cos_pi_div_two

theorem sin_pi : sin π = 0 := Real.sin_pi

theorem cos_pi : cos π = -1 := Real.cos_pi
