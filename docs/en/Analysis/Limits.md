# Limits and Continuity

> **日本語で読む →** [Limits.md](../../ja/Analysis/Limits.md)

Corresponding Lean file: `LeanMathAtlas/Analysis/Limits.lean`

## Contents

### Equivalence of ε-δ and Filter.Tendsto
| Theorem Name | Statement |
|--------|------|
| `tendsto_iff_eps_delta` | `Filter.Tendsto f (𝓝 a) (𝓝 b) ↔ ∀ε>0, ∃δ>0, \|x-a\|<δ → \|f x-b\|<ε` |
| `tendsto_of_eps_delta` | Construct Filter.Tendsto from an ε-δ condition |

### Basic Limits
| Theorem Name | Statement |
|--------|------|
| `my_tendsto_const` | lim c = c (constant function) |
| `my_tendsto_id` | lim x = a (identity function) |
| `tendsto_linear` | lim (mx + b) = ma + b |
| `tendsto_sq` | lim x² = a² |

### Arithmetic Rules for Limits
| Theorem Name | Statement |
|--------|------|
| `my_tendsto_add` | lim(f + g) = lim f + lim g |
| `my_tendsto_const_mul` | lim(c·f) = c·lim f |
| `my_tendsto_mul` | lim(f·g) = lim f · lim g |
| `my_tendsto_comp` | Limit of a composite function (chain rule) |

### Continuity and Squeeze Theorem
| Theorem Name | Statement |
|--------|------|
| `continuousAt_iff_tendsto` | `ContinuousAt f a ↔ Tendsto f (𝓝 a) (𝓝 (f a))` |
| `continuous_poly` | The polynomial x² + 3x + 1 is continuous |
| `squeeze_tendsto` | Squeeze theorem |

## Key Learning Points

- `𝓝 a` (`nhds a`) is the neighborhood filter at point a — an abstraction of "all points sufficiently close to a."
- `Filter.Tendsto f l₁ l₂` is the abstract definition of a limit: "f maps the filter l₁ into l₂."
- Use `Metric.tendsto_nhds_nhds` to convert to the ε-δ formulation in a metric space.
- `∀ᶠ x in 𝓝 a, P x` (`Filter.Eventually`) means "P x holds for almost all x in a neighborhood of a."
- The squeeze theorem uses `tendsto_of_tendsto_of_tendsto_of_le_of_le'` (with the `'` suffix) — the `∀ᶠ` version.
