import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_quotient_eq_zero_iff (I : Ideal R) (a : R) : Ideal.Quotient.mk I a = 0 ↔ a ∈ I
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   a : R
--   ⊢ (Ideal.Quotient.mk I) a = 0 ↔ a ∈ I
-- added: 2026-06-10
theorem my_quotient_eq_zero_iff (I : Ideal R) (a : R) : Ideal.Quotient.mk I a = 0 ↔ a ∈ I := by
  exact Ideal.Quotient.eq_zero_iff_mem

end AutoProved

