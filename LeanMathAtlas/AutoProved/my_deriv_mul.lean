import Mathlib

open Real

namespace AutoProved
-- stmt: theorem my_deriv_mul {f g : ℝ → ℝ} {f' g' a : ℝ} (hf : HasDerivAt f f' a) (hg : HasDerivAt g g' a) : HasDerivAt (fun x => f x * g x) (f' * g a + f a * g') a
-- goal:
--   f g : ℝ → ℝ
--   f' g' a : ℝ
--   hf : HasDerivAt f f' a
--   hg : HasDerivAt g g' a
--   ⊢ HasDerivAt (fun x => f x * g x) (f' * g a + f a * g') a
-- added: 2026-06-10
theorem my_deriv_mul {f g : ℝ → ℝ} {f' g' a : ℝ} (hf : HasDerivAt f f' a) (hg : HasDerivAt g g' a) : HasDerivAt (fun x => f x * g x) (f' * g a + f a * g') a := by
  exact HasDerivAt.fun_mul hf hg

end AutoProved

