import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem pascal (n k : ℕ) : n.choose k + n.choose (k + 1) = (n + 1).choose (k + 1)
-- goal:
--   n k : ℕ
--   ⊢ n.choose k + n.choose (k + 1) = (n + 1).choose (k + 1)
-- added: 2026-06-10
theorem pascal (n k : ℕ) : n.choose k + n.choose (k + 1) = (n + 1).choose (k + 1) := by
  rfl

end AutoProved

