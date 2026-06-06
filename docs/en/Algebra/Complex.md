# Complex Numbers

> **日本語で読む →** [Complex.md](../../ja/Algebra/Complex.md)

Corresponding Lean file: `LeanMathAtlas/Algebra/Complex.lean`

## Contents

### Basic Operations
| Theorem Name | Statement |
|--------|------|
| `I_sq` | $i^2 = -1$ |

### Absolute Value (Modulus)
| Theorem Name | Statement |
|--------|------|
| `normSq_eq_sq` | $\|z\|_{\text{sq}} = \text{re}(z)^2 + \text{im}(z)^2$ |
| `abs_sq` | $\|z\|^2 = \text{normSq}(z)$ |
| `my_abs_mul` | $|zw| = |z||w|$ (absolute value of a product) |
| `my_abs_add` | $|z+w| \leq |z| + |w|$ (triangle inequality) |

### Complex Conjugate
| Theorem Name | Statement |
|--------|------|
| `conj_conj` | $\overline{\overline{z}} = z$ (double conjugate) |
| `conj_add` | $\overline{z+w} = \overline{z} + \overline{w}$ |
| `conj_mul` | $\overline{zw} = \overline{z}\,\overline{w}$ |
| `mul_conj'` | $z \cdot \overline{z} = \|z\|^2$ |

### Euler's Formula and De Moivre's Theorem
| Theorem Name | Statement |
|--------|------|
| `euler_formula` | $e^{i\theta} = \cos\theta + i\sin\theta$ |
| `abs_exp_I` | $|e^{i\theta}| = 1$ (on the unit circle) |
| `de_moivre` | $(e^{i\theta})^n = e^{in\theta}$ (De Moivre's theorem) |

## Learning Points

- In Lean, the complex conjugate is written as `star z` (or `conj z`). This is an instance of the `Star` type class.
- `Complex.normSq` is useful for integer-valued computations of $\text{re}^2 + \text{im}^2$ (avoiding square roots).
- `Complex.abs` is defined as $\sqrt{\text{normSq}}$.
- From Euler's formula, `de_moivre` can be derived using `exp_nat_mul` and `ring`.
