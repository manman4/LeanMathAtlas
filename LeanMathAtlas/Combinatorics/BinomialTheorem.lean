import Mathlib.Tactic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Nat.Choose.Sum

/-!
# Binomial Theorem

Properties of `Nat.choose`, Pascal's triangle, and the binomial theorem
`(a + b)^n = Σ C(n,k) aᵏ b^(n-k)`.

**Requires**: `ℕ`, `Nat.choose`, `Finset`
**Tags**: Combinatorics, Algebra
-/

open BigOperators Finset

-- ============================================================
-- 1. 組み合わせの基本性質 (数A)
-- ============================================================

-- nC0 = 1
theorem choose_zero (n : ℕ) : n.choose 0 = 1 := Nat.choose_zero_right n

-- nCn = 1
theorem choose_self (n : ℕ) : n.choose n = 1 := Nat.choose_self n

-- nC1 = n
theorem choose_one (n : ℕ) : n.choose 1 = n := Nat.choose_one_right n

-- nCk = nC(n-k)（対称性）
theorem choose_symm (n k : ℕ) (h : k ≤ n) : n.choose k = n.choose (n - k) :=
  (Nat.choose_symm h).symm

-- パスカルの三角形: nCk + nC(k+1) = (n+1)C(k+1)
theorem pascal (n k : ℕ) : n.choose k + n.choose (k + 1) = (n + 1).choose (k + 1) :=
  (Nat.choose_succ_succ n k).symm

-- ============================================================
-- 2. 二項定理 (数II)
--    (a + b)^n = Σ_{k=0}^{n} nCk * a^k * b^(n-k)
-- ============================================================

theorem binomial_theorem (a b : ℝ) (n : ℕ) :
    (a + b) ^ n = ∑ k ∈ range (n + 1), a ^ k * b ^ (n - k) * (n.choose k : ℝ) :=
  add_pow a b n

-- ============================================================
-- 3. 二項定理の系 (数II)
-- ============================================================

-- Σ_{k=0}^{n} nCk = 2^n  （a = b = 1 を代入）
theorem sum_choose_eq_pow2 (n : ℕ) :
    ∑ k ∈ range (n + 1), n.choose k = 2 ^ n :=
  Nat.sum_range_choose n

-- Σ_{k=0}^{n} (-1)^k * nCk = 0  （a = -1, b = 1 を代入）
theorem alternating_sum_choose (n : ℕ) (hn : 0 < n) :
    ∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * n.choose k = 0 := by
  have h : ((-1 : ℤ) + 1) ^ n =
      ∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * (n.choose k : ℤ) := by
    have := add_pow (-1 : ℤ) 1 n
    simp only [one_pow, mul_one] at this
    push_cast at this ⊢
    linarith
  rw [show (-1 : ℤ) + 1 = 0 from by norm_num,
      zero_pow (Nat.pos_iff_ne_zero.mp hn)] at h
  linarith
