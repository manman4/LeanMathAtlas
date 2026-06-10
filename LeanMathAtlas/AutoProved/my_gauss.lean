import Mathlib

open BigOperators

namespace AutoProved
-- stmt: theorem my_gauss (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)
-- goal:
--   n : ℕ
--   ⊢ 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)
-- added: 2026-06-10
theorem my_gauss (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1) := by
  induction n with
    | zero => simp
    | succ m ih =>
      rw [Finset.sum_range_succ]; nlinarith [ih]

end AutoProved

