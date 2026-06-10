import Mathlib

open BigOperators

namespace AutoProved
-- stmt: theorem sum_geom (a r : ℝ) (n : ℕ) : (r - 1) * ∑ k ∈ Finset.range n, a * r ^ k = a * (r ^ n - 1)
-- goal:
--   a r : ℝ
--   n : ℕ
--   ⊢ (r - 1) * ∑ k ∈ Finset.range n, a * r ^ k = a * (r ^ n - 1)
-- added: 2026-06-10
theorem sum_geom (a r : ℝ) (n : ℕ) : (r - 1) * ∑ k ∈ Finset.range n, a * r ^ k = a * (r ^ n - 1) := by
  induction n with
    | zero => simp
    | succ m ih =>
      rw [Finset.sum_range_succ, mul_add, ih]; ring

end AutoProved

