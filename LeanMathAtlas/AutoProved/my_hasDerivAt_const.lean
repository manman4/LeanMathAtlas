import Mathlib

open Real

namespace AutoProved
-- stmt: theorem my_hasDerivAt_const (a c : ℝ) : HasDerivAt (fun _ => c) 0 a
-- goal:
--   a c : ℝ
--   ⊢ HasDerivAt (fun x => c) 0 a
-- added: 2026-06-10
theorem my_hasDerivAt_const (a c : ℝ) : HasDerivAt (fun _ => c) 0 a := by
  exact hasDerivAt_const _ _

end AutoProved

