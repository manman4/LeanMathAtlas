import Mathlib

open Real

namespace AutoProved
-- stmt: theorem tan_def (x : ℝ) : tan x = sin x / cos x
-- goal:
--   x : ℝ
--   ⊢ tan x = sin x / cos x
-- added: 2026-06-10
theorem tan_def (x : ℝ) : tan x = sin x / cos x := by
  exact tan_eq_sin_div_cos x

end AutoProved

