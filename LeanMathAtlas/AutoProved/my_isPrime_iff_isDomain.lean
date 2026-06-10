import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_isPrime_iff_isDomain (I : Ideal R) : I.IsPrime ↔ IsDomain (R ⧸ I)
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   ⊢ I.IsPrime ↔ IsDomain (R ⧸ I)
-- added: 2026-06-10
theorem my_isPrime_iff_isDomain (I : Ideal R) : I.IsPrime ↔ IsDomain (R ⧸ I) := by
  exact Iff.symm (Ideal.Quotient.isDomain_iff_prime I)

end AutoProved

