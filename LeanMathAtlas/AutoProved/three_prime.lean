import Mathlib

namespace AutoProved
-- stmt: theorem three_prime : Nat.Prime 3
-- goal:
--   ⊢ Nat.Prime 3
-- added: 2026-06-10
theorem three_prime : Nat.Prime 3 := by
  norm_num

end AutoProved

