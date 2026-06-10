import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem normSq_sq (z : ℂ) : normSq z = z.re ^ 2 + z.im ^ 2
-- goal:
--   z : ℂ
--   ⊢ normSq z = z.re ^ 2 + z.im ^ 2
-- added: 2026-06-10
theorem normSq_sq (z : ℂ) : normSq z = z.re ^ 2 + z.im ^ 2 := by
  simp [normSq_apply, sq]

end AutoProved

