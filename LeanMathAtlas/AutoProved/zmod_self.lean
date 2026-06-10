import Mathlib

namespace AutoProved
-- stmt: theorem zmod_self (n : ℕ) : (n : ZMod n) = 0
-- goal:
--   n : ℕ
--   ⊢ ↑n = 0
-- added: 2026-06-10
theorem zmod_self (n : ℕ) : (n : ZMod n) = 0 := by
  simp

end AutoProved

