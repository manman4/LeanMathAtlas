import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_ring_mul_add (a b c : R) : a * (b + c) = a * b + a * c
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a b c : R
--   ⊢ a * (b + c) = a * b + a * c
-- added: 2026-06-10
theorem my_ring_mul_add (a b c : R) : a * (b + c) = a * b + a * c := by
  ring

end AutoProved

