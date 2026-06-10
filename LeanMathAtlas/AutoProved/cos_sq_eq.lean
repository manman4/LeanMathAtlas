import Mathlib

open Real

namespace AutoProved
-- stmt: theorem cos_sq_eq (x : ℝ) : cos x ^ 2 = 1 - sin x ^ 2
-- goal:
--   x : ℝ
--   ⊢ cos x ^ 2 = 1 - sin x ^ 2
-- added: 2026-06-10
theorem cos_sq_eq (x : ℝ) : cos x ^ 2 = 1 - sin x ^ 2 := by
  exact cos_sq' x

end AutoProved

