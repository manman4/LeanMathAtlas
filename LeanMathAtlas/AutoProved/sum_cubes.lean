import Mathlib

open BigOperators

namespace AutoProved
-- stmt: theorem sum_cubes (n : ℕ) : 4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2
-- goal:
--   n : ℕ
--   ⊢ 4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2
-- added: 2026-06-10
theorem sum_cubes (n : ℕ) : 4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2 := by
  induction n with
    | zero => simp
    | succ m ih =>
      rw [Finset.sum_range_succ]; nlinarith [ih]

end AutoProved

