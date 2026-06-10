import Mathlib

open Real

namespace AutoProved
-- stmt: theorem my_deriv_comp {f g : ℝ → ℝ} {f' g' a : ℝ} (hg : HasDerivAt g g' (f a)) (hf : HasDerivAt f f' a) : HasDerivAt (g ∘ f) (g' * f') a
-- goal:
--   f g : ℝ → ℝ
--   f' g' a : ℝ
--   hg : HasDerivAt g g' (f a)
--   hf : HasDerivAt f f' a
--   ⊢ HasDerivAt (g ∘ f) (g' * f') a
-- added: 2026-06-10
theorem my_deriv_comp {f g : ℝ → ℝ} {f' g' a : ℝ} (hg : HasDerivAt g g' (f a)) (hf : HasDerivAt f f' a) : HasDerivAt (g ∘ f) (g' * f') a := by
  exact HasDerivAt.comp a hg hf

end AutoProved

