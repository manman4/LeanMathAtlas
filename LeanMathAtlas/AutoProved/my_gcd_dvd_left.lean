import Mathlib

namespace AutoProved
-- stmt: theorem my_gcd_dvd_left (a b : ℕ) : Nat.gcd a b ∣ a
-- goal:
--   a b : ℕ
--   ⊢ a.gcd b ∣ a
-- added: 2026-06-10
theorem my_gcd_dvd_left (a b : ℕ) : Nat.gcd a b ∣ a := by
  exact Nat.gcd_dvd_left a b

end AutoProved

