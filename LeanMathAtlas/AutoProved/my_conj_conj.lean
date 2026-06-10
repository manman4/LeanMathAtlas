import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem my_conj_conj (z : ℂ) : conj (conj z : ℂ) = z
-- goal:
--   z : ℂ
--   ⊢ (starRingEnd ℂ) ((starRingEnd ℂ) z) = z
-- added: 2026-06-10
theorem my_conj_conj (z : ℂ) : conj (conj z : ℂ) = z := by
  simp

end AutoProved

