# Integration Theory: Interval Integrals and the Fundamental Theorem of Calculus

> **日本語で読む →** [Integration.md](../../ja/Analysis/Integration.md)

Corresponding Lean file: `LeanMathAtlas/Analysis/Integration.lean`

## Contents

### Basic Properties of Interval Integrals

| Theorem Name | Statement |
|--------|------|
| `my_integral_const` | Integral of a constant function: ∫[a,b] c dx = (b-a) * c |
| `my_integral_symm` | Orientation of interval: ∫[b,a] f = -∫[a,b] f |
| `my_integral_add` | Additivity: ∫(f+g) = ∫f + ∫g |
| `my_integral_sub` | Subtractivity: ∫(f-g) = ∫f - ∫g |
| `my_integral_smul` | Scalar multiple: ∫ c•f = c • ∫f |
| `my_integral_add_adjacent` | Interval splitting: ∫[a,b] + ∫[b,c] = ∫[a,c] |

### Integrability

| Theorem Name | Statement |
|--------|------|
| `my_continuous_intervalIntegrable` | Continuous functions are interval-integrable |

### Fundamental Theorem of Calculus

| Theorem Name | Statement |
|--------|------|
| `my_ftc2` | Part 2: If F' = f, then ∫[a,b] f = F(b) - F(a) |
| `my_ftc1` | Part 1: d/dx ∫[a,x] f(t) dt = f(x) |

### Concrete Examples

| Expression | Value |
|----|----|
| ∫[0,1] x dx | 1/2 |
| ∫[0,1] x² dx | 1/3 |
| ∫[0,π] sin x dx | 2 |
| ∫[0,1] eˣ dx | e - 1 |

## Key Learning Points

- **Notation for interval integrals**: `∫ x in a..b, f x` is the integral over [a,b] defined by `intervalIntegral`.
  In Lean, this is built on top of measure theory (`MeasureTheory`).

- **`IntervalIntegrable`**: Theorems about additivity, subtractivity, etc. of integrals require `IntervalIntegrable f volume a b`
  (meaning f is integrable on [a,b]). Continuous functions are always integrable (`Continuous.intervalIntegrable`).

- **How to use FTC Part 2**:
  ```lean
  intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint
  -- hderiv : ∀ x ∈ Set.uIcc a b, HasDerivAt F (f x) x
  -- hint   : IntervalIntegrable f volume a b
  ```

- **Finding antiderivatives**:
  ```
  f(x) = x     → F(x) = x²/2    (HasDerivAt constructed via (hasDerivAt_pow 2 x).div_const 2)
  f(x) = x²    → F(x) = x³/3
  f(x) = sin x → F(x) = -cos x  (HasDerivAt constructed via (Real.hasDerivAt_cos x).neg)
  f(x) = eˣ   → F(x) = eˣ      (use Real.hasDerivAt_exp x directly)
  ```

- **How to use FTC Part 1**:
  ```lean
  Continuous.deriv_integral f hf a b
  -- : deriv (fun u => ∫ x in a..u, f x) b = f b
  ```

- **Scalar multiplication `•` and real multiplication**: In ℝ, `c • x = c * x` (`smul_eq_mul`).
  The result of `integral_const` is in the form `(b - a) • c`, so use `smul_eq_mul` as needed.

## Calculation Example

```lean
-- ∫[0,π] sin x dx = 2
-- (-cos x)' = sin x (HasDerivAt.neg)
-- -cos π - (-cos 0) = 1 - (-1) = 2
have h := integral_eq_sub_of_hasDerivAt
  (f := fun x => -Real.cos x) (f' := Real.sin) ...
simp [Real.cos_zero, Real.cos_pi] at h  -- -(-1) - (-1) = 2
```
