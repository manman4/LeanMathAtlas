import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem sq_diff (a b : ℝ) : (a - b)^2 = a^2 - 2*a*b + b^2
-- goal:
--   a b : ℝ
--   ⊢ (a - b) ^ 2 = a ^ 2 - 2 * a * b + b ^ 2
-- added: 2026-06-09
theorem sq_diff (a b : ℝ) : (a - b)^2 = a^2 - 2*a*b + b^2 := by
  ring

end AutoProved

