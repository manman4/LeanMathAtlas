import Mathlib

namespace AutoProved
-- stmt: theorem coprime_succ (n : ℕ) : Nat.Coprime n (n + 1)
-- goal:
--   n : ℕ
--   ⊢ n.Coprime (n + 1)
-- added: 2026-06-10
theorem coprime_succ (n : ℕ) : Nat.Coprime n (n + 1) := by
  simp

end AutoProved

