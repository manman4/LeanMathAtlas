import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem euler_formula (x : ℝ) : exp (↑x * I) = cos ↑x + sin ↑x * I
-- goal:
--   x : ℝ
--   ⊢ cexp (↑x * I) = cos ↑x + sin ↑x * I
-- added: 2026-06-10
theorem euler_formula (x : ℝ) : exp (↑x * I) = cos ↑x + sin ↑x * I := by
  exact exp_mul_I ↑x

end AutoProved

