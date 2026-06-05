import Mathlib.Tactic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

/-!
# Integration: Interval Integrals and the Fundamental Theorem of Calculus

Working with `intervalIntegral` (written `∫ x in a..b, f x`) and the
Fundamental Theorem of Calculus.

**Requires**: `MeasureTheory`, `intervalIntegral`, `HasDerivAt`
**Tags**: Analysis, Integration, FundamentalTheorem
-/

open MeasureTheory

-- ============================================================
-- 1. 区間積分の基本性質 (Basic Properties of Interval Integrals)
-- ============================================================

-- 定数関数の積分: ∫ c dx = (b - a) * c
theorem my_integral_const (a b c : ℝ) :
    ∫ _ in a..b, c = (b - a) * c := by
  rw [intervalIntegral.integral_const, smul_eq_mul]

-- 積分の方向を逆にすると符号が変わる
theorem my_integral_symm (f : ℝ → ℝ) (a b : ℝ) :
    ∫ x in b..a, f x = -∫ x in a..b, f x :=
  intervalIntegral.integral_symm a b

-- 積分の加法性 (linearity: addition)
theorem my_integral_add (f g : ℝ → ℝ) (a b : ℝ)
    (hf : IntervalIntegrable f volume a b) (hg : IntervalIntegrable g volume a b) :
    ∫ x in a..b, (f x + g x) = (∫ x in a..b, f x) + ∫ x in a..b, g x :=
  intervalIntegral.integral_add hf hg

-- 積分の減法性 (linearity: subtraction)
theorem my_integral_sub (f g : ℝ → ℝ) (a b : ℝ)
    (hf : IntervalIntegrable f volume a b) (hg : IntervalIntegrable g volume a b) :
    ∫ x in a..b, (f x - g x) = (∫ x in a..b, f x) - ∫ x in a..b, g x :=
  intervalIntegral.integral_sub hf hg

-- スカラー倍: ∫ c • f dx = c • ∫ f dx
theorem my_integral_smul (f : ℝ → ℝ) (c : ℝ) (a b : ℝ) :
    ∫ x in a..b, c • f x = c • ∫ x in a..b, f x :=
  intervalIntegral.integral_smul c (fun x => f x)

-- 積分の区間分割: ∫[a,b] + ∫[b,c] = ∫[a,c]
theorem my_integral_add_adjacent (f : ℝ → ℝ) (a b c : ℝ)
    (hab : IntervalIntegrable f volume a b) (hbc : IntervalIntegrable f volume b c) :
    (∫ x in a..b, f x) + ∫ x in b..c, f x = ∫ x in a..c, f x :=
  intervalIntegral.integral_add_adjacent_intervals hab hbc

-- ============================================================
-- 2. 積分可能性 (Integrability)
-- ============================================================

-- 連続関数は区間積分可能
theorem my_continuous_intervalIntegrable (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) :
    IntervalIntegrable f volume a b :=
  hf.intervalIntegrable a b

-- ============================================================
-- 3. 微積分の基本定理 (Fundamental Theorem of Calculus)
-- ============================================================

-- 微積分の基本定理・第2部 (FTC Part 2):
-- F の導関数が f ならば ∫[a,b] f = F(b) - F(a)
theorem my_ftc2 (F f : ℝ → ℝ) (a b : ℝ)
    (hderiv : ∀ x ∈ Set.uIcc a b, HasDerivAt F (f x) x)
    (hint : IntervalIntegrable f volume a b) :
    ∫ x in a..b, f x = F b - F a :=
  intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint

-- 微積分の基本定理・第1部 (FTC Part 1):
-- 連続な f に対し d/dx ∫[a,x] f(t) dt = f(x)
theorem my_ftc1 (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) :
    deriv (fun u => ∫ x in a..u, f x) b = f b :=
  Continuous.deriv_integral f hf a b

-- ============================================================
-- 4. 具体例 (Concrete Examples)
-- ============================================================

-- ∫[0,1] x dx = 1/2  (原始関数: x²/2)
example : ∫ x in (0:ℝ)..1, x = 1/2 := by
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun x => x^2 / 2) (f' := fun x => x)
    (a := (0:ℝ)) (b := 1)
    (fun x _ => by
      have := (hasDerivAt_pow 2 x).div_const (2:ℝ)
      simp at this; exact this)
    (continuous_id.intervalIntegrable _ _)
  simp at h; linarith

-- ∫[0,1] x² dx = 1/3  (原始関数: x³/3)
example : ∫ x in (0:ℝ)..1, x^2 = 1/3 := by
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun x => x^3 / 3) (f' := fun x => x^2)
    (a := (0:ℝ)) (b := 1)
    (fun x _ => by
      have := (hasDerivAt_pow 3 x).div_const (3:ℝ)
      simp at this; exact this)
    ((continuous_pow 2).intervalIntegrable _ _)
  simp at h; linarith

-- ∫[0,π] sin x dx = 2  (原始関数: -cos x)
-- なぜなら (-cos x)' = sin x, cos 0 = 1, cos π = -1
example : ∫ x in (0:ℝ)..Real.pi, Real.sin x = 2 := by
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun x => -Real.cos x) (f' := Real.sin)
    (a := (0:ℝ)) (b := Real.pi)
    (fun x _ => by have hd := (Real.hasDerivAt_cos x).neg; simp at hd; exact hd)
    (Real.continuous_sin.intervalIntegrable _ _)
  simp [Real.cos_zero, Real.cos_pi] at h; linarith

-- ∫[0,1] eˣ dx = e - 1  (原始関数: exp x)
-- なぜなら (exp x)' = exp x, exp 0 = 1
example : ∫ x in (0:ℝ)..1, Real.exp x = Real.exp 1 - 1 := by
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := Real.exp) (f' := Real.exp)
    (a := (0:ℝ)) (b := 1)
    (fun x _ => Real.hasDerivAt_exp x)
    (Real.continuous_exp.intervalIntegrable _ _)
  simp [Real.exp_zero] at h; linarith
