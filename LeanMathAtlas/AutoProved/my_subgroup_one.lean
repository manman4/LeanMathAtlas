import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_subgroup_one (H : Subgroup G) : (1 : G) ∈ H
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   H : Subgroup G
--   ⊢ 1 ∈ H
-- added: 2026-06-10
theorem my_subgroup_one (H : Subgroup G) : (1 : G) ∈ H := by
  simp

end AutoProved

