import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem choose_zero (n : ℕ) : n.choose 0 = 1
-- goal:
--   n : ℕ
--   ⊢ n.choose 0 = 1
-- added: 2026-06-10
theorem choose_zero (n : ℕ) : n.choose 0 = 1 := by
  simp

end AutoProved

