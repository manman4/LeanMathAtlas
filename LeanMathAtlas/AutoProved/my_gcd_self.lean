import Mathlib

namespace AutoProved
-- stmt: theorem my_gcd_self (a : ℕ) : Nat.gcd a a = a
-- goal:
--   a : ℕ
--   ⊢ a.gcd a = a
-- added: 2026-06-10
theorem my_gcd_self (a : ℕ) : Nat.gcd a a = a := by
  simp

end AutoProved

