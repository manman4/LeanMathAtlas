import Mathlib

namespace AutoProved
-- stmt: theorem prime_ge_two (p : ℕ) (hp : Nat.Prime p) : 2 ≤ p
-- goal:
--   p : ℕ
--   hp : Nat.Prime p
--   ⊢ 2 ≤ p
-- added: 2026-06-10
theorem prime_ge_two (p : ℕ) (hp : Nat.Prime p) : 2 ≤ p := by
  exact Nat.Prime.two_le hp

end AutoProved

