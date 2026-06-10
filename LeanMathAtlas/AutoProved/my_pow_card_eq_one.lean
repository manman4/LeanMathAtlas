import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_pow_card_eq_one [Fintype G] (a : G) : a ^ Fintype.card G = 1
-- goal:
--   G : Type u_1
--   inst✝¹ : Group G
--   inst✝ : Fintype G
--   a : G
--   ⊢ a ^ Fintype.card G = 1
-- added: 2026-06-10
theorem my_pow_card_eq_one [Fintype G] (a : G) : a ^ Fintype.card G = 1 := by
  norm_num

end AutoProved

