import Mathlib

namespace AutoProved
-- stmt: theorem my_add_assoc (a b c : Nat) : (a + b) + c = a + (b + c)
-- goal:
--   a b c : ℕ
--   ⊢ a + b + c = a + (b + c)
-- added: 2026-06-10
theorem my_add_assoc (a b c : Nat) : (a + b) + c = a + (b + c) := by
  omega

end AutoProved

