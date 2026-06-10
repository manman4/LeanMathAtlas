import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_orderOf_dvd_of_pow_eq_one {a : G} {n : ℕ} (h : a ^ n = 1) : orderOf a ∣ n
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   a : G
--   n : ℕ
--   h : a ^ n = 1
--   ⊢ orderOf a ∣ n
-- added: 2026-06-10
theorem my_orderOf_dvd_of_pow_eq_one {a : G} {n : ℕ} (h : a ^ n = 1) : orderOf a ∣ n := by
  exact orderOf_dvd_of_pow_eq_one h

end AutoProved

