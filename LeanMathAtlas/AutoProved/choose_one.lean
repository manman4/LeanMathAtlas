import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem choose_one (n : ℕ) : n.choose 1 = n
-- goal:
--   n : ℕ
--   ⊢ n.choose 1 = n
-- added: 2026-06-10
theorem choose_one (n : ℕ) : n.choose 1 = n := by
  simp

end AutoProved

