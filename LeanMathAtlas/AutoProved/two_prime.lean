import Mathlib

namespace AutoProved
-- stmt: theorem two_prime : Nat.Prime 2
-- goal:
--   ⊢ Nat.Prime 2
-- added: 2026-06-10
theorem two_prime : Nat.Prime 2 := by
  norm_num

end AutoProved

