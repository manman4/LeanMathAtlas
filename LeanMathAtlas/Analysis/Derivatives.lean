import Mathlib.Tactic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

/-!
# Derivatives

Differentiation rules (`HasDerivAt`) and their applications.

`HasDerivAt f f' a` means "f is differentiable at a and f'(a) = f'".

**Requires**: `ℝ`, `HasDerivAt`
**Tags**: Analysis, Calculus
-/

open Real

-- ============================================================
-- 1. 基本的な導関数
-- ============================================================

-- 定数関数の導関数は 0
theorem my_hasDerivAt_const (a c : ℝ) : HasDerivAt (fun _ => c) 0 a :=
  hasDerivAt_const a c

-- 恒等関数の導関数は 1
theorem my_hasDerivAt_id (a : ℝ) : HasDerivAt id 1 a :=
  hasDerivAt_id a

-- x^n の導関数は n * x^(n-1)
theorem my_hasDerivAt_pow (n : ℕ) (a : ℝ) :
    HasDerivAt (fun x => x ^ n) (↑n * a ^ (n - 1)) a :=
  hasDerivAt_pow n a

-- x^2 の導関数は 2x
theorem deriv_sq (a : ℝ) : HasDerivAt (fun x => x ^ 2) (2 * a) a := by
  simpa using hasDerivAt_pow 2 a

-- x^3 の導関数は 3x²
theorem deriv_cube (a : ℝ) : HasDerivAt (fun x => x ^ 3) (3 * a ^ 2) a := by
  simpa using hasDerivAt_pow 3 a

-- ============================================================
-- 2. 微分の法則
-- ============================================================

-- 和の微分: (f + g)' = f' + g'
theorem my_deriv_add {f g : ℝ → ℝ} {f' g' a : ℝ}
    (hf : HasDerivAt f f' a) (hg : HasDerivAt g g' a) :
    HasDerivAt (fun x => f x + g x) (f' + g') a :=
  hf.add hg

-- 定数倍の微分: (c * f)' = c * f'
theorem my_deriv_const_mul {f : ℝ → ℝ} {f' a c : ℝ}
    (hf : HasDerivAt f f' a) :
    HasDerivAt (fun x => c * f x) (c * f') a :=
  hf.const_mul c

-- 積の微分: (f * g)' = f' * g + f * g'
theorem my_deriv_mul {f g : ℝ → ℝ} {f' g' a : ℝ}
    (hf : HasDerivAt f f' a) (hg : HasDerivAt g g' a) :
    HasDerivAt (fun x => f x * g x) (f' * g a + f a * g') a :=
  hf.mul hg

-- 合成関数の微分（連鎖律）: (g ∘ f)' = g'(f(a)) * f'(a)
theorem my_deriv_comp {f g : ℝ → ℝ} {f' g' a : ℝ}
    (hg : HasDerivAt g g' (f a)) (hf : HasDerivAt f f' a) :
    HasDerivAt (g ∘ f) (g' * f') a :=
  hg.comp a hf

-- ============================================================
-- 3. 具体的な応用例
-- ============================================================

-- d/dx [x² + 3x + 1] = 2x + 3
theorem deriv_quadratic (a : ℝ) :
    HasDerivAt (fun x => x ^ 2 + 3 * x + 1) (2 * a + 3) a := by
  have h1 : HasDerivAt (fun x => x ^ 2) (2 * a) a  := by simpa using hasDerivAt_pow 2 a
  have h2 : HasDerivAt (fun x => 3 * x) (3 * 1) a  := (hasDerivAt_id a).const_mul 3
  have h3 : HasDerivAt (fun _ => (1 : ℝ)) 0 a       := hasDerivAt_const a 1
  have h4 := h1.add h2
  have h5 := h4.add h3
  convert h5 using 1; ring

-- d/dx [x * (x + 1)] = 2x + 1
theorem deriv_product_example (a : ℝ) :
    HasDerivAt (fun x => x * (x + 1)) (2 * a + 1) a := by
  have hf := hasDerivAt_id a
  have hg : HasDerivAt (fun x => x + 1) 1 a := by
    have h := hf.add (hasDerivAt_const a 1)
    convert h using 1; norm_num
  have h := hf.mul hg
  convert h using 1; simp; ring

-- ============================================================
-- 4. 三角関数の導関数
-- ============================================================

-- d/dx [sin x] = cos x
theorem deriv_sin' (a : ℝ) : HasDerivAt Real.sin (Real.cos a) a :=
  Real.hasDerivAt_sin a

-- d/dx [cos x] = -sin x
theorem deriv_cos' (a : ℝ) : HasDerivAt Real.cos (-Real.sin a) a :=
  Real.hasDerivAt_cos a

-- d/dx [sin(2x)] = 2 * cos(2x)（連鎖律の使用例）
theorem deriv_sin_double (a : ℝ) :
    HasDerivAt (fun x => Real.sin (2 * x)) (2 * Real.cos (2 * a)) a := by
  have hf : HasDerivAt (fun x => 2 * x) 2 a :=
    by simpa using (hasDerivAt_id a).const_mul 2
  have hg : HasDerivAt Real.sin (Real.cos (2 * a)) (2 * a) :=
    Real.hasDerivAt_sin (2 * a)
  have h := hg.comp a hf
  convert h using 1
  ring

-- d/dx [sin x * cos x] = cos²x - sin²x
theorem deriv_sin_cos (a : ℝ) :
    HasDerivAt (fun x => Real.sin x * Real.cos x) (Real.cos a ^ 2 - Real.sin a ^ 2) a := by
  have hf := Real.hasDerivAt_sin a
  have hg := Real.hasDerivAt_cos a
  have h  := hf.mul hg
  convert h using 1; ring
