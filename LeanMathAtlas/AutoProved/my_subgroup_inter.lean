import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_subgroup_inter {H K : Subgroup G} {a : G} (ha : a ∈ H) (hb : a ∈ K) : a ∈ H ⊓ K
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   H K : Subgroup G
--   a : G
--   ha : a ∈ H
--   hb : a ∈ K
--   ⊢ a ∈ H ⊓ K
-- added: 2026-06-10
theorem my_subgroup_inter {H K : Subgroup G} {a : G} (ha : a ∈ H) (hb : a ∈ K) : a ∈ H ⊓ K := by
  tauto

end AutoProved

