import Mathlib

open Real

namespace AutoProved
-- stmt: theorem sin_sub_formula (x y : ℝ) : sin (x - y) = sin x * cos y - cos x * sin y
-- goal:
--   x y : ℝ
--   ⊢ sin (x - y) = sin x * cos y - cos x * sin y
-- added: 2026-06-10
theorem sin_sub_formula (x y : ℝ) : sin (x - y) = sin x * cos y - cos x * sin y := by
  exact sin_sub x y

end AutoProved

