import Mathlib

variable {G : Type*} [Group G]

namespace AutoProved
-- stmt: theorem my_one_unique {e : G} (h : ∀ a : G, e * a = a) : e = 1
-- goal:
--   G : Type u_1
--   inst✝ : Group G
--   e : G
--   h : ∀ (a : G), e * a = a
--   ⊢ e = 1
-- added: 2026-06-10
theorem my_one_unique {e : G} (h : ∀ a : G, e * a = a) : e = 1 := by
  aesop

end AutoProved

