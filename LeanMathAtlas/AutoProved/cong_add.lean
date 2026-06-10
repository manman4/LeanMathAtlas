import Mathlib

namespace AutoProved
-- stmt: theorem cong_add {n : ℕ} {a b : ZMod n} (h : a = b) (c : ZMod n) : a + c = b + c
-- goal:
--   n : ℕ
--   a b : ZMod n
--   h : a = b
--   c : ZMod n
--   ⊢ a + c = b + c
-- added: 2026-06-10
theorem cong_add {n : ℕ} {a b : ZMod n} (h : a = b) (c : ZMod n) : a + c = b + c := by
  exact (add_left_inj c).mpr h

end AutoProved

