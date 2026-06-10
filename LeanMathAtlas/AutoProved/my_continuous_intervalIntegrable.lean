import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_continuous_intervalIntegrable (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) : IntervalIntegrable f volume a b
-- goal:
--   f : ℝ → ℝ
--   hf : Continuous f
--   a b : ℝ
--   ⊢ IntervalIntegrable f volume a b
-- added: 2026-06-10
theorem my_continuous_intervalIntegrable (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) : IntervalIntegrable f volume a b := by
  exact Continuous.intervalIntegrable hf a b

end AutoProved

