import Mathlib

open MeasureTheory

namespace AutoProved
-- stmt: theorem my_ftc1 (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) : deriv (fun u => ∫ x in a..u, f x) b = f b
-- goal:
--   f : ℝ → ℝ
--   hf : Continuous f
--   a b : ℝ
--   ⊢ deriv (fun u => ∫ (x : ℝ) in a..u, f x) b = f b
-- added: 2026-06-10
theorem my_ftc1 (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) : deriv (fun u => ∫ x in a..u, f x) b = f b := by
  exact Continuous.deriv_integral f hf a b

end AutoProved

