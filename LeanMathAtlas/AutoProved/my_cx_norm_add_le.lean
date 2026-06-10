import Mathlib

open Complex
open scoped ComplexConjugate

namespace AutoProved
-- stmt: theorem my_cx_norm_add_le (z w : ℂ) : ‖z + w‖ ≤ ‖z‖ + ‖w‖
-- goal:
--   z w : ℂ
--   ⊢ ‖z + w‖ ≤ ‖z‖ + ‖w‖
-- added: 2026-06-10
theorem my_cx_norm_add_le (z w : ℂ) : ‖z + w‖ ≤ ‖z‖ + ‖w‖ := by
  exact norm_add_le z w

end AutoProved

