import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_integral_const (a b c : ℝ) : ∫ _ in a..b, c = (b - a) * c
-- goal:
--   a b c : ℝ
--   ⊢ ∫ (x : ℝ) in a..b, c = (b - a) * c
-- added: 2026-06-10
theorem my_integral_const (a b c : ℝ) : ∫ _ in a..b, c = (b - a) * c := by
  norm_num

end AutoProved

