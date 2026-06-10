import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem ker_intCast_eq_span (n : ℕ) : RingHom.ker (Int.castRingHom (ZMod n)) = Ideal.span ({(n : ℤ)} : Set ℤ)
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   n : ℕ
--   ⊢ RingHom.ker (Int.castRingHom (ZMod n)) = Ideal.span {↑n}
-- added: 2026-06-10
theorem ker_intCast_eq_span (n : ℕ) : RingHom.ker (Int.castRingHom (ZMod n)) = Ideal.span ({(n : ℤ)} : Set ℤ) := by
  exact ZMod.ker_intCastRingHom n

end AutoProved

