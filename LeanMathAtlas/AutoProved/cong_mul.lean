import Mathlib

namespace AutoProved
-- stmt: theorem cong_mul {n : ℕ} {a b : ZMod n} (h : a = b) (c : ZMod n) : a * c = b * c
-- goal:
--   n : ℕ
--   a b : ZMod n
--   h : a = b
--   c : ZMod n
--   ⊢ a * c = b * c
-- added: 2026-06-10
theorem cong_mul {n : ℕ} {a b : ZMod n} (h : a = b) (c : ZMod n) : a * c = b * c := by
  exact ZMod.valMinAbs_inj.mp (congrArg ZMod.valMinAbs (congrFun (congrArg HMul.hMul h) c))

end AutoProved

