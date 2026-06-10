import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_inner_self_eq_zero (x : E) : inner (𝕜 := ℝ) x x = 0 ↔ x = 0
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x : E
--   ⊢ inner ℝ x x = 0 ↔ x = 0
-- added: 2026-06-10
theorem my_inner_self_eq_zero (x : E) : inner (𝕜 := ℝ) x x = 0 ↔ x = 0 := by
  exact inner_self_eq_zero

end AutoProved

