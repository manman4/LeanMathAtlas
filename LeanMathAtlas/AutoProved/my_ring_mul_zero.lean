import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_mul_zero (a : R) : a * 0 = 0
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a : R
--   ⊢ a * 0 = 0
-- added: 2026-06-10
theorem my_ring_mul_zero (a : R) : a * 0 = 0 := by
  ring

end AutoProved

