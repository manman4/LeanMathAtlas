import Mathlib

namespace AutoProved
-- stmt: theorem my_gcd_comm (a b : ℕ) : Nat.gcd a b = Nat.gcd b a
-- goal:
--   a b : ℕ
--   ⊢ a.gcd b = b.gcd a
-- added: 2026-06-10
theorem my_gcd_comm (a b : ℕ) : Nat.gcd a b = Nat.gcd b a := by
  exact Nat.gcd_comm a b

end AutoProved

