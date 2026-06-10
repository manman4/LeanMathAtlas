import Mathlib

open Real

namespace AutoProved
-- stmt: theorem cos_zero : cos 0 = 1
-- goal:
--   ⊢ cos 0 = 1
-- added: 2026-06-10
theorem cos_zero : cos 0 = 1 := by
  simp

end AutoProved

