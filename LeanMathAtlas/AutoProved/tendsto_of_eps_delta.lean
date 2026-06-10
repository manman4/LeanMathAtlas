import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem tendsto_of_eps_delta {f : ℝ → ℝ} {a b : ℝ} (h : ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε) : Tendsto f (𝓝 a) (𝓝 b)
-- goal:
--   f : ℝ → ℝ
--   a b : ℝ
--   h : ∀ ε > 0, ∃ δ > 0, ∀ (x : ℝ), |x - a| < δ → |f x - b| < ε
--   ⊢ Tendsto f (𝓝 a) (𝓝 b)
-- added: 2026-06-10
theorem tendsto_of_eps_delta {f : ℝ → ℝ} {a b : ℝ} (h : ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε) : Tendsto f (𝓝 a) (𝓝 b) := by
  exact Metric.tendsto_nhds_nhds.mpr h

end AutoProved

