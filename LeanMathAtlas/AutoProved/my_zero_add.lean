import Mathlib

namespace AutoProved
-- stmt: theorem my_zero_add (n : Nat) : 0 + n = n
-- goal:
--   n : ℕ
--   ⊢ 0 + n = n
-- added: 2026-06-10
theorem my_zero_add (n : Nat) : 0 + n = n := by
  omega

end AutoProved

