import Mathlib

namespace AutoProved
-- stmt: theorem coprime_dvd_of_dvd_mul {k m n : ℕ} (hco : Nat.Coprime k n) (h : k ∣ m * n) : k ∣ m
-- goal:
--   k m n : ℕ
--   hco : k.Coprime n
--   h : k ∣ m * n
--   ⊢ k ∣ m
-- added: 2026-06-10
theorem coprime_dvd_of_dvd_mul {k m n : ℕ} (hco : Nat.Coprime k n) (h : k ∣ m * n) : k ∣ m := by
  exact Nat.Coprime.dvd_of_dvd_mul_right hco h

end AutoProved

