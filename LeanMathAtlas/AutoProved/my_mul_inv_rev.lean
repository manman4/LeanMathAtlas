import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_mul_inv_rev (a b : G) : (a * b)⁻¹ = b⁻¹ * a⁻¹
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a b : G
--   ⊢ (a * b)⁻¹ = b⁻¹ * a⁻¹
-- added: 2026-06-10
theorem my_mul_inv_rev (a b : G) : (a * b)⁻¹ = b⁻¹ * a⁻¹ := by
  simp

end AutoProved

