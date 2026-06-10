import Mathlib

namespace AutoProved
-- stmt: theorem even_add_even (a b : Nat) (ha : Even a) (hb : Even b) : Even (a + b)
-- goal:
--   a b : ℕ
--   ha : Even a
--   hb : Even b
--   ⊢ Even (a + b)
-- added: 2026-06-10
theorem even_add_even (a b : Nat) (ha : Even a) (hb : Even b) : Even (a + b) := by
  exact Even.add ha hb

end AutoProved

