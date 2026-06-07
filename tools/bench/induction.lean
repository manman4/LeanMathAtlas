import Mathlib
open BigOperators

theorem bench_sum_gauss (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1) := by sorry
theorem bench_sum_sq (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1) := by sorry
theorem bench_sum_cube (n : ℕ) : 4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2 := by sorry
theorem bench_geom_sum (n : ℕ) : ∑ k ∈ Finset.range (n + 1), 2 ^ k + 1 = 2 ^ (n + 1) := by sorry
theorem bench_sum_odd (n : ℕ) : ∑ k ∈ Finset.range n, (2 * k + 1) = n ^ 2 := by sorry
