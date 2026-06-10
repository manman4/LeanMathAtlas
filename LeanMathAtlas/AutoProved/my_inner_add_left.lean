import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_inner_add_left (x y z : E) : inner (𝕜 := ℝ) (x + y) z = inner (𝕜 := ℝ) x z + inner (𝕜 := ℝ) y z
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x y z : E
--   ⊢ inner ℝ (x + y) z = inner ℝ x z + inner ℝ y z
-- added: 2026-06-10
theorem my_inner_add_left (x y z : E) : inner (𝕜 := ℝ) (x + y) z = inner (𝕜 := ℝ) x z + inner (𝕜 := ℝ) y z := by
  exact inner_add_left _ _ _

end AutoProved

