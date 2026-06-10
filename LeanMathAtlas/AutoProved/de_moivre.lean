import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem de_moivre (θ : ℝ) (n : ℕ) : (exp (↑θ * I)) ^ n = exp (↑n * ↑θ * I)
-- goal:
--   θ : ℝ
--   n : ℕ
--   ⊢ cexp (↑θ * I) ^ n = cexp (↑n * ↑θ * I)
-- added: 2026-06-10
theorem de_moivre (θ : ℝ) (n : ℕ) : (exp (↑θ * I)) ^ n = exp (↑n * ↑θ * I) := by
  rw [← exp_nat_mul]; congr 1; ring

end AutoProved

