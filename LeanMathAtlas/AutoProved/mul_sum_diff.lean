import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem mul_sum_diff (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2
-- goal:
--   a b : ℝ
--   ⊢ (a + b) * (a - b) = a ^ 2 - b ^ 2
-- added: 2026-06-09
theorem mul_sum_diff (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2 := by
  ring

end AutoProved

