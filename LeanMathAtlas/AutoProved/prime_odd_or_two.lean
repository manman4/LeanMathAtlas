import Mathlib

namespace AutoProved
-- stmt: theorem prime_odd_or_two (p : ℕ) (hp : Nat.Prime p) (hne : p ≠ 2) : p % 2 = 1
-- goal:
--   p : ℕ
--   hp : Nat.Prime p
--   hne : p ≠ 2
--   ⊢ p % 2 = 1
-- added: 2026-06-10
theorem prime_odd_or_two (p : ℕ) (hp : Nat.Prime p) (hne : p ≠ 2) : p % 2 = 1 := by
  exact (Nat.Prime.mod_two_eq_one_iff_ne_two hp).mpr hne

end AutoProved

