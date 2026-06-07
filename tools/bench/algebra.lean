import Mathlib

theorem bench_sq_sum (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by sorry
theorem bench_sq_diff (a b : ℝ) : (a - b)^2 = a^2 - 2*a*b + b^2 := by sorry
theorem bench_diff_sq (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2 := by sorry
theorem bench_cube_sum (a b : ℝ) : (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3 := by sorry
theorem bench_nat_comm (a b : ℕ) : a + b = b + a := by sorry
theorem bench_nat_assoc (a b c : ℕ) : (a + b) + c = a + (b + c) := by sorry
theorem bench_nat_le (n : ℕ) : n ≤ n + 1 := by sorry
theorem bench_int_linarith (a b : ℤ) (h1 : a ≤ b) (h2 : b ≤ a) : a = b := by sorry
theorem bench_cube_diff (a b : ℝ) : (a - b)^3 = a^3 - 3*a^2*b + 3*a*b^2 - b^3 := by sorry
theorem bench_am_gm (a b : ℝ) : 2 * a * b ≤ a^2 + b^2 := by sorry
theorem bench_sq_nonneg (a : ℝ) : 0 ≤ a^2 := by sorry
theorem bench_mul_comm_real (a b : ℝ) : a * b = b * a := by sorry
-- polynomial inequalities (nlinarith with pairwise sq witnesses)
theorem bench_cauchy2d (a b c d : ℝ) : (a ^ 2 + b ^ 2) * (c ^ 2 + d ^ 2) ≥ (a * c + b * d) ^ 2 := by sorry
theorem bench_sym3 (a b c : ℝ) : a ^ 2 + b ^ 2 + c ^ 2 ≥ a * b + b * c + a * c := by sorry
theorem bench_cube_am_gm (a b c : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) : a ^ 3 + b ^ 3 + c ^ 3 ≥ 3 * a * b * c := by sorry
theorem bench_cs_sum (a b c : ℝ) : (a + b + c) ^ 2 ≤ 3 * (a ^ 2 + b ^ 2 + c ^ 2) := by sorry
