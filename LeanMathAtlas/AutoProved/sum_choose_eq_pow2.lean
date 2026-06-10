import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem sum_choose_eq_pow2 (n : ℕ) : ∑ k ∈ range (n + 1), n.choose k = 2 ^ n
-- goal:
--   n : ℕ
--   ⊢ ∑ k ∈ range (n + 1), n.choose k = 2 ^ n
-- added: 2026-06-10
theorem sum_choose_eq_pow2 (n : ℕ) : ∑ k ∈ range (n + 1), n.choose k = 2 ^ n := by
  exact Nat.sum_range_choose n

end AutoProved

