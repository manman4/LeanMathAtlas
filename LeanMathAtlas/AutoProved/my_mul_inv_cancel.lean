import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_mul_inv_cancel (a : G) : a * a⁻¹ = 1
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a : G
--   ⊢ a * a⁻¹ = 1
-- added: 2026-06-10
theorem my_mul_inv_cancel (a : G) : a * a⁻¹ = 1 := by
  simp

end AutoProved

