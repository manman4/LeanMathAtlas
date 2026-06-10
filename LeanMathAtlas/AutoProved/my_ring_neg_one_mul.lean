import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_neg_one_mul (a : R) : -1 * a = -a
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a : R
--   ⊢ -1 * a = -a
-- added: 2026-06-10
theorem my_ring_neg_one_mul (a : R) : -1 * a = -a := by
  ring

end AutoProved

