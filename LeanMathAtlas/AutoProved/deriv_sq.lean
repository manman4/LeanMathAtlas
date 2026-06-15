import Mathlib

open Real

namespace AutoProved
-- stmt: theorem deriv_sq (a : ℝ) : HasDerivAt (fun x => x ^ 2) (2 * a) a
-- goal:
--   a : ℝ
--   ⊢ HasDerivAt (fun x => x ^ 2) (2 * a) a
-- added: 2026-06-15
theorem deriv_sq (a : ℝ) : HasDerivAt (fun x => x ^ 2) (2 * a) a := by
  simpa using hasDerivAt_pow 2 a

end AutoProved
