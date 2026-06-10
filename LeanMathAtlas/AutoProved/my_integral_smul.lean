import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_integral_smul (f : ℝ → ℝ) (c : ℝ) (a b : ℝ) : ∫ x in a..b, c • f x = c • ∫ x in a..b, f x
-- goal:
--   f : ℝ → ℝ
--   c a b : ℝ
--   ⊢ ∫ (x : ℝ) in a..b, c • f x = c • ∫ (x : ℝ) in a..b, f x
-- added: 2026-06-10
theorem my_integral_smul (f : ℝ → ℝ) (c : ℝ) (a b : ℝ) : ∫ x in a..b, c • f x = c • ∫ x in a..b, f x := by
  norm_num

end AutoProved

