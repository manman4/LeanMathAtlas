import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem cube_sum (a b : ℝ) : (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3
-- goal:
--   a b : ℝ
--   ⊢ (a + b) ^ 3 = a ^ 3 + 3 * a ^ 2 * b + 3 * a * b ^ 2 + b ^ 3
-- added: 2026-06-09
theorem cube_sum (a b : ℝ) : (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3 := by
  ring

end AutoProved

