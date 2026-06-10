import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_eq_inv_mul_of_mul_eq {a b c : G} (h : a * b = c) : b = a⁻¹ * c
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a b c : G
--   h : a * b = c
--   ⊢ b = a⁻¹ * c
-- added: 2026-06-10
theorem my_eq_inv_mul_of_mul_eq {a b c : G} (h : a * b = c) : b = a⁻¹ * c := by
  aesop

end AutoProved

