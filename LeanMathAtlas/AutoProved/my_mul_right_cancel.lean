import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_mul_right_cancel {a b c : G} (h : a * b = c * b) : a = c
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a b c : G
--   h : a * b = c * b
--   ⊢ a = c
-- added: 2026-06-10
theorem my_mul_right_cancel {a b c : G} (h : a * b = c * b) : a = c := by
  aesop

end AutoProved

