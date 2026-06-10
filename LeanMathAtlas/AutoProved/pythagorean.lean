import Mathlib

open Real

namespace AutoProved
-- stmt: theorem pythagorean (x : ℝ) : sin x ^ 2 + cos x ^ 2 = 1
-- goal:
--   x : ℝ
--   ⊢ sin x ^ 2 + cos x ^ 2 = 1
-- added: 2026-06-10
theorem pythagorean (x : ℝ) : sin x ^ 2 + cos x ^ 2 = 1 := by
  simp [cos_two_mul, sin_sq_add_cos_sq]

end AutoProved

