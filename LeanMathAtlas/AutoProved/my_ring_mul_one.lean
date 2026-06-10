import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_mul_one (a : R) : a * 1 = a
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a : R
--   ⊢ a * 1 = a
-- added: 2026-06-10
theorem my_ring_mul_one (a : R) : a * 1 = a := by
  ring

end AutoProved

