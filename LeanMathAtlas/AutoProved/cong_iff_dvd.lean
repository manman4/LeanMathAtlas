import Mathlib

namespace AutoProved
-- stmt: theorem cong_iff_dvd (a b : ℤ) (n : ℕ) : (a : ZMod n) = b ↔ (n : ℤ) ∣ b - a
-- goal:
--   a b : ℤ
--   n : ℕ
--   ⊢ ↑a = ↑b ↔ ↑n ∣ b - a
-- added: 2026-06-10
theorem cong_iff_dvd (a b : ℤ) (n : ℕ) : (a : ZMod n) = b ↔ (n : ℤ) ∣ b - a := by
  exact ZMod.intCast_eq_intCast_iff_dvd_sub a b n

end AutoProved

