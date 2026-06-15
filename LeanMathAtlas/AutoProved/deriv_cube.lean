import Mathlib

open Real

namespace AutoProved
-- stmt: theorem deriv_cube (a : ℝ) : HasDerivAt (fun x => x ^ 3) (3 * a ^ 2) a
-- goal:
--   a : ℝ
--   ⊢ HasDerivAt (fun x => x ^ 3) (3 * a ^ 2) a
-- added: 2026-06-15
theorem deriv_cube (a : ℝ) : HasDerivAt (fun x => x ^ 3) (3 * a ^ 2) a := by
  simpa using hasDerivAt_pow 3 a

end AutoProved
