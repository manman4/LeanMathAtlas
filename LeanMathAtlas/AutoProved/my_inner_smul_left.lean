import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_inner_smul_left (c : ℝ) (x y : E) : inner (𝕜 := ℝ) (c • x) y = c * inner (𝕜 := ℝ) x y
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   c : ℝ
--   x y : E
--   ⊢ inner ℝ (c • x) y = c * inner ℝ x y
-- added: 2026-06-10
theorem my_inner_smul_left (c : ℝ) (x y : E) : inner (𝕜 := ℝ) (c • x) y = c * inner (𝕜 := ℝ) x y := by
  exact inner_smul_left _ _ _

end AutoProved

