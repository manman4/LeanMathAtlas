import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem remainder_theorem (p : ℝ[X]) (a : ℝ) : p %ₘ (X - C a) = C (p.eval a)
-- goal:
--   p : ℝ[X]
--   a : ℝ
--   ⊢ p %ₘ (X - C a) = C (eval a p)
-- added: 2026-06-09
theorem remainder_theorem (p : ℝ[X]) (a : ℝ) : p %ₘ (X - C a) = C (p.eval a) := by
  norm_num

end AutoProved

