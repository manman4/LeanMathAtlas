import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem my_norm_mul (z w : ℂ) : ‖z * w‖ = ‖z‖ * ‖w‖
-- goal:
--   z w : ℂ
--   ⊢ ‖z * w‖ = ‖z‖ * ‖w‖
-- added: 2026-06-10
theorem my_norm_mul (z w : ℂ) : ‖z * w‖ = ‖z‖ * ‖w‖ := by
  simp

end AutoProved

