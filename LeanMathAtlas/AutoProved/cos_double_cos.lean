import Mathlib

open Real

namespace AutoProved
-- stmt: theorem cos_double_cos (x : ℝ) : cos (2 * x) = 2 * cos x ^ 2 - 1
-- goal:
--   x : ℝ
--   ⊢ cos (2 * x) = 2 * cos x ^ 2 - 1
-- added: 2026-06-10
theorem cos_double_cos (x : ℝ) : cos (2 * x) = 2 * cos x ^ 2 - 1 := by
  exact cos_two_mul x

end AutoProved

