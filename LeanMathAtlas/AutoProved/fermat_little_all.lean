import Mathlib

namespace AutoProved
-- stmt: theorem fermat_little_all {p : ℕ} [hp : Fact (Nat.Prime p)] (a : ZMod p) : a ^ p = a
-- goal:
--   p : ℕ
--   hp : Fact (Nat.Prime p)
--   a : ZMod p
--   ⊢ a ^ p = a
-- added: 2026-06-10
theorem fermat_little_all {p : ℕ} [hp : Fact (Nat.Prime p)] (a : ZMod p) : a ^ p = a := by
  simp

end AutoProved

