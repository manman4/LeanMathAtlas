import Mathlib.Tactic
import Mathlib.Algebra.Polynomial.Div

/-!
# Basic Algebraic Identities

Expansion and factoring formulas, quadratic inequalities,
and the factor/remainder theorems for polynomials.

**Requires**: `ℝ`, `Polynomial`
**Tags**: Algebra, Polynomial
-/

open Polynomial

-- ============================================================
-- 1. 式の展開公式 (数I)
-- ============================================================

theorem sq_sum (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by ring

theorem sq_diff (a b : ℝ) : (a - b)^2 = a^2 - 2*a*b + b^2 := by ring

theorem mul_sum_diff (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2 := by ring

theorem cube_sum (a b : ℝ) : (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3 := by ring

theorem cube_diff (a b : ℝ) : (a - b)^3 = a^3 - 3*a^2*b + 3*a*b^2 - b^3 := by ring

-- ============================================================
-- 2. 因数分解公式 (数I)
-- ============================================================

theorem factor_diff_sq (a b : ℝ) : a^2 - b^2 = (a + b) * (a - b) := by ring

theorem factor_sum_cubes (a b : ℝ) : a^3 + b^3 = (a + b) * (a^2 - a*b + b^2) := by ring

theorem factor_diff_cubes (a b : ℝ) : a^3 - b^3 = (a - b) * (a^2 + a*b + b^2) := by ring

-- ============================================================
-- 3. 二次不等式 (数I)
--    a > 0 かつ判別式 D ≤ 0 のとき a*x² + b*x + c ≥ 0
-- ============================================================

-- 完全平方式は非負
theorem sq_nonneg_form (a b : ℝ) : (a + b)^2 ≥ 0 := sq_nonneg _

-- 標準形での非負判定: a*(x - p)² + q ≥ q （a ≥ 0 のとき）
theorem vertex_form_nonneg (a p q x : ℝ) (ha : 0 ≤ a) :
    a * (x - p)^2 + q ≥ q := by nlinarith [sq_nonneg (x - p)]

-- 判別式 D < 0 のとき ax²+bx+c > 0 （a > 0 の場合）
-- 4a(ax²+bx+c) = (2ax+b)² + (4ac-b²) として証明
theorem quadratic_pos_of_neg_disc (a b c x : ℝ) (ha : 0 < a) (hd : b ^ 2 - 4 * a * c < 0) :
    a * x^2 + b * x + c > 0 := by nlinarith [sq_nonneg (2*a*x + b)]

-- ============================================================
-- 4. 因数定理 (数II)
--    p(a) = 0 ⟺ (X - a) が p(X) を割り切る
-- ============================================================

theorem factor_theorem (p : ℝ[X]) (a : ℝ) :
    p.eval a = 0 ↔ (X - C a) ∣ p :=
  Polynomial.dvd_iff_isRoot.symm

-- ============================================================
-- 5. 剰余定理 (数II)
--    p(X) を (X - a) で割った余りは p(a)
-- ============================================================

theorem remainder_theorem (p : ℝ[X]) (a : ℝ) :
    p %ₘ (X - C a) = C (p.eval a) :=
  Polynomial.modByMonic_X_sub_C_eq_C_eval p a
