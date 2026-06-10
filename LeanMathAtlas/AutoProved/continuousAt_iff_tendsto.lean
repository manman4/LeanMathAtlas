import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem continuousAt_iff_tendsto (f : ℝ → ℝ) (a : ℝ) : ContinuousAt f a ↔ Tendsto f (𝓝 a) (𝓝 (f a))
-- goal:
--   f : ℝ → ℝ
--   a : ℝ
--   ⊢ ContinuousAt f a ↔ Tendsto f (𝓝 a) (𝓝 (f a))
-- added: 2026-06-10
theorem continuousAt_iff_tendsto (f : ℝ → ℝ) (a : ℝ) : ContinuousAt f a ↔ Tendsto f (𝓝 a) (𝓝 (f a)) := by
  aesop

end AutoProved

