import Mathlib.Tactic
import Mathlib.Analysis.Complex.Trigonometric

open Complex
open scoped ComplexConjugate

/-!
# Complex Numbers

Arithmetic of ℂ, norm/modulus, complex conjugate, Euler's formula,
and de Moivre's theorem.

**Requires**: `ℂ`, `Complex.normSq`, `Complex.exp`
**Tags**: Algebra, Analysis, Complex
-/

-- ============================================================
-- 1. 基本演算
-- ============================================================

-- i の実部・虚部
example : (I : ℂ).re = 0 := I_re
example : (I : ℂ).im = 1 := I_im

-- i² = -1
theorem I_sq : (I : ℂ) ^ 2 = -1 := by
  rw [sq, I_mul_I]

-- ============================================================
-- 2. normSq とノルム
-- ============================================================

-- normSq z = z.re² + z.im²
theorem normSq_sq (z : ℂ) : normSq z = z.re ^ 2 + z.im ^ 2 := by
  simp [normSq_apply, sq]

-- normSq は非負
example (z : ℂ) : 0 ≤ normSq z := normSq_nonneg z

-- ‖z * w‖ = ‖z‖ * ‖w‖（積のノルム）
theorem my_norm_mul (z w : ℂ) : ‖z * w‖ = ‖z‖ * ‖w‖ := norm_mul z w

-- 三角不等式: ‖z + w‖ ≤ ‖z‖ + ‖w‖
theorem my_norm_add_le (z w : ℂ) : ‖z + w‖ ≤ ‖z‖ + ‖w‖ := norm_add_le z w

-- ‖z‖ ≥ 0
example (z : ℂ) : 0 ≤ ‖z‖ := norm_nonneg z

-- ============================================================
-- 3. 共役複素数 (Complex Conjugate)
--    open scoped ComplexConjugate により conj 記法が使える
-- ============================================================

-- conj z の実部・虚部
example (z : ℂ) : (conj z : ℂ).re = z.re  := conj_re z
example (z : ℂ) : (conj z : ℂ).im = -z.im := conj_im z

-- conj(conj z) = z
theorem my_conj_conj (z : ℂ) : conj (conj z : ℂ) = z := star_star z

-- conj(z + w) = conj z + conj w（加法準同型）
theorem my_conj_add (z w : ℂ) : conj (z + w : ℂ) = conj z + conj w :=
  (starRingEnd ℂ).map_add z w

-- conj(z * w) = conj z * conj w（乗法準同型）
theorem my_conj_mul (z w : ℂ) : conj (z * w : ℂ) = conj z * conj w :=
  (starRingEnd ℂ).map_mul z w

-- z * conj z = ‖z‖²
-- Complex.mul_conj' : z * conj z = ‖z‖ ^ 2
theorem my_mul_conj (z : ℂ) : z * conj z = ‖z‖ ^ 2 := mul_conj' z

-- ============================================================
-- 4. オイラーの公式
--    exp(x * i) = cos x + i * sin x  （x : ℝ）
-- ============================================================

-- Complex.exp_mul_I : exp (x * I) = cos x + sin x * I
theorem euler_formula (x : ℝ) :
    exp (↑x * I) = cos ↑x + sin ↑x * I :=
  exp_mul_I (↑x : ℂ)

-- |exp(i * x)| = 1（単位円上に乗る）
-- Complex.norm_exp_ofReal_mul_I : ‖exp (x * I)‖ = 1
theorem norm_exp_I_eq_one (x : ℝ) : ‖exp (↑x * I)‖ = 1 :=
  norm_exp_ofReal_mul_I x

-- ============================================================
-- 5. ド・モアブルの定理
--    (exp(i*θ))^n = exp(i * n * θ)
-- ============================================================

-- Complex.exp_nat_mul : exp (↑n * z) = exp z ^ n
theorem de_moivre (θ : ℝ) (n : ℕ) :
    (exp (↑θ * I)) ^ n = exp (↑n * ↑θ * I) := by
  rw [← exp_nat_mul]
  congr 1
  ring
