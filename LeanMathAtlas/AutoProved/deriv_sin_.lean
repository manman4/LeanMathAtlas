import Mathlib

open Real

namespace AutoProved
-- stmt: theorem deriv_sin' (a : ℝ) : HasDerivAt Real.sin (Real.cos a) a
-- goal:
--   a : ℝ
--   ⊢ HasDerivAt sin (cos a) a
-- added: 2026-06-10
theorem deriv_sin' (a : ℝ) : HasDerivAt Real.sin (Real.cos a) a := by
  exact hasDerivAt_sin a

end AutoProved

