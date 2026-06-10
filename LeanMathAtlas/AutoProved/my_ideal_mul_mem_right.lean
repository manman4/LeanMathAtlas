import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ideal_mul_mem_right (I : Ideal R) (r : R) {a : R} (ha : a ∈ I) : a * r ∈ I
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   r a : R
--   ha : a ∈ I
--   ⊢ a * r ∈ I
-- added: 2026-06-10
theorem my_ideal_mul_mem_right (I : Ideal R) (r : R) {a : R} (ha : a ∈ I) : a * r ∈ I := by
  exact Ideal.IsTwoSided.mul_mem_of_left r ha

end AutoProved

