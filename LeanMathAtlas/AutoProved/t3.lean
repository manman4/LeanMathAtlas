import Mathlib

namespace AutoProved
-- stmt: theorem t3 (a b : ℤ) : a + b = b + a
-- goal:
--   a b : ℤ
--   ⊢ a + b = b + a
-- added: 2026-06-09
theorem t3 (a b : ℤ) : a + b = b + a := by
  omega

end AutoProved

