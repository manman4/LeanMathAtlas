import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem alternating_sum_choose (n : ℕ) (hn : 0 < n) : ∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * n.choose k = 0
-- goal:
--   n : ℕ
--   hn : 0 < n
--   ⊢ ∑ k ∈ range (n + 1), (-1) ^ k * ↑(n.choose k) = 0
-- added: 2026-06-10
theorem alternating_sum_choose (n : ℕ) (hn : 0 < n) : ∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * n.choose k = 0 := by
  refine Int.alternating_sum_range_choose_of_ne ?_
    all_goals omega

end AutoProved

