import Mathlib

namespace AutoProved
-- stmt: theorem my_add_comm (a b : Nat) : a + b = b + a
-- goal:
--   a b : ℕ
--   ⊢ a + b = b + a
-- added: 2026-06-10
theorem my_add_comm (a b : Nat) : a + b = b + a := by
  omega

end AutoProved

