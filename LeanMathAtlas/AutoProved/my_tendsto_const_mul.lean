import Mathlib

open Filter Topology

namespace AutoProved
-- stmt: theorem my_tendsto_const_mul {f : ℝ → ℝ} {a b : ℝ} (c : ℝ) (hf : Tendsto f (𝓝 a) (𝓝 b)) : Tendsto (fun x => c * f x) (𝓝 a) (𝓝 (c * b))
-- goal:
--   f : ℝ → ℝ
--   a b c : ℝ
--   hf : Tendsto f (𝓝 a) (𝓝 b)
--   ⊢ Tendsto (fun x => c * f x) (𝓝 a) (𝓝 (c * b))
-- added: 2026-06-10
theorem my_tendsto_const_mul {f : ℝ → ℝ} {a b : ℝ} (c : ℝ) (hf : Tendsto f (𝓝 a) (𝓝 b)) : Tendsto (fun x => c * f x) (𝓝 a) (𝓝 (c * b)) := by
  exact Tendsto.const_mul c hf

end AutoProved

