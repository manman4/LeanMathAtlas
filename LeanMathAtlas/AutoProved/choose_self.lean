import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem choose_self (n : ℕ) : n.choose n = 1
-- goal:
--   n : ℕ
--   ⊢ n.choose n = 1
-- added: 2026-06-10
theorem choose_self (n : ℕ) : n.choose n = 1 := by
  simp

end AutoProved

