import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem choose_symm (n k : ℕ) (h : k ≤ n) : n.choose k = n.choose (n - k)
-- goal:
--   n k : ℕ
--   h : k ≤ n
--   ⊢ n.choose k = n.choose (n - k)
-- added: 2026-06-10
theorem choose_symm (n k : ℕ) (h : k ≤ n) : n.choose k = n.choose (n - k) := by
  exact Eq.symm (Nat.choose_symm h)

end AutoProved

