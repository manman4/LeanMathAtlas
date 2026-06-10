import Mathlib

namespace AutoProved
-- stmt: theorem prime_divisors (p : ℕ) (hp : Nat.Prime p) (k : ℕ) (hk : k ∣ p) : k = 1 ∨ k = p
-- goal:
--   p : ℕ
--   hp : Nat.Prime p
--   k : ℕ
--   hk : k ∣ p
--   ⊢ k = 1 ∨ k = p
-- added: 2026-06-10
theorem prime_divisors (p : ℕ) (hp : Nat.Prime p) (k : ℕ) (hk : k ∣ p) : k = 1 ∨ k = p := by
  exact (Nat.dvd_prime hp).mp hk

end AutoProved

