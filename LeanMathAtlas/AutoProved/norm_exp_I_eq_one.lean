import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem norm_exp_I_eq_one (x : ℝ) : ‖exp (↑x * I)‖ = 1
-- goal:
--   x : ℝ
--   ⊢ ‖cexp (↑x * I)‖ = 1
-- added: 2026-06-10
theorem norm_exp_I_eq_one (x : ℝ) : ‖exp (↑x * I)‖ = 1 := by
  norm_num

end AutoProved

