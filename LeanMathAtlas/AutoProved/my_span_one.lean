import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_span_one : (Ideal.span ({1} : Set R)) = ⊤
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   ⊢ Ideal.span {1} = ⊤
-- added: 2026-06-10
theorem my_span_one : (Ideal.span ({1} : Set R)) = ⊤ := by
  simp

end AutoProved

