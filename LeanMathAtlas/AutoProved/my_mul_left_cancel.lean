import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_mul_left_cancel {a b c : G} (h : a * b = a * c) : b = c
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a b c : G
--   h : a * b = a * c
--   ⊢ b = c
-- added: 2026-06-10
theorem my_mul_left_cancel {a b c : G} (h : a * b = a * c) : b = c := by
  aesop

end AutoProved

