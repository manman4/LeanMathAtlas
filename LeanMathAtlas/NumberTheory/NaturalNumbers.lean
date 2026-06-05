import Mathlib.Tactic

/-!
# Natural Number Arithmetic

Basic properties of `ℕ` proved by induction:
divisibility, parity, and elementary number-theoretic identities.

**Requires**: `ℕ`
**Tags**: NumberTheory
-/

-- ============================================================
-- 1. 基本的な等式
-- ============================================================

-- 0 + n = n（加法の左単位元）
example (n : Nat) : 0 + n = n := by
  omega

-- n + 0 = n（加法の右単位元）
example (n : Nat) : n + 0 = n := by
  rfl

-- ============================================================
-- 2. 帰納法 (induction) の基本
-- ============================================================

-- 帰納法の構造:
-- 1. base case（基底）: n = 0 の場合を証明
-- 2. inductive step（帰納段階）: n = k のとき成り立つと仮定して、n = k + 1 を証明

-- 例: 0 + n = n を帰納法で明示的に証明
-- (既存の zero_add と名前が衝突するため my_ を付ける)
theorem my_zero_add (n : Nat) : 0 + n = n := by
  induction n with
  | zero => rfl                        -- base: 0 + 0 = 0
  | succ k ih =>                       -- step: ih : 0 + k = k
    rw [Nat.add_succ]                  -- 0 + (k + 1) = (0 + k) + 1
    rw [ih]                            -- (0 + k) + 1 = k + 1

-- ============================================================
-- 3. 加法の結合法則
-- ============================================================

-- (a + b) + c = a + (b + c)
-- omega で一発で証明可能
example (a b c : Nat) : (a + b) + c = a + (b + c) := by omega

-- 帰納法で手動証明する場合
theorem my_add_assoc (a b c : Nat) : (a + b) + c = a + (b + c) := by
  induction c with
  | zero => rfl                        -- (a + b) + 0 = a + (b + 0)
  | succ k ih =>                       -- ih : (a + b) + k = a + (b + k)
    -- ゴール: (a + b) + (k + 1) = a + (b + (k + 1))
    -- succ を展開して ih を使う
    simp only [Nat.add_succ, ih]

-- ============================================================
-- 4. 加法の交換法則
-- ============================================================

-- omega で一発で証明可能
example (a b : Nat) : a + b = b + a := by omega

-- 帰納法で手動証明する場合
theorem my_add_comm (a b : Nat) : a + b = b + a := by
  induction b with
  | zero =>
    -- ゴール: a + 0 = 0 + a
    omega
  | succ k ih =>
    -- ih : a + k = k + a
    -- ゴール: a + (k + 1) = (k + 1) + a
    rw [Nat.add_succ, Nat.succ_add, ih]

-- ============================================================
-- 5. 乗法の基本性質
-- ============================================================

-- 0 * n = 0
example (n : Nat) : 0 * n = n * 0 := by
  simp

-- 分配法則: a * (b + c) = a * b + a * c
example (a b c : Nat) : a * (b + c) = a * b + a * c := by
  ring

-- 乗法の交換法則
example (a b : Nat) : a * b = b * a := by
  ring

-- 乗法の結合法則
example (a b c : Nat) : (a * b) * c = a * (b * c) := by
  ring

-- ============================================================
-- 6. 不等式の証明
-- ============================================================

-- n ≤ n（反射律）
example (n : Nat) : n ≤ n := by
  omega

-- n ≤ n + 1
example (n : Nat) : n ≤ n + 1 := by
  omega

-- 推移律
example (a b c : Nat) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  omega

-- ============================================================
-- 7. 帰納法の応用
-- ============================================================

-- n + n = 2 * n（帰納法で証明）
theorem double_eq_two_mul (n : Nat) : n + n = 2 * n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    -- ih : k + k = 2 * k
    -- ゴール: (k + 1) + (k + 1) = 2 * (k + 1)
    omega

-- 0 は任意の自然数以下: 0 ≤ n（帰納法で証明）
theorem my_zero_le (n : Nat) : 0 ≤ n := by
  induction n with
  | zero => omega
  | succ k _ih => omega

-- ============================================================
-- 8. 偶数・奇数
-- ============================================================

-- 偶数の定義を使った証明
example : Even 4 := ⟨2, by ring⟩

example : Odd 5 := ⟨2, by ring⟩

-- 偶数 + 偶数 = 偶数
theorem even_add_even (a b : Nat) (ha : Even a) (hb : Even b) : Even (a + b) := by
  obtain ⟨k, hk⟩ := ha
  obtain ⟨l, hl⟩ := hb
  exact ⟨k + l, by omega⟩
