import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem tendsto_sq (a : ℝ) : Tendsto (fun x => x ^ 2) (𝓝 a) (𝓝 (a ^ 2))
-- goal:
--   a : ℝ
--   ⊢ Tendsto (fun x => x ^ 2) (𝓝 a) (𝓝 (a ^ 2))
-- added: 2026-06-10
theorem tendsto_sq (a : ℝ) : Tendsto (fun x => x ^ 2) (𝓝 a) (𝓝 (a ^ 2)) := by
  exact Tendsto.pow (fun ⦃U⦄ a => a) 2

end AutoProved

