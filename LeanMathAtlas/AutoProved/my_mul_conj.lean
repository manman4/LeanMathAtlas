import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem my_mul_conj (z : ℂ) : z * conj z = ‖z‖ ^ 2
-- goal:
--   z : ℂ
--   ⊢ z * (starRingEnd ℂ) z = ↑‖z‖ ^ 2
-- added: 2026-06-10
theorem my_mul_conj (z : ℂ) : z * conj z = ‖z‖ ^ 2 := by
  exact mul_conj' z

end AutoProved

