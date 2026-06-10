import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem my_tendsto_id (a : ℝ) : Tendsto id (𝓝 a) (𝓝 a)
-- goal:
--   a : ℝ
--   ⊢ Tendsto id (𝓝 a) (𝓝 a)
-- added: 2026-06-10
theorem my_tendsto_id (a : ℝ) : Tendsto id (𝓝 a) (𝓝 a) := by
  exact tendsto_ofReal_iff'.mp fun ⦃U⦄ a => a

end AutoProved

