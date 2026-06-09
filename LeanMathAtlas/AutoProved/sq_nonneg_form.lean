import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem sq_nonneg_form (a b : ℝ) : (a + b)^2 ≥ 0
-- goal:
--   a b : ℝ
--   ⊢ (a + b) ^ 2 ≥ 0
-- added: 2026-06-09
theorem sq_nonneg_form (a b : ℝ) : (a + b)^2 ≥ 0 := by
  nlinarith [sq_nonneg (a - b)]

end AutoProved

