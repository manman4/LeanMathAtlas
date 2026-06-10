import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ideal_mul_mem_left (I : Ideal R) (r : R) {a : R} (ha : a ∈ I) : r * a ∈ I
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   r a : R
--   ha : a ∈ I
--   ⊢ r * a ∈ I
-- added: 2026-06-10
theorem my_ideal_mul_mem_left (I : Ideal R) (r : R) {a : R} (ha : a ∈ I) : r * a ∈ I := by
  exact Ideal.mul_mem_left I r ha

end AutoProved

