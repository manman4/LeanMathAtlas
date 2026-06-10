import Mathlib

open Real

namespace AutoProved
-- stmt: theorem cos_double (x : ℝ) : cos (2 * x) = cos x ^ 2 - sin x ^ 2
-- goal:
--   x : ℝ
--   ⊢ cos (2 * x) = cos x ^ 2 - sin x ^ 2
-- added: 2026-06-10
theorem cos_double (x : ℝ) : cos (2 * x) = cos x ^ 2 - sin x ^ 2 := by
  exact cos_two_mul' x

end AutoProved

