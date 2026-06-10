import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_mul_one (a : G) : a * 1 = a
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a : G
--   ⊢ a * 1 = a
-- added: 2026-06-10
theorem my_mul_one (a : G) : a * 1 = a := by
  simp

end AutoProved

