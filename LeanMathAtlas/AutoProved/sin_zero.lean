import Mathlib

open Real

namespace AutoProved
-- stmt: theorem sin_zero : sin 0 = 0
-- goal:
--   ⊢ sin 0 = 0
-- added: 2026-06-10
theorem sin_zero : sin 0 = 0 := by
  simp

end AutoProved

