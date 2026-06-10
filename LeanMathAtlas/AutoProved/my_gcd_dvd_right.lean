import Mathlib

namespace AutoProved
-- stmt: theorem my_gcd_dvd_right (a b : ℕ) : Nat.gcd a b ∣ b
-- goal:
--   a b : ℕ
--   ⊢ a.gcd b ∣ b
-- added: 2026-06-10
theorem my_gcd_dvd_right (a b : ℕ) : Nat.gcd a b ∣ b := by
  exact Nat.gcd_dvd_right a b

end AutoProved

