import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_orderOf_dvd_card [Fintype G] (a : G) : orderOf a ∣ Fintype.card G
-- goal:
--   G : Type u_1
--   inst✝¹ : Group G
--   inst✝ : Fintype G
--   a : G
--   ⊢ orderOf a ∣ Fintype.card G
-- added: 2026-06-10
theorem my_orderOf_dvd_card [Fintype G] (a : G) : orderOf a ∣ Fintype.card G := by
  exact orderOf_dvd_card

end AutoProved

