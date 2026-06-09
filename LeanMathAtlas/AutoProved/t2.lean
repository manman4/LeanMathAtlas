import Mathlib

namespace AutoProved
-- stmt: theorem t2 (n : ℕ) : n + 0 = n
-- goal:
--   n : ℕ
--   ⊢ n + 0 = n
-- added: 2026-06-09
theorem t2 (n : ℕ) : n + 0 = n := by
  omega

end AutoProved

