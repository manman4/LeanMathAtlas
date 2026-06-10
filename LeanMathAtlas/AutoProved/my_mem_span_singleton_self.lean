import Mathlib

variable {R : Type*} [CommRing R]

namespace AutoProved
-- stmt: theorem my_mem_span_singleton_self (a : R) : a ∈ Ideal.span ({a} : Set R)
-- goal:
--   R : Type u_1
--   inst✝ : CommRing R
--   a : R
--   ⊢ a ∈ Ideal.span {a}
-- added: 2026-06-10
theorem my_mem_span_singleton_self (a : R) : a ∈ Ideal.span ({a} : Set R) := by
  exact Ideal.mem_span_singleton_self a

end AutoProved

