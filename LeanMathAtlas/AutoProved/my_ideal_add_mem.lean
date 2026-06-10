import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ideal_add_mem (I : Ideal R) {a b : R} (ha : a ∈ I) (hb : b ∈ I) : a + b ∈ I
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   a b : R
--   ha : a ∈ I
--   hb : b ∈ I
--   ⊢ a + b ∈ I
-- added: 2026-06-10
theorem my_ideal_add_mem (I : Ideal R) {a b : R} (ha : a ∈ I) (hb : b ∈ I) : a + b ∈ I := by
  aesop

end AutoProved

