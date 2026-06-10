import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_norm_neg (x : E) : ‖-x‖ = ‖x‖
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x : E
--   ⊢ ‖-x‖ = ‖x‖
-- added: 2026-06-10
theorem my_norm_neg (x : E) : ‖-x‖ = ‖x‖ := by
  norm_num

end AutoProved

