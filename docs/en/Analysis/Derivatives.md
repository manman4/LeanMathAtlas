# Differentiation (Derivatives)

> **日本語で読む →** [Derivatives.md](../../ja/Analysis/Derivatives.md)

Corresponding Lean file: `LeanMathAtlas/Analysis/Derivatives.lean`

## How to Read `HasDerivAt`

```lean
HasDerivAt f f' a
```

This means: "the function f is differentiable at point a, and f'(a) = f'."

## Contents

### Basic Derivatives
| Theorem Name | Statement |
|--------|------|
| `deriv_const` | The derivative of a constant function is 0 |
| `deriv_id'` | The derivative of the identity function is 1 |
| `deriv_pow'` | $\dfrac{d}{dx}[x^n] = n x^{n-1}$ |
| `deriv_sq` | $\dfrac{d}{dx}[x^2] = 2x$ |
| `deriv_cube` | $\dfrac{d}{dx}[x^3] = 3x^2$ |

### Rules of Differentiation
| Theorem Name | Statement |
|--------|------|
| `deriv_add'` | Sum rule: $(f+g)' = f' + g'$ |
| `deriv_const_mul'` | Constant multiple rule: $(cf)' = cf'$ |
| `deriv_mul'` | Product rule: $(fg)' = f'g + fg'$ |
| `deriv_comp'` | Chain rule: $(g \circ f)' = g'(f(a)) \cdot f'(a)$ |

### Concrete Applications
| Theorem Name | Statement |
|--------|------|
| `deriv_quadratic` | $\dfrac{d}{dx}[x^2+3x+1] = 2x+3$ |
| `deriv_product_example` | $\dfrac{d}{dx}[x(x+1)] = 2x+1$ |

### Derivatives of Trigonometric Functions
| Theorem Name | Statement |
|--------|------|
| `deriv_sin'` | $\dfrac{d}{dx}[\sin x] = \cos x$ |
| `deriv_cos'` | $\dfrac{d}{dx}[\cos x] = -\sin x$ |
| `deriv_sin_double` | $\dfrac{d}{dx}[\sin 2x] = 2\cos 2x$ (application of the chain rule) |
| `deriv_sin_cos` | $\dfrac{d}{dx}[\sin x \cos x] = \cos^2 x - \sin^2 x$ (product rule → double-angle formula) |

## Key Learning Points

- In Lean, differentiation is expressed with `HasDerivAt`, which simultaneously asserts differentiability at a point a and the value of the derivative.
- For the chain rule, `hg.comp a hf` calls `.comp` on the outer derivative information `hg`.
- Use `simpa using hasDerivAt_pow n a` to obtain the concrete derivative of $x^n$.
