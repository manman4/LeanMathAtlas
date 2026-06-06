# Inner Products, Norms, and the Cauchy-Schwarz Inequality

> **日本語で読む →** [Vectors.md](../../ja/LinearAlgebra/Vectors.md)

Corresponding Lean file: `LeanMathAtlas/LinearAlgebra/Vectors.lean`

## Contents

### Basic Properties of Inner Products
| Theorem name | Description |
|--------|------|
| `my_inner_comm` | Symmetry: ⟪x, y⟫ = ⟪y, x⟫ |
| `my_inner_add_left` | Additivity in the left argument: ⟪x + y, z⟫ = ⟪x, z⟫ + ⟪y, z⟫ |
| `my_inner_smul_left` | Scalar multiplication: ⟪c • x, y⟫ = c * ⟪x, y⟫ |
| `my_inner_self_nonneg` | Positive definiteness: ⟪x, x⟫ ≥ 0 |
| `my_inner_self_eq_zero` | ⟪x, x⟫ = 0 ↔ x = 0 |
| `my_inner_self_eq_norm_sq` | ⟪x, x⟫ = ‖x‖² |

### Basic Properties of Norms
| Theorem name | Description |
|--------|------|
| `my_norm_nonneg` | ‖x‖ ≥ 0 |
| `my_norm_eq_zero` | ‖x‖ = 0 ↔ x = 0 |
| `my_norm_smul` | ‖c • x‖ = \|c\| * ‖x‖ |
| `my_norm_add_le` | Triangle inequality: ‖x + y‖ ≤ ‖x‖ + ‖y‖ |
| `my_norm_neg` | ‖-x‖ = ‖x‖ |

### Cauchy-Schwarz Inequality
| Theorem name | Description |
|--------|------|
| `cauchy_schwarz` | \|⟪x, y⟫\| ≤ ‖x‖ * ‖y‖ |
| `cauchy_schwarz_sq` | ⟪x, y⟫² ≤ ⟪x, x⟫ * ⟪y, y⟫ |

### Concrete Examples in ℝ²
| Theorem name | Description |
|--------|------|
| `e1_inner_e2` | Standard basis vectors e₁, e₂ are orthogonal: ⟪e₁, e₂⟫ = 0 |
| `norm_e1`, `norm_e2` | ‖e₁‖ = ‖e₂‖ = 1 |

## Learning Points

- `InnerProductSpace ℝ E` is an inner product space over the real field ℝ. `EuclideanSpace ℝ (Fin n)` is a concrete instance for ℝⁿ.
- In Lean, the inner product is written as `inner x y` (fixing to the real inner product by specifying `𝕜 := ℝ`).
- The Cauchy-Schwarz inequality is available in Mathlib as `abs_real_inner_le_norm`.
- The triangle inequality follows from Cauchy-Schwarz (directly usable via `norm_add_le`).
