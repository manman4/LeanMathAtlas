import Mathlib.Tactic

/-!
# Primes and Divisibility

Prime numbers, GCD, coprimality, and Euclid's theorem that primes are infinite.

**Requires**: `ℕ`, `Nat.Prime`, `Nat.gcd`, `Nat.Coprime`
**Tags**: NumberTheory, Primes
-/

-- ============================================================
-- 1. 素数の例 (Concrete prime examples)
-- ============================================================

-- decide タクティクは有限の計算を自動実行する
theorem two_prime   : Nat.Prime 2 := by decide
theorem three_prime : Nat.Prime 3 := by decide
theorem five_prime  : Nat.Prime 5 := by decide
theorem seven_prime : Nat.Prime 7 := by decide

-- 1 は素数でない
example : ¬ Nat.Prime 1 := by decide

-- 4 は素数でない（2 × 2）
example : ¬ Nat.Prime 4 := by decide

-- ============================================================
-- 2. 素数の基本性質
-- ============================================================

-- すべての素数は 2 以上
theorem prime_ge_two (p : ℕ) (hp : Nat.Prime p) : 2 ≤ p :=
  hp.two_le

-- 素数 p の約数は 1 と p だけ
theorem prime_divisors (p : ℕ) (hp : Nat.Prime p) (k : ℕ) (hk : k ∣ p) :
    k = 1 ∨ k = p :=
  hp.eq_one_or_self_of_dvd k hk

-- 素数は奇数か 2（2 以外の偶数は素数でない）
theorem prime_odd_or_two (p : ℕ) (hp : Nat.Prime p) (hne : p ≠ 2) : p % 2 = 1 := by
  rcases hp.eq_two_or_odd with rfl | h
  · exact absurd rfl hne
  · exact h

-- ============================================================
-- 3. 最大公約数 (GCD)
-- ============================================================

-- gcd は両方を割り切る
theorem my_gcd_dvd_left  (a b : ℕ) : Nat.gcd a b ∣ a := Nat.gcd_dvd_left  a b
theorem my_gcd_dvd_right (a b : ℕ) : Nat.gcd a b ∣ b := Nat.gcd_dvd_right a b

-- 公約数の中で最大（任意の公約数は gcd を割り切る）
theorem my_dvd_gcd {k a b : ℕ} (ha : k ∣ a) (hb : k ∣ b) : k ∣ Nat.gcd a b :=
  Nat.dvd_gcd ha hb

-- 交換法則
theorem my_gcd_comm (a b : ℕ) : Nat.gcd a b = Nat.gcd b a := Nat.gcd_comm a b

-- 特殊値
theorem my_gcd_zero_right (a : ℕ) : Nat.gcd a 0 = a := Nat.gcd_zero_right a
theorem my_gcd_zero_left  (a : ℕ) : Nat.gcd 0 a = a := Nat.gcd_zero_left  a
theorem my_gcd_self       (a : ℕ) : Nat.gcd a a = a := Nat.gcd_self a

-- gcd の計算例
#eval Nat.gcd 12 18   -- 6
#eval Nat.gcd 35 49   -- 7
#eval Nat.gcd 100 75  -- 25

-- ============================================================
-- 4. 互いに素 (Coprimality)
-- ============================================================

-- 定義: gcd(a, b) = 1
example (a b : ℕ) : Nat.Coprime a b ↔ Nat.gcd a b = 1 := Iff.rfl

-- 連続する自然数は互いに素
-- 証明の核心: gcd(n, n+1) | (n+1) - n = 1
theorem coprime_succ (n : ℕ) : Nat.Coprime n (n + 1) := by
  show Nat.gcd n (n + 1) = 1
  have h1 : Nat.gcd n (n + 1) ∣ n     := Nat.gcd_dvd_left  n (n + 1)
  have h2 : Nat.gcd n (n + 1) ∣ n + 1 := Nat.gcd_dvd_right n (n + 1)
  have h3 : Nat.gcd n (n + 1) ∣ 1     := by simpa using Nat.dvd_sub' h2 h1
  exact Nat.dvd_one.mp h3

-- 素数 p が a を割り切らないなら p と a は互いに素
theorem prime_coprime_of_not_dvd {p n : ℕ} (hp : Nat.Prime p) (h : ¬ p ∣ n) :
    Nat.Coprime p n :=
  hp.coprime_iff_not_dvd.mpr h

-- 互いに素なら積が割り切る条件（Gauss の補題）
theorem coprime_dvd_of_dvd_mul {k m n : ℕ}
    (hco : Nat.Coprime k n) (h : k ∣ m * n) : k ∣ m :=
  Nat.Coprime.dvd_of_dvd_mul_right hco h

-- ============================================================
-- 5. 素数は無限個存在する（ユークリッド）
-- ============================================================

-- 任意の n に対して n 以上の素数が存在する
theorem exists_prime_ge (n : ℕ) : ∃ p, n ≤ p ∧ Nat.Prime p :=
  Nat.exists_infinite_primes n
