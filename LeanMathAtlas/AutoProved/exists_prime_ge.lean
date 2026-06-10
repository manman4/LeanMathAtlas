import Mathlib

namespace AutoProved
-- stmt: theorem exists_prime_ge (n : ℕ) : ∃ p, n ≤ p ∧ Nat.Prime p
-- goal:
--   n : ℕ
--   ⊢ ∃ p, n ≤ p ∧ Nat.Prime p
-- added: 2026-06-10
theorem exists_prime_ge (n : ℕ) : ∃ p, n ≤ p ∧ Nat.Prime p := by
  exact Nat.exists_infinite_primes n

end AutoProved

