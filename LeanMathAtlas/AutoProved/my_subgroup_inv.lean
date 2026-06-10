import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_subgroup_inv {H : Subgroup G} {a : G} (ha : a ∈ H) : a⁻¹ ∈ H
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   H : Subgroup G
--   a : G
--   ha : a ∈ H
--   ⊢ a⁻¹ ∈ H
-- added: 2026-06-10
theorem my_subgroup_inv {H : Subgroup G} {a : G} (ha : a ∈ H) : a⁻¹ ∈ H := by
  aesop

end AutoProved

