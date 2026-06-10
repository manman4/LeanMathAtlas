import Mathlib

namespace AutoProved
-- stmt: theorem fermat_little {p : ℕ} [Fact (Nat.Prime p)] (a : ZMod p) (ha : a ≠ 0) : a ^ (p - 1) = 1
-- goal:
--   p : ℕ
--   inst✝ : Fact (Nat.Prime p)
--   a : ZMod p
--   ha : a ≠ 0
--   ⊢ a ^ (p - 1) = 1
-- added: 2026-06-10
theorem fermat_little {p : ℕ} [Fact (Nat.Prime p)] (a : ZMod p) (ha : a ≠ 0) : a ^ (p - 1) = 1 := by
  exact ZMod.pow_card_sub_one_eq_one ha

end AutoProved

