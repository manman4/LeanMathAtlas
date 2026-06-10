import Mathlib

open Real

namespace AutoProved
-- stmt: theorem my_hasDerivAt_pow (n : ℕ) (a : ℝ) : HasDerivAt (fun x => x ^ n) (↑n * a ^ (n - 1)) a
-- goal:
--   n : ℕ
--   a : ℝ
--   ⊢ HasDerivAt (fun x => x ^ n) (↑n * a ^ (n - 1)) a
-- added: 2026-06-10
theorem my_hasDerivAt_pow (n : ℕ) (a : ℝ) : HasDerivAt (fun x => x ^ n) (↑n * a ^ (n - 1)) a := by
  exact hasDerivAt_pow n a

end AutoProved

