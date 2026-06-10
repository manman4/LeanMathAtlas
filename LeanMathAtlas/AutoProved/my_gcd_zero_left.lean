import Mathlib

namespace AutoProved
-- stmt: theorem my_gcd_zero_left (a : ℕ) : Nat.gcd 0 a = a
-- goal:
--   a : ℕ
--   ⊢ Nat.gcd 0 a = a
-- added: 2026-06-10
theorem my_gcd_zero_left (a : ℕ) : Nat.gcd 0 a = a := by
  simp

end AutoProved

