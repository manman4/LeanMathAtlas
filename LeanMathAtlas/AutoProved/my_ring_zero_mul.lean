import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_zero_mul (a : R) : 0 * a = 0
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a : R
--   ⊢ 0 * a = 0
-- added: 2026-06-10
theorem my_ring_zero_mul (a : R) : 0 * a = 0 := by
  ring

end AutoProved

