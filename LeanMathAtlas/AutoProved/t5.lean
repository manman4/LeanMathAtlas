import Mathlib

namespace AutoProved
-- stmt: theorem t5 (a b c : ℕ) : (a + b) + c = a + (b + c)
-- goal:
--   a b c : ℕ
--   ⊢ a + b + c = a + (b + c)
-- added: 2026-06-09
theorem t5 (a b c : ℕ) : (a + b) + c = a + (b + c) := by
  omega

end AutoProved

