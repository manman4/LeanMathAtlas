import Mathlib

namespace AutoProved
-- stmt: theorem my_zero_le (n : Nat) : 0 ≤ n
-- goal:
--   n : ℕ
--   ⊢ 0 ≤ n
-- added: 2026-06-10
theorem my_zero_le (n : Nat) : 0 ≤ n := by
  omega

end AutoProved

