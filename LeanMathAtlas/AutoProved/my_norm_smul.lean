import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_norm_smul (c : ℝ) (x : E) : ‖c • x‖ = |c| * ‖x‖
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   c : ℝ
--   x : E
--   ⊢ ‖c • x‖ = |c| * ‖x‖
-- added: 2026-06-10
theorem my_norm_smul (c : ℝ) (x : E) : ‖c • x‖ = |c| * ‖x‖ := by
  exact norm_smul _ _

end AutoProved

