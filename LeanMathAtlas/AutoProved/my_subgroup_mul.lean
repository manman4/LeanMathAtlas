import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_subgroup_mul {H : Subgroup G} {a b : G} (ha : a ∈ H) (hb : b ∈ H) : a * b ∈ H
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   H : Subgroup G
--   a b : G
--   ha : a ∈ H
--   hb : b ∈ H
--   ⊢ a * b ∈ H
-- added: 2026-06-10
theorem my_subgroup_mul {H : Subgroup G} {a b : G} (ha : a ∈ H) (hb : b ∈ H) : a * b ∈ H := by
  aesop

end AutoProved

