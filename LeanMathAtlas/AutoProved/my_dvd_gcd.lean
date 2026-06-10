import Mathlib

namespace AutoProved
-- stmt: theorem my_dvd_gcd {k a b : ℕ} (ha : k ∣ a) (hb : k ∣ b) : k ∣ Nat.gcd a b
-- goal:
--   k a b : ℕ
--   ha : k ∣ a
--   hb : k ∣ b
--   ⊢ k ∣ a.gcd b
-- added: 2026-06-10
theorem my_dvd_gcd {k a b : ℕ} (ha : k ∣ a) (hb : k ∣ b) : k ∣ Nat.gcd a b := by
  exact Nat.dvd_gcd ha hb

end AutoProved

