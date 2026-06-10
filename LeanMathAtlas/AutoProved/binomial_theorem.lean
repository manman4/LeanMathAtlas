import Mathlib

open BigOperators Finset

namespace AutoProved
-- stmt: theorem binomial_theorem (a b : ℝ) (n : ℕ) : (a + b) ^ n = ∑ k ∈ range (n + 1), a ^ k * b ^ (n - k) * (n.choose k : ℝ)
-- goal:
--   a b : ℝ
--   n : ℕ
--   ⊢ (a + b) ^ n = ∑ k ∈ range (n + 1), a ^ k * b ^ (n - k) * ↑(n.choose k)
-- added: 2026-06-10
theorem binomial_theorem (a b : ℝ) (n : ℕ) : (a + b) ^ n = ∑ k ∈ range (n + 1), a ^ k * b ^ (n - k) * (n.choose k : ℝ) := by
  exact add_pow a b n

end AutoProved

