import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic
import Mathlib.FieldTheory.Finite.Basic

/-!
# Modular Arithmetic

Arithmetic in `ZMod n` and Fermat's little theorem.

`ZMod n` is the type of integers modulo n (i.e. ℤ/nℤ).

**Requires**: `ZMod`, `Nat.Prime`, `Fact`
**Tags**: NumberTheory
-/

-- ============================================================
-- 1. ZMod の基本 (数A・数論)
-- ============================================================

-- n ≡ 0 (mod n)
theorem zmod_self (n : ℕ) : (n : ZMod n) = 0 :=
  ZMod.natCast_self n

-- ZMod の加法
example : (3 : ZMod 5) + 4 = 2 := by decide

-- ZMod の乗法
example : (3 : ZMod 5) * 4 = 2 := by decide

-- ZMod の冪
example : (2 : ZMod 7) ^ 3 = 1 := by decide

-- ============================================================
-- 2. 合同式の基本性質
-- ============================================================

-- a ≡ b (mod n) ↔ n ∣ (b - a)
theorem cong_iff_dvd (a b : ℤ) (n : ℕ) :
    (a : ZMod n) = b ↔ (n : ℤ) ∣ b - a := by
  rw [ZMod.intCast_eq_intCast_iff]
  exact Int.modEq_iff_dvd

-- 加法の合同: a ≡ b → a + c ≡ b + c (mod n)
theorem cong_add {n : ℕ} {a b : ZMod n} (h : a = b) (c : ZMod n) :
    a + c = b + c := by rw [h]

-- 乗法の合同: a ≡ b → a * c ≡ b * c (mod n)
theorem cong_mul {n : ℕ} {a b : ZMod n} (h : a = b) (c : ZMod n) :
    a * c = b * c := by rw [h]

-- ============================================================
-- 3. 素数 mod での性質
-- ============================================================

-- p が素数のとき ZMod p は体（Field）
-- Mathlib: [Fact (Nat.Prime p)] → Field (ZMod p)
example (p : ℕ) [Fact (Nat.Prime p)] : Field (ZMod p) :=
  ZMod.instField p

-- ZMod p の非ゼロ元は可逆
theorem zmod_prime_inv {p : ℕ} [Fact (Nat.Prime p)]
    (a : ZMod p) (ha : a ≠ 0) : a * a⁻¹ = 1 :=
  mul_inv_cancel₀ ha

-- ============================================================
-- 4. フェルマーの小定理 (数A・整数論)
--    p が素数, a ≢ 0 (mod p) のとき a^(p-1) ≡ 1 (mod p)
-- ============================================================

theorem fermat_little {p : ℕ} [Fact (Nat.Prime p)]
    (a : ZMod p) (ha : a ≠ 0) : a ^ (p - 1) = 1 :=
  ZMod.pow_card_sub_one_eq_one ha

-- 系: a^p ≡ a (mod p)（すべての a に対して）
theorem fermat_little_all {p : ℕ} [hp : Fact (Nat.Prime p)]
    (a : ZMod p) : a ^ p = a := by
  have := hp.out
  by_cases ha : a = 0
  · simp [ha, zero_pow (Nat.Prime.ne_zero this)]
  · have h := fermat_little a ha
    have hp1 : p = p - 1 + 1 := (Nat.succ_pred_eq_of_pos this.pos).symm
    calc a ^ p = a ^ (p - 1 + 1) := by rw [← hp1]
      _ = a ^ (p - 1) * a      := pow_succ a (p - 1)
      _ = 1 * a                := by rw [h]
      _ = a                    := one_mul a

-- ============================================================
-- 5. 具体的な計算例
-- ============================================================

-- 2^4 ≡ 1 (mod 5)  （フェルマーの小定理: p=5, a=2）
example : (2 : ZMod 5) ^ 4 = 1 := by decide

-- 3^6 ≡ 1 (mod 7)  （フェルマーの小定理: p=7, a=3）
example : (3 : ZMod 7) ^ 6 = 1 := by decide

-- 7^10 ≡ 7 (mod 11)  （系: a^p ≡ a）
example : (7 : ZMod 11) ^ 11 = 7 := by decide
