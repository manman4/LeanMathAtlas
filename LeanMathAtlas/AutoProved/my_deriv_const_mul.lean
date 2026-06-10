import Mathlib

open Real

namespace AutoProved
-- stmt: theorem my_deriv_const_mul {f : ℝ → ℝ} {f' a c : ℝ} (hf : HasDerivAt f f' a) : HasDerivAt (fun x => c * f x) (c * f') a
-- goal:
--   f : ℝ → ℝ
--   f' a c : ℝ
--   hf : HasDerivAt f f' a
--   ⊢ HasDerivAt (fun x => c * f x) (c * f') a
-- added: 2026-06-10
theorem my_deriv_const_mul {f : ℝ → ℝ} {f' a c : ℝ} (hf : HasDerivAt f f' a) : HasDerivAt (fun x => c * f x) (c * f') a := by
  exact HasDerivAt.const_mul c hf

end AutoProved

