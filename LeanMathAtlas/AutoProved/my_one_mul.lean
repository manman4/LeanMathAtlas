import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_one_mul (a : G) : 1 * a = a
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a : G
--   ⊢ 1 * a = a
-- added: 2026-06-10
theorem my_one_mul (a : G) : 1 * a = a := by
  simp

end AutoProved

