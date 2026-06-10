import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_isMaximal_iff_isField (I : Ideal R) : I.IsMaximal ↔ IsField (R ⧸ I)
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   ⊢ I.IsMaximal ↔ IsField (R ⧸ I)
-- added: 2026-06-10
theorem my_isMaximal_iff_isField (I : Ideal R) : I.IsMaximal ↔ IsField (R ⧸ I) := by
  exact Ideal.Quotient.maximal_ideal_iff_isField_quotient I

end AutoProved

