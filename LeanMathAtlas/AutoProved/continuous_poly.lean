import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem continuous_poly (a : ℝ) : ContinuousAt (fun x => x ^ 2 + 3 * x + 1) a
-- goal:
--   a : ℝ
--   ⊢ ContinuousAt (fun x => x ^ 2 + 3 * x + 1) a
-- added: 2026-06-10
theorem continuous_poly (a : ℝ) : ContinuousAt (fun x => x ^ 2 + 3 * x + 1) a := by
  fun_prop

end AutoProved

