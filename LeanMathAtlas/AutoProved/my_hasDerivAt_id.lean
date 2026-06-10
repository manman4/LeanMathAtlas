import Mathlib

open Real

namespace AutoProved
-- stmt: theorem my_hasDerivAt_id (a : ℝ) : HasDerivAt id 1 a
-- goal:
--   a : ℝ
--   ⊢ HasDerivAt id 1 a
-- added: 2026-06-10
theorem my_hasDerivAt_id (a : ℝ) : HasDerivAt id 1 a := by
  exact hasDerivAt_id _

end AutoProved

