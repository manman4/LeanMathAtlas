import Mathlib.Tactic

/-!
# Sequences and Series

Arithmetic and geometric sequences as functions `ℕ → R`,
with closed-form summation formulas proved by induction.

**Requires**: `ℕ`, `ℤ`, `ℝ`, `Finset.range`, `BigOperators`
**Tags**: Algebra, NumberTheory
-/

open BigOperators

-- ============================================================
-- 1. 数列の基本
-- ============================================================

def squareSeq : ℕ → ℕ := fun n => n ^ 2

#eval squareSeq 5   -- 25

def oddSeq : ℕ → ℕ := fun n => 2 * n + 1

#eval List.map oddSeq [0, 1, 2, 3, 4]  -- [1, 3, 5, 7, 9]

-- ============================================================
-- 2. 等差数列 (Arithmetic Sequence)
--    a_n = a + n * d  （初項 a, 公差 d）
-- ============================================================

def arith (a d : ℤ) : ℕ → ℤ := fun n => a + n * d

-- 隣接する項の差は常に d
theorem arith_diff (a d : ℤ) (n : ℕ) :
    arith a d (n + 1) - arith a d n = d := by
  simp [arith]; ring

-- 初項の確認
theorem arith_zero (a d : ℤ) : arith a d 0 = a := by simp [arith]

-- ============================================================
-- 3. 等比数列 (Geometric Sequence)
--    a_n = a * r^n  （初項 a, 公比 r）
-- ============================================================

def geom (a r : ℝ) : ℕ → ℝ := fun n => a * r ^ n

-- 隣接する項の比は r（a ≠ 0, r ≠ 0 のとき）
theorem geom_ratio (a r : ℝ) (ha : a ≠ 0) (hr : r ≠ 0) (n : ℕ) :
    geom a r (n + 1) / geom a r n = r := by
  unfold geom
  rw [pow_succ, ← mul_assoc]
  exact mul_div_cancel_left₀ r (mul_ne_zero ha (pow_ne_zero _ hr))

-- ============================================================
-- 4. 数列の和：Σ の表記
--    Finset.sum を使って Σ_{i=0}^{n-1} f(i) を書く
-- ============================================================

#eval ∑ i ∈ Finset.range 5, i   -- 0+1+2+3+4 = 10

-- ============================================================
-- 5. 自然数の和の公式 (ガウスの公式)
--    2 * Σ_{k=0}^{n-1} k = n*(n-1)    （Mathlib から導出）
--    2 * Σ_{k=0}^{n} k   = n*(n+1)    （帰納法で証明）
-- ============================================================

-- Mathlib の定理: (∑ i ∈ Finset.range n, i) * 2 = n * (n - 1)
#check Finset.sum_range_id_mul_two

-- Mathlib の定理から omega で直接導出
theorem sum_range_eq (n : ℕ) :
    2 * ∑ k ∈ Finset.range n, k = n * (n - 1) := by
  have h := Finset.sum_range_id_mul_two n
  omega

-- 帰納法で独自証明（n+1 項版）
theorem my_gauss (n : ℕ) :
    2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1) := by
  induction n with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ]
    nlinarith

-- ============================================================
-- 6. 平方和の公式
--    6 * Σ_{k=0}^{n} k^2 = n*(n+1)*(2n+1)
-- ============================================================

theorem sum_sq (n : ℕ) :
    6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1) := by
  induction n with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ]
    nlinarith [ih]

-- ============================================================
-- 7. 等差数列の和
--    2 * Σ_{k=0}^{n-1} (a + k*d) = 2*n*a + d*n*(n-1)
-- ============================================================

theorem sum_arith (a d : ℤ) (n : ℕ) :
    2 * ∑ k ∈ Finset.range n, arith a d k = 2 * n * a + d * (n * (n - 1)) := by
  induction n with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, arith]
    push_cast
    linarith [ih]

-- ============================================================
-- 8. 等比数列の和（公比 r ≠ 1 のとき）
--    (r - 1) * Σ_{k=0}^{n-1} a*r^k = a*(r^n - 1)
-- ============================================================

theorem sum_geom (a r : ℝ) (n : ℕ) :
    (r - 1) * ∑ k ∈ Finset.range n, a * r ^ k = a * (r ^ n - 1) := by
  induction n with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, mul_add, ih]
    ring

-- 公比 r ≠ 1 のとき和の閉じた形
theorem sum_geom_div (a r : ℝ) (hr : r ≠ 1) (n : ℕ) :
    ∑ k ∈ Finset.range n, a * r ^ k = a * (r ^ n - 1) / (r - 1) := by
  have h : r - 1 ≠ 0 := sub_ne_zero.mpr hr
  field_simp [h]
  linear_combination sum_geom a r n

-- ============================================================
-- 9. 立方和の公式
--    4 * Σ_{k=0}^{n} k^3 = (n*(n+1))^2
--    （ガウスの公式の二乗に等しい）
-- ============================================================

theorem sum_cubes (n : ℕ) :
    4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2 := by
  induction n with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, mul_add, ih]
    ring
