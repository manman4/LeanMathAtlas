import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem my_tendsto_mul {f g : ℝ → ℝ} {a b c : ℝ} (hf : Tendsto f (𝓝 a) (𝓝 b)) (hg : Tendsto g (𝓝 a) (𝓝 c)) : Tendsto (fun x => f x * g x) (𝓝 a) (𝓝 (b * c))
-- goal:
--   f g : ℝ → ℝ
--   a b c : ℝ
--   hf : Tendsto f (𝓝 a) (𝓝 b)
--   hg : Tendsto g (𝓝 a) (𝓝 c)
--   ⊢ Tendsto (fun x => f x * g x) (𝓝 a) (𝓝 (b * c))
-- added: 2026-06-10
theorem my_tendsto_mul {f g : ℝ → ℝ} {a b c : ℝ} (hf : Tendsto f (𝓝 a) (𝓝 b)) (hg : Tendsto g (𝓝 a) (𝓝 c)) : Tendsto (fun x => f x * g x) (𝓝 a) (𝓝 (b * c)) := by
  exact Tendsto.mul hf hg

end AutoProved

