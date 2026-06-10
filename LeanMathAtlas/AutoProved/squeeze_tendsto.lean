import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem squeeze_tendsto {f g h : ℝ → ℝ} {a L : ℝ} (hg : Tendsto g (𝓝 a) (𝓝 L)) (hh : Tendsto h (𝓝 a) (𝓝 L)) (hfg : ∀ᶠ x in 𝓝 a, g x ≤ f x) (hfh : ∀ᶠ x in 𝓝 a, f x ≤ h x) : Tendsto f (𝓝 a) (𝓝 L)
-- goal:
--   f g h : ℝ → ℝ
--   a L : ℝ
--   hg : Tendsto g (𝓝 a) (𝓝 L)
--   hh : Tendsto h (𝓝 a) (𝓝 L)
--   hfg : ∀ᶠ (x : ℝ) in 𝓝 a, g x ≤ f x
--   hfh : ∀ᶠ (x : ℝ) in 𝓝 a, f x ≤ h x
--   ⊢ Tendsto f (𝓝 a) (𝓝 L)
-- added: 2026-06-10
theorem squeeze_tendsto {f g h : ℝ → ℝ} {a L : ℝ} (hg : Tendsto g (𝓝 a) (𝓝 L)) (hh : Tendsto h (𝓝 a) (𝓝 L)) (hfg : ∀ᶠ x in 𝓝 a, g x ≤ f x) (hfh : ∀ᶠ x in 𝓝 a, f x ≤ h x) : Tendsto f (𝓝 a) (𝓝 L) := by
  exact Tendsto.squeeze' hg hh hfg hfh

end AutoProved

