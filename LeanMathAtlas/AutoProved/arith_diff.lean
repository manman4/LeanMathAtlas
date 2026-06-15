import Mathlib
import LeanMathAtlas.Algebra.Sequences

open BigOperators

namespace AutoProved
-- stmt: theorem arith_diff (a d : ℤ) (n : ℕ) : arith a d (n + 1) - arith a d n = d
-- goal:
--   a d : ℤ
--   n : ℕ
--   ⊢ arith a d (n + 1) - arith a d n = d
-- added: 2026-06-15
theorem arith_diff (a d : ℤ) (n : ℕ) : arith a d (n + 1) - arith a d n = d := by
  simp [arith]
  ring

end AutoProved
