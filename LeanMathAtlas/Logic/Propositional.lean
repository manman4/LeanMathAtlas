import Mathlib.Tactic

/-!
# Propositional Logic

Classical and intuitionistic propositional logic in Lean 4:
introduction/elimination rules, De Morgan's laws, and tautologies.

**Requires**: `Prop`
**Tags**: Logic
-/

-- ============================================================
-- 1. True と False
-- ============================================================

-- True は常に証明可能
example : True := trivial

-- False からは何でも導ける（爆発律 / ex falso）
example : False → 1 = 2 := by
  intro h
  exact h.elim

-- ============================================================
-- 2. 含意 (→) — intro と exact
-- ============================================================

-- P → P（恒等関数 / 同一律）
-- intro: ゴールが P → Q のとき、P を仮定に加えてゴールを Q にする
-- exact: ゴールと完全に一致する項を与えて証明を完了する
example (P : Prop) : P → P := by
  intro h   -- h : P がコンテキストに追加され、ゴールは P になる
  exact h   -- h がゴール P と一致するので証明完了

-- P → Q → P（弱化 / weakening）
example (P Q : Prop) : P → Q → P := by
  intro hp _hq
  exact hp

-- 含意の推移律: (P → Q) → (Q → R) → (P → R)
-- apply: ゴールが R のとき、Q → R を apply すると新しいゴールが Q になる
example (P Q R : Prop) : (P → Q) → (Q → R) → (P → R) := by
  intro hpq hqr hp
  apply hqr
  apply hpq
  exact hp

-- ============================================================
-- 3. 論理積 (∧ / And) — constructor, And.left, And.right
-- ============================================================

-- P ∧ Q を証明するには、P と Q の両方を証明する
-- constructor: ゴールが P ∧ Q のとき、2つのサブゴール P と Q に分割する
example (P Q : Prop) (hp : P) (hq : Q) : P ∧ Q := by
  constructor
  · exact hp   -- 第1サブゴール: P
  · exact hq   -- 第2サブゴール: Q

-- P ∧ Q から P を取り出す
example (P Q : Prop) (h : P ∧ Q) : P := by
  exact h.left   -- または h.1

-- P ∧ Q から Q を取り出す
example (P Q : Prop) (h : P ∧ Q) : Q := by
  exact h.right  -- または h.2

-- 論理積の交換法則: P ∧ Q → Q ∧ P
-- obtain: 仮定を分解する（h を hp と hq に分ける）
example (P Q : Prop) : P ∧ Q → Q ∧ P := by
  intro h
  obtain ⟨hp, hq⟩ := h
  constructor
  · exact hq
  · exact hp

-- ============================================================
-- 4. 論理和 (∨ / Or) — Or.inl, Or.inr, rcases
-- ============================================================

-- P から P ∨ Q を証明する（左側）
-- Or.inl: 左側の命題から論理和を構成する
example (P Q : Prop) (hp : P) : P ∨ Q := by
  left       -- ゴールが P になる
  exact hp

-- Q から P ∨ Q を証明する（右側）
-- Or.inr: 右側の命題から論理和を構成する
example (P Q : Prop) (hq : Q) : P ∨ Q := by
  right      -- ゴールが Q になる
  exact hq

-- 論理和の交換法則: P ∨ Q → Q ∨ P
-- rcases: 仮定を場合分けする
example (P Q : Prop) : P ∨ Q → Q ∨ P := by
  intro h
  rcases h with hp | hq
  · right; exact hp    -- P の場合: Q ∨ P の右側
  · left; exact hq     -- Q の場合: Q ∨ P の左側

-- ============================================================
-- 5. 否定 (¬) — ¬P は P → False の略記
-- ============================================================

-- ¬False は True と同じ
example : ¬False := by
  intro h
  exact h

-- 対偶: (P → Q) → (¬Q → ¬P)
example (P Q : Prop) : (P → Q) → (¬Q → ¬P) := by
  intro hpq hnq hp
  apply hnq
  apply hpq
  exact hp

-- 矛盾から何でも: P → ¬P → Q
example (P Q : Prop) : P → ¬P → Q := by
  intro hp hnp
  exact absurd hp hnp

-- ============================================================
-- 6. 同値 (↔ / Iff)
-- ============================================================

-- P ↔ P（反射律）
example (P : Prop) : P ↔ P := by
  constructor
  · intro h; exact h
  · intro h; exact h

-- P ∧ Q ↔ Q ∧ P（論理積の交換法則、同値版）
example (P Q : Prop) : P ∧ Q ↔ Q ∧ P := by
  constructor
  · intro ⟨hp, hq⟩
    exact ⟨hq, hp⟩
  · intro ⟨hq, hp⟩
    exact ⟨hp, hq⟩

-- ↔ を使った書き換え
example (P Q : Prop) (h : P ↔ Q) (hp : P) : Q := by
  exact h.mp hp   -- mp = modus ponens（→ 方向）

-- ============================================================
-- 7. 組み合わせた証明
-- ============================================================

-- ド・モルガンの法則（一方向）: ¬(P ∨ Q) → ¬P ∧ ¬Q
example (P Q : Prop) : ¬(P ∨ Q) → ¬P ∧ ¬Q := by
  intro h
  constructor
  · intro hp
    apply h
    left; exact hp
  · intro hq
    apply h
    right; exact hq

-- 分配法則: P ∧ (Q ∨ R) → (P ∧ Q) ∨ (P ∧ R)
example (P Q R : Prop) : P ∧ (Q ∨ R) → (P ∧ Q) ∨ (P ∧ R) := by
  intro ⟨hp, hqr⟩
  rcases hqr with hq | hr
  · left; exact ⟨hp, hq⟩
  · right; exact ⟨hp, hr⟩
