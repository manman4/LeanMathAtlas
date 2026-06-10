import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_isMaximal_isPrime (I : Ideal R) (hM : I.IsMaximal) : I.IsPrime
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   hM : I.IsMaximal
--   ⊢ I.IsPrime
-- added: 2026-06-10
theorem my_isMaximal_isPrime (I : Ideal R) (hM : I.IsMaximal) : I.IsPrime := by
  exact Ideal.IsMaximal.isPrime hM

end AutoProved

