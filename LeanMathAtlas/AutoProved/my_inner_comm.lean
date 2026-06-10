import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_inner_comm (x y : E) : inner (𝕜 := ℝ) x y = inner (𝕜 := ℝ) y x
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x y : E
--   ⊢ inner ℝ x y = inner ℝ y x
-- added: 2026-06-10
theorem my_inner_comm (x y : E) : inner (𝕜 := ℝ) x y = inner (𝕜 := ℝ) y x := by
  exact real_inner_comm _ _

end AutoProved

