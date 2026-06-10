import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem my_conj_add (z w : ℂ) : conj (z + w : ℂ) = conj z + conj w
-- goal:
--   z w : ℂ
--   ⊢ (starRingEnd ℂ) (z + w) = (starRingEnd ℂ) z + (starRingEnd ℂ) w
-- added: 2026-06-10
theorem my_conj_add (z w : ℂ) : conj (z + w : ℂ) = conj z + conj w := by
  simp

end AutoProved

