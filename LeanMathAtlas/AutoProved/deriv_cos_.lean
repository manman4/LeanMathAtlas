import Mathlib

open Real

namespace AutoProved
-- stmt: theorem deriv_cos' (a : ℝ) : HasDerivAt Real.cos (-Real.sin a) a
-- goal:
--   a : ℝ
--   ⊢ HasDerivAt cos (-sin a) a
-- added: 2026-06-10
theorem deriv_cos' (a : ℝ) : HasDerivAt Real.cos (-Real.sin a) a := by
  exact hasDerivAt_cos a

end AutoProved

