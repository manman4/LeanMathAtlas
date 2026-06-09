import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem factor_sum_cubes (a b : ℝ) : a^3 + b^3 = (a + b) * (a^2 - a*b + b^2)
-- goal:
--   a b : ℝ
--   ⊢ a ^ 3 + b ^ 3 = (a + b) * (a ^ 2 - a * b + b ^ 2)
-- added: 2026-06-09
theorem factor_sum_cubes (a b : ℝ) : a^3 + b^3 = (a + b) * (a^2 - a*b + b^2) := by
  ring

end AutoProved

