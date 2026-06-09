import Mathlib

open Polynomial

namespace AutoProved
-- stmt: theorem vertex_form_nonneg (a p q x : ℝ) (ha : 0 ≤ a) : a * (x - p)^2 + q ≥ q
-- goal:
--   a p q x : ℝ
--   ha : 0 ≤ a
--   ⊢ a * (x - p) ^ 2 + q ≥ q
-- added: 2026-06-09
theorem vertex_form_nonneg (a p q x : ℝ) (ha : 0 ≤ a) : a * (x - p)^2 + q ≥ q := by
  nlinarith [sq_nonneg (a - p), sq_nonneg (a - q), sq_nonneg (a - x), sq_nonneg (p - q), sq_nonneg (p - x), sq_nonneg (q - x), sq_nonneg (a*x - p*q)]

end AutoProved

