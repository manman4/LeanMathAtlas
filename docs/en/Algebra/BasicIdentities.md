# Algebraic Expansion, Factoring, and the Binomial Theorem

> **日本語で読む →** [BasicIdentities.md](../../ja/Algebra/BasicIdentities.md)

Corresponding Lean file: `LeanMathAtlas/Algebra/BasicIdentities.lean`

## Contents

### Algebra I — Polynomial Expansion
| Theorem Name | Statement |
|--------|------|
| `sq_sum` | $(a+b)^2 = a^2+2ab+b^2$ |
| `sq_diff` | $(a-b)^2 = a^2-2ab+b^2$ |
| `mul_sum_diff` | $(a+b)(a-b) = a^2-b^2$ |
| `cube_sum` | $(a+b)^3 = a^3+3a^2b+3ab^2+b^3$ |
| `cube_diff` | $(a-b)^3 = a^3-3a^2b+3ab^2-b^3$ |

### Algebra I — Factoring
| Theorem Name | Statement |
|--------|------|
| `factor_diff_sq` | $a^2-b^2 = (a+b)(a-b)$ |
| `factor_sum_cubes` | $a^3+b^3 = (a+b)(a^2-ab+b^2)$ |
| `factor_diff_cubes` | $a^3-b^3 = (a-b)(a^2+ab+b^2)$ |

### Algebra I — Quadratic Inequalities
| Theorem Name | Statement |
|--------|------|
| `quadratic_pos_of_neg_disc` | If $b^2-4ac < 0$ and $a>0$, then $ax^2+bx+c>0$ |

### Algebra II — Polynomials
| Theorem Name | Statement |
|--------|------|
| `factor_theorem` | Factor theorem: $p(a)=0 \iff (X-a) \mid p(X)$ |
| `remainder_theorem` | Remainder theorem: the remainder when dividing by $(X-a)$ is $p(a)$ |
