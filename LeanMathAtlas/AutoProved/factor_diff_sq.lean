import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem factor_diff_sq (a b : ℝ) : a^2 - b^2 = (a + b) * (a - b)
-- goal:
--   a b : ℝ
--   ⊢ a ^ 2 - b ^ 2 = (a + b) * (a - b)
-- added: 2026-06-09
theorem factor_diff_sq (a b : ℝ) : a^2 - b^2 = (a + b) * (a - b) := by
  ring

end AutoProved

