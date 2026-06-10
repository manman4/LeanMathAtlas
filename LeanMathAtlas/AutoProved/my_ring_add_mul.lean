import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_add_mul (a b c : R) : (a + b) * c = a * c + b * c
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a b c : R
--   ⊢ (a + b) * c = a * c + b * c
-- added: 2026-06-10
theorem my_ring_add_mul (a b c : R) : (a + b) * c = a * c + b * c := by
  ring

end AutoProved

