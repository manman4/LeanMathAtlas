import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_pow_orderOf_eq_one (a : G) : a ^ orderOf a = 1
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a : G
--   ⊢ a ^ orderOf a = 1
-- added: 2026-06-10
theorem my_pow_orderOf_eq_one (a : G) : a ^ orderOf a = 1 := by
  norm_num

end AutoProved

