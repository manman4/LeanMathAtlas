import Mathlib

open Real

namespace AutoProved
-- stmt: theorem sin_pi_div_two : sin (π / 2) = 1
-- goal:
--   ⊢ sin (π / 2) = 1
-- added: 2026-06-10
theorem sin_pi_div_two : sin (π / 2) = 1 := by
  simp

end AutoProved

