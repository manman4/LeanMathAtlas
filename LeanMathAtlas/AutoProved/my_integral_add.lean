import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_integral_add (f g : ℝ → ℝ) (a b : ℝ) (hf : IntervalIntegrable f volume a b) (hg : IntervalIntegrable g volume a b) : ∫ x in a..b, (f x + g x) = (∫ x in a..b, f x) + ∫ x in a..b, g x
-- goal:
--   f g : ℝ → ℝ
--   a b : ℝ
--   hf : IntervalIntegrable f volume a b
--   hg : IntervalIntegrable g volume a b
--   ⊢ ∫ (x : ℝ) in a..b, f x + g x = (∫ (x : ℝ) in a..b, f x) + ∫ (x : ℝ) in a..b, g x
-- added: 2026-06-10
theorem my_integral_add (f g : ℝ → ℝ) (a b : ℝ) (hf : IntervalIntegrable f volume a b) (hg : IntervalIntegrable g volume a b) : ∫ x in a..b, (f x + g x) = (∫ x in a..b, f x) + ∫ x in a..b, g x := by
  exact intervalIntegral.integral_add hf hg

end AutoProved

