import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_integral_symm (f : ℝ → ℝ) (a b : ℝ) : ∫ x in b..a, f x = -∫ x in a..b, f x
-- goal:
--   f : ℝ → ℝ
--   a b : ℝ
--   ⊢ ∫ (x : ℝ) in b..a, f x = -∫ (x : ℝ) in a..b, f x
-- added: 2026-06-10
theorem my_integral_symm (f : ℝ → ℝ) (a b : ℝ) : ∫ x in b..a, f x = -∫ x in a..b, f x := by
  exact intervalIntegral.integral_symm a b

end AutoProved

