import Mathlib
import LeanMathAtlas.Algebra.Sequences

open BigOperators

namespace AutoProved
-- stmt: theorem arith_zero (a d : ℤ) : arith a d 0 = a
-- goal:
--   a d : ℤ
--   ⊢ arith a d 0 = a
-- added: 2026-06-15
theorem arith_zero (a d : ℤ) : arith a d 0 = a := by
  simp [arith]

end AutoProved
