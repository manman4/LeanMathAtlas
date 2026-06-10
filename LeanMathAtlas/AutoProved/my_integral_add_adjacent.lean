import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_integral_add_adjacent (f : ℝ → ℝ) (a b c : ℝ) (hab : IntervalIntegrable f volume a b) (hbc : IntervalIntegrable f volume b c) : (∫ x in a..b, f x) + ∫ x in b..c, f x = ∫ x in a..c, f x
-- goal:
--   f : ℝ → ℝ
--   a b c : ℝ
--   hab : IntervalIntegrable f volume a b
--   hbc : IntervalIntegrable f volume b c
--   ⊢ (∫ (x : ℝ) in a..b, f x) + ∫ (x : ℝ) in b..c, f x = ∫ (x : ℝ) in a..c, f x
-- added: 2026-06-10
theorem my_integral_add_adjacent (f : ℝ → ℝ) (a b c : ℝ) (hab : IntervalIntegrable f volume a b) (hbc : IntervalIntegrable f volume b c) : (∫ x in a..b, f x) + ∫ x in b..c, f x = ∫ x in a..c, f x := by
  exact intervalIntegral.integral_add_adjacent_intervals hab hbc

end AutoProved

