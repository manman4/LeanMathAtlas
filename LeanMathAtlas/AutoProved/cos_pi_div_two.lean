import Mathlib

open Real

namespace AutoProved
-- stmt: theorem cos_pi_div_two : cos (π / 2) = 0
-- goal:
--   ⊢ cos (π / 2) = 0
-- added: 2026-06-10
theorem cos_pi_div_two : cos (π / 2) = 0 := by
  simp

end AutoProved

