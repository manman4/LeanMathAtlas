import Mathlib

namespace AutoProved
-- stmt: theorem zmod_prime_inv {p : ℕ} [Fact (Nat.Prime p)] (a : ZMod p) (ha : a ≠ 0) : a * a⁻¹ = 1
-- goal:
--   p : ℕ
--   inst✝ : Fact (Nat.Prime p)
--   a : ZMod p
--   ha : a ≠ 0
--   ⊢ a * a⁻¹ = 1
-- added: 2026-06-10
theorem zmod_prime_inv {p : ℕ} [Fact (Nat.Prime p)] (a : ZMod p) (ha : a ≠ 0) : a * a⁻¹ = 1 := by
  exact CommGroupWithZero.mul_inv_cancel a ha

end AutoProved

