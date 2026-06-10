import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem lagrange_index (H : Subgroup G) : Nat.card H * H.index = Nat.card G
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   H : Subgroup G
--   ⊢ Nat.card ↥H * H.index = Nat.card G
-- added: 2026-06-10
theorem lagrange_index (H : Subgroup G) : Nat.card H * H.index = Nat.card G := by
  simp

end AutoProved

