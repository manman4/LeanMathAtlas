import Mathlib

namespace AutoProved
-- stmt: theorem double_eq_two_mul (n : Nat) : n + n = 2 * n
-- goal:
--   n : ℕ
--   ⊢ n + n = 2 * n
-- added: 2026-06-10
theorem double_eq_two_mul (n : Nat) : n + n = 2 * n := by
  omega

end AutoProved

