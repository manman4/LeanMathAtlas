import Mathlib.Tactic
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# Inner Product Spaces, Norms, and Cauchy-Schwarz

Working with inner products and norms `‖x‖` in a real inner product space.

`inner x y` denotes the inner product ⟪x, y⟫ in ℝ.

**Requires**: `ℝ`, `InnerProductSpace`, `EuclideanSpace`
**Tags**: LinearAlgebra, Analysis
-/

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

set_option linter.unusedSectionVars false

-- ============================================================
-- 1. 内積の基本性質
-- ============================================================

-- 対称性: ⟪x, y⟫ = ⟪y, x⟫
theorem my_inner_comm (x y : E) :
    inner (𝕜 := ℝ) x y = inner (𝕜 := ℝ) y x :=
  (real_inner_comm x y).symm

-- 加法線形性: ⟪x + y, z⟫ = ⟪x, z⟫ + ⟪y, z⟫
theorem my_inner_add_left (x y z : E) :
    inner (𝕜 := ℝ) (x + y) z =
    inner (𝕜 := ℝ) x z + inner (𝕜 := ℝ) y z :=
  inner_add_left x y z

-- スカラー倍: ⟪c • x, y⟫ = c * ⟪x, y⟫
theorem my_inner_smul_left (c : ℝ) (x y : E) :
    inner (𝕜 := ℝ) (c • x) y = c * inner (𝕜 := ℝ) x y := by
  simp [inner_smul_left]

-- 正定値性: ⟪x, x⟫ ≥ 0
theorem my_inner_self_nonneg (x : E) : 0 ≤ inner (𝕜 := ℝ) x x :=
  real_inner_self_nonneg

-- ⟪x, x⟫ = 0 ↔ x = 0
theorem my_inner_self_eq_zero (x : E) :
    inner (𝕜 := ℝ) x x = 0 ↔ x = 0 :=
  inner_self_eq_zero

-- ⟪x, x⟫ = ‖x‖²
theorem my_inner_self_eq_norm_sq (x : E) :
    inner (𝕜 := ℝ) x x = ‖x‖ ^ 2 :=
  real_inner_self_eq_norm_sq x

-- ============================================================
-- 2. ノルムの基本性質
-- ============================================================

-- 非負性: ‖x‖ ≥ 0
theorem my_norm_nonneg (x : E) : 0 ≤ ‖x‖ :=
  norm_nonneg x

-- 正定値性: ‖x‖ = 0 ↔ x = 0
theorem my_norm_eq_zero (x : E) : ‖x‖ = 0 ↔ x = 0 :=
  norm_eq_zero

-- スカラー倍のノルム: ‖c • x‖ = |c| * ‖x‖
theorem my_norm_smul (c : ℝ) (x : E) : ‖c • x‖ = |c| * ‖x‖ :=
  norm_smul c x

-- 三角不等式: ‖x + y‖ ≤ ‖x‖ + ‖y‖
theorem my_norm_add_le (x y : E) : ‖x + y‖ ≤ ‖x‖ + ‖y‖ :=
  norm_add_le x y

-- ‖-x‖ = ‖x‖
theorem my_norm_neg (x : E) : ‖-x‖ = ‖x‖ :=
  norm_neg x

-- ============================================================
-- 3. コーシー・シュワルツの不等式
--    |⟪x, y⟫| ≤ ‖x‖ * ‖y‖
-- ============================================================

theorem cauchy_schwarz (x y : E) :
    |inner (𝕜 := ℝ) x y| ≤ ‖x‖ * ‖y‖ :=
  abs_real_inner_le_norm x y

-- 二乗形式: ⟪x, y⟫² ≤ ⟪x, x⟫ * ⟪y, y⟫
theorem cauchy_schwarz_sq (x y : E) :
    inner (𝕜 := ℝ) x y ^ 2 ≤
    inner (𝕜 := ℝ) x x * inner (𝕜 := ℝ) y y := by
  have h  := abs_real_inner_le_norm x y
  have hx := real_inner_self_eq_norm_sq x
  have hy := real_inner_self_eq_norm_sq y
  have hsq : inner (𝕜 := ℝ) x y ^ 2 ≤ (‖x‖ * ‖y‖) ^ 2 := by
    have := sq_abs (inner (𝕜 := ℝ) x y)
    nlinarith [abs_nonneg (inner (𝕜 := ℝ) x y)]
  nlinarith [mul_pow ‖x‖ ‖y‖ 2]

-- ============================================================
-- 4. ℝ² での具体例
-- ============================================================

noncomputable abbrev e₁ : EuclideanSpace ℝ (Fin 2) := EuclideanSpace.single 0 1
noncomputable abbrev e₂ : EuclideanSpace ℝ (Fin 2) := EuclideanSpace.single 1 1

-- e₁ と e₂ は直交
theorem e1_inner_e2 : inner (𝕜 := ℝ) e₁ e₂ = 0 := by
  simp [e₁, e₂, EuclideanSpace.inner_single_left]

-- ‖e₁‖ = 1
theorem norm_e1 : ‖e₁‖ = 1 := by
  simp [e₁, EuclideanSpace.norm_single]

-- ‖e₂‖ = 1
theorem norm_e2 : ‖e₂‖ = 1 := by
  simp [e₂, EuclideanSpace.norm_single]
