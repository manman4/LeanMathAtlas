import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem tendsto_iff_eps_delta (f : ℝ → ℝ) (a b : ℝ) : Tendsto f (𝓝 a) (𝓝 b) ↔ ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε
-- goal:
--   f : ℝ → ℝ
--   a b : ℝ
--   ⊢ Tendsto f (𝓝 a) (𝓝 b) ↔ ∀ ε > 0, ∃ δ > 0, ∀ (x : ℝ), |x - a| < δ → |f x - b| < ε
-- added: 2026-06-10
theorem tendsto_iff_eps_delta (f : ℝ → ℝ) (a b : ℝ) : Tendsto f (𝓝 a) (𝓝 b) ↔ ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε := by
  exact Metric.tendsto_nhds_nhds

end AutoProved

