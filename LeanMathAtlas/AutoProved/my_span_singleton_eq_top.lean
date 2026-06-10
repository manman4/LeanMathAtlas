import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_span_singleton_eq_top (a : R) : Ideal.span ({a} : Set R) = ⊤ ↔ IsUnit a
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a : R
--   ⊢ Ideal.span {a} = ⊤ ↔ IsUnit a
-- added: 2026-06-10
theorem my_span_singleton_eq_top (a : R) : Ideal.span ({a} : Set R) = ⊤ ↔ IsUnit a := by
  simp

end AutoProved

