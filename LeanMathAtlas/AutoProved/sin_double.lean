import Mathlib

open Real

namespace AutoProved
-- stmt: theorem sin_double (x : ℝ) : sin (2 * x) = 2 * sin x * cos x
-- goal:
--   x : ℝ
--   ⊢ sin (2 * x) = 2 * sin x * cos x
-- added: 2026-06-10
theorem sin_double (x : ℝ) : sin (2 * x) = 2 * sin x * cos x := by
  exact sin_two_mul x

end AutoProved

