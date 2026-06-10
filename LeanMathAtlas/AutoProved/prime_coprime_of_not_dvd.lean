import Mathlib

namespace AutoProved
-- stmt: theorem prime_coprime_of_not_dvd {p n : ℕ} (hp : Nat.Prime p) (h : ¬ p ∣ n) : Nat.Coprime p n
-- goal:
--   p n : ℕ
--   hp : Nat.Prime p
--   h : ¬p ∣ n
--   ⊢ p.Coprime n
-- added: 2026-06-10
theorem prime_coprime_of_not_dvd {p n : ℕ} (hp : Nat.Prime p) (h : ¬ p ∣ n) : Nat.Coprime p n := by
  exact (Nat.Prime.coprime_iff_not_dvd hp).mpr h

end AutoProved

