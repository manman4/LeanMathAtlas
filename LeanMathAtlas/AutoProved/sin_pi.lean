import Mathlib

open Real

namespace AutoProved
-- stmt: theorem sin_pi : sin π = 0
-- goal:
--   ⊢ sin π = 0
-- added: 2026-06-10
theorem sin_pi : sin π = 0 := by
  simp

end AutoProved

