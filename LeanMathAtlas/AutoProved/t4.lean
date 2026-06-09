import Mathlib
import LeanMathAtlas.AutoProved.t1
import LeanMathAtlas.AutoProved.t2
import LeanMathAtlas.AutoProved.t3

namespace AutoProved
-- stmt: theorem t4 (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2
-- goal:
--   a b : ℝ
--   ⊢ (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2
-- added: 2026-06-09
theorem t4 (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by
  ring

end AutoProved

