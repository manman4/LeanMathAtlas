import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_quotient_mk_eq_iff (I : Ideal R) (a b : R) : Ideal.Quotient.mk I a = Ideal.Quotient.mk I b ↔ a - b ∈ I
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   a b : R
--   ⊢ (Ideal.Quotient.mk I) a = (Ideal.Quotient.mk I) b ↔ a - b ∈ I
-- added: 2026-06-10
theorem my_quotient_mk_eq_iff (I : Ideal R) (a b : R) : Ideal.Quotient.mk I a = Ideal.Quotient.mk I b ↔ a - b ∈ I := by
  exact Ideal.Quotient.mk_eq_mk_iff_sub_mem a b

end AutoProved

