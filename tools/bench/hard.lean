import Mathlib

-- Multi-step `have` with specific Mathlib lemmas
theorem bench_hard_deriv (a : ℝ) : HasDerivAt (fun x => 2 * Real.sin x) (2 * Real.cos a) a := by sorry
theorem bench_hard_prime_inf : ∀ n : ℕ, ∃ p, n ≤ p ∧ Nat.Prime p := by sorry
-- sqrt: needs Real.sqrt_sq
theorem bench_hard_sqrt (a : ℝ) (ha : 0 ≤ a) : Real.sqrt (a ^ 2) = a := by sorry
-- continuous composition: needs Continuous.comp or fun_prop
theorem bench_hard_cont_comp (f g : ℝ → ℝ) (hf : Continuous f) (hg : Continuous g) : Continuous (f ∘ g) := by sorry
-- chain rule sin(2x): needs HasDerivAt.comp
theorem bench_hard_chain (a : ℝ) : HasDerivAt (fun x => Real.sin (2 * x)) (2 * Real.cos (2 * a)) a := by sorry
-- irrational sqrt 2: direct Mathlib lemma
theorem bench_hard_irrational_sqrt2 : Irrational (Real.sqrt 2) := by sorry
-- integer mod mod: needs Int.emod_emod_of_dvd
theorem bench_hard_emod (a b c : ℤ) (h : c ∣ b) : a % b % c = a % c := by sorry
-- finset card of even numbers: needs Finset manipulation
theorem bench_hard_card_filter (n : ℕ) : ((Finset.range (2 * n)).filter (fun k => k % 2 = 0)).card = n := by sorry
-- single-trig inequality: needs sin_sq_add_cos_sq injected as have (Phase 3 target)
theorem bench_hard_sin_sq_double (x : ℝ) : 2 * Real.sin x ^ 2 ≤ 2 := by sorry
