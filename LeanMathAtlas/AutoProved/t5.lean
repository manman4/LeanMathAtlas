import Mathlib
import LeanMathAtlas.AutoProved.t1
import LeanMathAtlas.AutoProved.t2
import LeanMathAtlas.AutoProved.t3
import LeanMathAtlas.AutoProved.t4

namespace AutoProved
-- stmt: theorem t5 (a b c : ℕ) : (a + b) + c = a + (b + c)
-- goal:
--   a b c : ℕ
--   ⊢ a + b + c = a + (b + c)
-- added: 2026-06-09
theorem t5 (a b c : ℕ) : (a + b) + c = a + (b + c) := by
  omega

end AutoProved

