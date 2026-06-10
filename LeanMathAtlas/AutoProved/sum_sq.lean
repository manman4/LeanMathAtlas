import Mathlib

open BigOperators

namespace AutoProved
-- stmt: theorem sum_sq (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1)
-- goal:
--   n : ℕ
--   ⊢ 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1)
-- added: 2026-06-10
theorem sum_sq (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1) := by
  induction n with
    | zero => simp
    | succ m ih =>
      rw [Finset.sum_range_succ]; nlinarith [ih]

end AutoProved

