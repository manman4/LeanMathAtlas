import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_exists_le_maximal (I : Ideal R) (hI : I ≠ ⊤) : ∃ M : Ideal R, M.IsMaximal ∧ I ≤ M
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   I : Ideal R
--   hI : I ≠ ⊤
--   ⊢ ∃ M, M.IsMaximal ∧ I ≤ M
-- added: 2026-06-10
theorem my_exists_le_maximal (I : Ideal R) (hI : I ≠ ⊤) : ∃ M : Ideal R, M.IsMaximal ∧ I ≤ M := by
  exact Ideal.ne_top_iff_exists_maximal.mp hI

end AutoProved

