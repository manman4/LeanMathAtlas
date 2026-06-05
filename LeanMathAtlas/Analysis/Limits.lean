import Mathlib.Tactic
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# Limits and Continuity

Two equivalent approaches to limits in ℝ:
- **ε-δ** (`∀ ε > 0, ∃ δ > 0, |x - a| < δ → |f x - b| < ε`)
- **Filter** (`Filter.Tendsto f (𝓝 a) (𝓝 b)`)

**Requires**: `ℝ`, `Filter`, `𝓝` (neighbourhood filter), `ContinuousAt`
**Tags**: Analysis, Topology
-/

open Filter Topology

-- ============================================================
-- 1. ε-δ と Filter.Tendsto の等価性
-- ============================================================

-- Filter.Tendsto を ε-δ で言い換える
theorem tendsto_iff_eps_delta (f : ℝ → ℝ) (a b : ℝ) :
    Tendsto f (𝓝 a) (𝓝 b) ↔
    ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε := by
  simp [Metric.tendsto_nhds_nhds, Real.dist_eq]

-- ε-δ から Filter.Tendsto を構成する
theorem tendsto_of_eps_delta {f : ℝ → ℝ} {a b : ℝ}
    (h : ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε) :
    Tendsto f (𝓝 a) (𝓝 b) :=
  (tendsto_iff_eps_delta f a b).mpr h

-- ============================================================
-- 2. 基本的な極限
-- ============================================================

-- 定数関数の極限: lim_{x→a} c = c
theorem my_tendsto_const (a c : ℝ) : Tendsto (fun _ => c) (𝓝 a) (𝓝 c) :=
  tendsto_const_nhds

-- 恒等関数の極限: lim_{x→a} x = a
theorem my_tendsto_id (a : ℝ) : Tendsto id (𝓝 a) (𝓝 a) :=
  tendsto_id

-- 線形関数の極限: lim_{x→a} (m*x + b) = m*a + b
theorem tendsto_linear (m b a : ℝ) :
    Tendsto (fun x => m * x + b) (𝓝 a) (𝓝 (m * a + b)) :=
  ((continuous_const.mul continuous_id').add continuous_const).continuousAt

-- x² の極限: lim_{x→a} x² = a²
theorem tendsto_sq (a : ℝ) : Tendsto (fun x => x ^ 2) (𝓝 a) (𝓝 (a ^ 2)) :=
  (continuous_pow 2).continuousAt

-- ============================================================
-- 3. 極限の演算法則
-- ============================================================

-- 和の極限: lim f + lim g
theorem my_tendsto_add {f g : ℝ → ℝ} {a b c : ℝ}
    (hf : Tendsto f (𝓝 a) (𝓝 b)) (hg : Tendsto g (𝓝 a) (𝓝 c)) :
    Tendsto (fun x => f x + g x) (𝓝 a) (𝓝 (b + c)) :=
  hf.add hg

-- 定数倍の極限: lim (c * f)
theorem my_tendsto_const_mul {f : ℝ → ℝ} {a b : ℝ} (c : ℝ)
    (hf : Tendsto f (𝓝 a) (𝓝 b)) :
    Tendsto (fun x => c * f x) (𝓝 a) (𝓝 (c * b)) :=
  hf.const_mul c

-- 積の極限: lim f * lim g
theorem my_tendsto_mul {f g : ℝ → ℝ} {a b c : ℝ}
    (hf : Tendsto f (𝓝 a) (𝓝 b)) (hg : Tendsto g (𝓝 a) (𝓝 c)) :
    Tendsto (fun x => f x * g x) (𝓝 a) (𝓝 (b * c)) :=
  hf.mul hg

-- 合成関数の極限（連鎖律）
theorem my_tendsto_comp {f g : ℝ → ℝ} {a b c : ℝ}
    (hg : Tendsto g (𝓝 b) (𝓝 c)) (hf : Tendsto f (𝓝 a) (𝓝 b)) :
    Tendsto (g ∘ f) (𝓝 a) (𝓝 c) :=
  hg.comp hf

-- ============================================================
-- 4. 連続性
-- ============================================================

-- ContinuousAt の定義: f が a で連続 ↔ lim_{x→a} f x = f a
theorem continuousAt_iff_tendsto (f : ℝ → ℝ) (a : ℝ) :
    ContinuousAt f a ↔ Tendsto f (𝓝 a) (𝓝 (f a)) :=
  Iff.rfl

-- 多項式は連続
theorem continuous_poly (a : ℝ) :
    ContinuousAt (fun x => x ^ 2 + 3 * x + 1) a :=
  ((continuous_pow 2).add (continuous_const.mul continuous_id')).add
    continuous_const |>.continuousAt

-- ============================================================
-- 5. はさみうちの定理 (Squeeze theorem)
-- ============================================================

-- g(x) ≤ f(x) ≤ h(x) が a の近傍で成り立ち lim g = lim h = L → lim f = L
theorem squeeze_tendsto {f g h : ℝ → ℝ} {a L : ℝ}
    (hg : Tendsto g (𝓝 a) (𝓝 L))
    (hh : Tendsto h (𝓝 a) (𝓝 L))
    (hfg : ∀ᶠ x in 𝓝 a, g x ≤ f x)
    (hfh : ∀ᶠ x in 𝓝 a, f x ≤ h x) :
    Tendsto f (𝓝 a) (𝓝 L) :=
  tendsto_of_tendsto_of_tendsto_of_le_of_le' hg hh hfg hfh

-- ============================================================
-- 6. 具体例
-- ============================================================

-- lim_{x→2} (3x + 1) = 7
example : Tendsto (fun x : ℝ => 3 * x + 1) (𝓝 2) (𝓝 7) := by
  have h := tendsto_linear 3 1 2; norm_num at h; exact h

-- lim_{x→3} x² = 9
example : Tendsto (fun x : ℝ => x ^ 2) (𝓝 3) (𝓝 9) := by
  have h := tendsto_sq 3; norm_num at h; exact h
