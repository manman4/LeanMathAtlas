import Mathlib

open Real

namespace AutoProved
-- stmt: theorem cos_sub_formula (x y : ℝ) : cos (x - y) = cos x * cos y + sin x * sin y
-- goal:
--   x y : ℝ
--   ⊢ cos (x - y) = cos x * cos y + sin x * sin y
-- added: 2026-06-10
theorem cos_sub_formula (x y : ℝ) : cos (x - y) = cos x * cos y + sin x * sin y := by
  exact cos_sub x y

end AutoProved

