import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem I_sq : (I : ℂ) ^ 2 = -1
-- goal:
--   ⊢ I ^ 2 = -1
-- added: 2026-06-10
theorem I_sq : (I : ℂ) ^ 2 = -1 := by
  norm_num

end AutoProved

