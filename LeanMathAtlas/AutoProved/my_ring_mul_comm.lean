import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_mul_comm (a b : R) : a * b = b * a
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a b : R
--   ⊢ a * b = b * a
-- added: 2026-06-10
theorem my_ring_mul_comm (a b : R) : a * b = b * a := by
  ring

end AutoProved

