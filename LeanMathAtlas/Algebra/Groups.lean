import Mathlib.Tactic
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.GroupTheory.Coset.Card
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Data.ZMod.Basic

/-!
# Group Theory: Groups, Subgroups, and Lagrange's Theorem

Working with the `Group` typeclass: basic laws, subgroups, and Lagrange's theorem.

**Requires**: `Group`, `Subgroup`, `orderOf`, `Fintype`
**Tags**: Algebra, GroupTheory
-/

variable {G : Type*} [Group G]

-- ============================================================
-- 1. 群の基本法則
-- ============================================================

-- 右単位元: a * 1 = a
theorem my_mul_one (a : G) : a * 1 = a := mul_one a

-- 左単位元: 1 * a = a
theorem my_one_mul (a : G) : 1 * a = a := one_mul a

-- 右逆元: a * a⁻¹ = 1
theorem my_mul_inv_cancel (a : G) : a * a⁻¹ = 1 := mul_inv_cancel a

-- 左逆元: a⁻¹ * a = 1
theorem my_inv_mul_cancel (a : G) : a⁻¹ * a = 1 := inv_mul_cancel a

-- 逆元の逆元: (a⁻¹)⁻¹ = a
theorem my_inv_inv (a : G) : a⁻¹⁻¹ = a := inv_inv a

-- 積の逆元: (a * b)⁻¹ = b⁻¹ * a⁻¹
theorem my_mul_inv_rev (a b : G) : (a * b)⁻¹ = b⁻¹ * a⁻¹ := mul_inv_rev a b

-- 左消去法則: a * b = a * c → b = c
theorem my_mul_left_cancel {a b c : G} (h : a * b = a * c) : b = c :=
  mul_left_cancel h

-- 右消去法則: a * b = c * b → a = c
theorem my_mul_right_cancel {a b c : G} (h : a * b = c * b) : a = c :=
  mul_right_cancel h

-- 単位元の一意性: 左単位元は必ず 1 に等しい
theorem my_one_unique {e : G} (h : ∀ a : G, e * a = a) : e = 1 := by
  have := h 1; rwa [mul_one] at this

-- 方程式 a * x = b の解: x = a⁻¹ * b
theorem my_eq_inv_mul_of_mul_eq {a b c : G} (h : a * b = c) : b = a⁻¹ * c := by
  rw [← h]; group

-- ============================================================
-- 2. 部分群 (Subgroup)
-- ============================================================

-- 部分群は単位元を含む
theorem my_subgroup_one (H : Subgroup G) : (1 : G) ∈ H :=
  H.one_mem

-- 部分群は積について閉じている
theorem my_subgroup_mul {H : Subgroup G} {a b : G}
    (ha : a ∈ H) (hb : b ∈ H) : a * b ∈ H :=
  H.mul_mem ha hb

-- 部分群は逆元について閉じている
theorem my_subgroup_inv {H : Subgroup G} {a : G} (ha : a ∈ H) : a⁻¹ ∈ H :=
  H.inv_mem ha

-- 自明な部分群: 全体群 ⊤ と 単位元のみの群 ⊥
example (H : Subgroup G) : H ≤ ⊤ := le_top
example (H : Subgroup G) : ⊥ ≤ H := bot_le

-- 共通部分も部分群: a ∈ H ∧ a ∈ K → a ∈ H ⊓ K
theorem my_subgroup_inter {H K : Subgroup G} {a : G} (ha : a ∈ H) (hb : a ∈ K) :
    a ∈ H ⊓ K :=
  ⟨ha, hb⟩

-- ============================================================
-- 3. ラグランジュの定理
--    有限群 G の部分群 H の位数は |G| を割り切る: |H| ∣ |G|
-- ============================================================

-- Nat.card を使った一般形
theorem lagrange (H : Subgroup G) : Nat.card H ∣ Nat.card G :=
  H.card_subgroup_dvd_card

-- 指数との関係: |H| * [G:H] = |G|
-- (index H = [G:H] は左剰余類の個数)
theorem lagrange_index (H : Subgroup G) : Nat.card H * H.index = Nat.card G :=
  H.card_mul_index

-- ============================================================
-- 4. 元の位数 (Order of Elements)
-- ============================================================

-- a^(orderOf a) = 1
theorem my_pow_orderOf_eq_one (a : G) : a ^ orderOf a = 1 :=
  pow_orderOf_eq_one a

-- orderOf a は a^n = 1 を満たす正の整数を割り切る
theorem my_orderOf_dvd_of_pow_eq_one {a : G} {n : ℕ} (h : a ^ n = 1) :
    orderOf a ∣ n :=
  orderOf_dvd_of_pow_eq_one h

-- 有限群では元の位数が |G| を割り切る（ラグランジュの系）
theorem my_orderOf_dvd_card [Fintype G] (a : G) :
    orderOf a ∣ Fintype.card G :=
  orderOf_dvd_card

-- 有限群では a^|G| = 1
theorem my_pow_card_eq_one [Fintype G] (a : G) :
    a ^ Fintype.card G = 1 :=
  pow_card_eq_one

-- ============================================================
-- 5. 具体例
-- ============================================================

-- ZMod 6: 加法巡回群, 位数 6
example : Fintype.card (ZMod 6) = 6 := by decide

-- S₃ = 3 文字の置換群, 位数 = 6
example : Fintype.card (Equiv.Perm (Fin 3)) = 6 := by decide

-- ZMod 6 の加法位数: addOrderOf (a : ZMod n) = n / gcd(n, a)
-- 1 は生成元: addOrderOf 1 = 6
example : addOrderOf (1 : ZMod 6) = 6 := ZMod.addOrderOf_one 6

-- addOrderOf 2 = 6 / gcd(6, 2) = 6 / 2 = 3
example : addOrderOf (2 : ZMod 6) = 3 := by
  rw [show (2 : ZMod 6) = ((2 : ℕ) : ZMod 6) from rfl,
      ZMod.addOrderOf_coe 2 (by norm_num)]
  norm_num

-- addOrderOf 3 = 6 / gcd(6, 3) = 6 / 3 = 2
example : addOrderOf (3 : ZMod 6) = 2 := by
  rw [show (3 : ZMod 6) = ((3 : ℕ) : ZMod 6) from rfl,
      ZMod.addOrderOf_coe 3 (by norm_num)]
  norm_num

-- ラグランジュの系の確認: addOrderOf a ∣ |G|
-- addOrderOf 2 = 3, |ZMod 6| = 6, 3 ∣ 6 ✓
example : addOrderOf (2 : ZMod 6) ∣ Fintype.card (ZMod 6) := addOrderOf_dvd_card
