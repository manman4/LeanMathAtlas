import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_inv_inv (a : G) : a⁻¹⁻¹ = a
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a : G
--   ⊢ a⁻¹⁻¹ = a
-- added: 2026-06-10
theorem my_inv_inv (a : G) : a⁻¹⁻¹ = a := by
  simp

end AutoProved

