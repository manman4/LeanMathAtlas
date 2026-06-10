import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_ftc2 (F f : ℝ → ℝ) (a b : ℝ) (hderiv : ∀ x ∈ Set.uIcc a b, HasDerivAt F (f x) x) (hint : IntervalIntegrable f volume a b) : ∫ x in a..b, f x = F b - F a
-- goal:
--   F f : ℝ → ℝ
--   a b : ℝ
--   hderiv : ∀ x ∈ Set.uIcc a b, HasDerivAt F (f x) x
--   hint : IntervalIntegrable f volume a b
--   ⊢ ∫ (x : ℝ) in a..b, f x = F b - F a
-- added: 2026-06-10
theorem my_ftc2 (F f : ℝ → ℝ) (a b : ℝ) (hderiv : ∀ x ∈ Set.uIcc a b, HasDerivAt F (f x) x) (hint : IntervalIntegrable f volume a b) : ∫ x in a..b, f x = F b - F a := by
  exact intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint

end AutoProved

