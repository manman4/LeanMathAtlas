import Mathlib

namespace AutoProved
-- stmt: theorem my_gcd_zero_right (a : ℕ) : Nat.gcd a 0 = a
-- goal:
--   a : ℕ
--   ⊢ a.gcd 0 = a
-- added: 2026-06-10
theorem my_gcd_zero_right (a : ℕ) : Nat.gcd a 0 = a := by
  simp

end AutoProved

