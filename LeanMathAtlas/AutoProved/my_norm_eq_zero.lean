import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_norm_eq_zero (x : E) : ‖x‖ = 0 ↔ x = 0
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x : E
--   ⊢ ‖x‖ = 0 ↔ x = 0
-- added: 2026-06-10
theorem my_norm_eq_zero (x : E) : ‖x‖ = 0 ↔ x = 0 := by
  norm_num

end AutoProved

