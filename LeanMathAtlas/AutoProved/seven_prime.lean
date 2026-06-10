import Mathlib

namespace AutoProved
-- stmt: theorem seven_prime : Nat.Prime 7
-- goal:
--   ⊢ Nat.Prime 7
-- added: 2026-06-10
theorem seven_prime : Nat.Prime 7 := by
  norm_num

end AutoProved

