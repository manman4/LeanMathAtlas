import Mathlib

namespace AutoProved
-- stmt: theorem five_prime : Nat.Prime 5
-- goal:
--   ⊢ Nat.Prime 5
-- added: 2026-06-10
theorem five_prime : Nat.Prime 5 := by
  norm_num

end AutoProved

