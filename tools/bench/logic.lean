import Mathlib

-- 含意
theorem bench_imp_id (P : Prop) : P → P := by sorry
theorem bench_imp_weak (P Q : Prop) : P → Q → P := by sorry
theorem bench_imp_trans (P Q R : Prop) : (P → Q) → (Q → R) → (P → R) := by sorry
-- 論理積
theorem bench_and_intro (P Q : Prop) (hp : P) (hq : Q) : P ∧ Q := by sorry
theorem bench_and_left (P Q : Prop) (h : P ∧ Q) : P := by sorry
theorem bench_and_right (P Q : Prop) (h : P ∧ Q) : Q := by sorry
theorem bench_and_comm (P Q : Prop) : P ∧ Q → Q ∧ P := by sorry
-- 論理和
theorem bench_or_inl (P Q : Prop) (hp : P) : P ∨ Q := by sorry
theorem bench_or_inr (P Q : Prop) (hq : Q) : P ∨ Q := by sorry
theorem bench_or_comm (P Q : Prop) : P ∨ Q → Q ∨ P := by sorry
-- 否定
theorem bench_not_false : ¬False := by sorry
theorem bench_contrapos (P Q : Prop) : (P → Q) → (¬Q → ¬P) := by sorry
theorem bench_absurd_ex (P Q : Prop) : P → ¬P → Q := by sorry
-- 同値
theorem bench_iff_refl (P : Prop) : P ↔ P := by sorry
theorem bench_iff_mp (P Q : Prop) (h : P ↔ Q) (hp : P) : Q := by sorry
-- ド・モルガン
theorem bench_demorgan (P Q : Prop) : ¬(P ∨ Q) → ¬P ∧ ¬Q := by sorry
