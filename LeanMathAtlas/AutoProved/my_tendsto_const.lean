import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem my_tendsto_const (a c : ℝ) : Tendsto (fun _ => c) (𝓝 a) (𝓝 c)
-- goal:
--   a c : ℝ
--   ⊢ Tendsto (fun x => c) (𝓝 a) (𝓝 c)
-- added: 2026-06-10
theorem my_tendsto_const (a c : ℝ) : Tendsto (fun _ => c) (𝓝 a) (𝓝 c) := by
  norm_num

end AutoProved

