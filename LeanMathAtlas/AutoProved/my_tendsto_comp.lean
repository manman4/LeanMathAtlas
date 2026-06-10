import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem my_tendsto_comp {f g : ℝ → ℝ} {a b c : ℝ} (hg : Tendsto g (𝓝 b) (𝓝 c)) (hf : Tendsto f (𝓝 a) (𝓝 b)) : Tendsto (g ∘ f) (𝓝 a) (𝓝 c)
-- goal:
--   f g : ℝ → ℝ
--   a b c : ℝ
--   hg : Tendsto g (𝓝 b) (𝓝 c)
--   hf : Tendsto f (𝓝 a) (𝓝 b)
--   ⊢ Tendsto (g ∘ f) (𝓝 a) (𝓝 c)
-- added: 2026-06-10
theorem my_tendsto_comp {f g : ℝ → ℝ} {a b c : ℝ} (hg : Tendsto g (𝓝 b) (𝓝 c)) (hf : Tendsto f (𝓝 a) (𝓝 b)) : Tendsto (g ∘ f) (𝓝 a) (𝓝 c) := by
  exact Tendsto.comp hg hf

end AutoProved

