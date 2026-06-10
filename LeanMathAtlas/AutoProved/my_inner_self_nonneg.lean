import Mathlib

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
set_option linter.unusedSectionVars false

namespace AutoProved
-- stmt: theorem my_inner_self_nonneg (x : E) : 0 ≤ inner (𝕜 := ℝ) x x
-- goal:
--   E : Type u_1
--   inst✝¹ : NormedAddCommGroup E
--   inst✝ : InnerProductSpace ℝ E
--   x : E
--   ⊢ 0 ≤ inner ℝ x x
-- added: 2026-06-10
theorem my_inner_self_nonneg (x : E) : 0 ≤ inner (𝕜 := ℝ) x x := by
  exact real_inner_self_nonneg

end AutoProved

