import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem lagrange (H : Subgroup G) : Nat.card H ∣ Nat.card G
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   H : Subgroup G
--   ⊢ Nat.card ↥H ∣ Nat.card G
-- added: 2026-06-10
theorem lagrange (H : Subgroup G) : Nat.card H ∣ Nat.card G := by
  exact Subgroup.card_subgroup_dvd_card H

end AutoProved

