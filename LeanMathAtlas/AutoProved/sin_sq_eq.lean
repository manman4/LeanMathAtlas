import Mathlib

open Real

namespace AutoProved
-- stmt: theorem sin_sq_eq (x : ℝ) : sin x ^ 2 = 1 - cos x ^ 2
-- goal:
--   x : ℝ
--   ⊢ sin x ^ 2 = 1 - cos x ^ 2
-- added: 2026-06-10
theorem sin_sq_eq (x : ℝ) : sin x ^ 2 = 1 - cos x ^ 2 := by
  exact sin_sq x

end AutoProved

