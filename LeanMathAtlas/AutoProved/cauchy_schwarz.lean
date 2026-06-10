import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem cauchy_schwarz (x y : E) : |inner (𝕜 := ℝ) x y| ≤ ‖x‖ * ‖y‖
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x y : E
--   ⊢ |inner ℝ x y| ≤ ‖x‖ * ‖y‖
-- added: 2026-06-10
theorem cauchy_schwarz (x y : E) : |inner (𝕜 := ℝ) x y| ≤ ‖x‖ * ‖y‖ := by
  exact abs_real_inner_le_norm x y

end AutoProved

