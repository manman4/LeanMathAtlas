# Combinatorics and the Binomial Theorem

> **日本語で読む →** [BinomialTheorem.md](../../ja/Combinatorics/BinomialTheorem.md)

Corresponding Lean file: `LeanMathAtlas/Combinatorics/BinomialTheorem.lean`

## Contents

### Properties of Combinations
| Theorem Name | Statement |
|--------|------|
| `choose_zero` | $\binom{n}{0} = 1$ |
| `choose_self` | $\binom{n}{n} = 1$ |
| `choose_one` | $\binom{n}{1} = n$ |
| `choose_symm` | $\binom{n}{k} = \binom{n}{n-k}$ (symmetry) |
| `pascal` | $\binom{n}{k} + \binom{n}{k+1} = \binom{n+1}{k+1}$ (Pascal's triangle) |

### Binomial Theorem
| Theorem Name | Statement |
|--------|------|
| `binomial_theorem` | $(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}$ |
| `sum_choose_eq_pow2` | $\sum_{k=0}^{n} \binom{n}{k} = 2^n$ |
| `alternating_sum_choose` | $\sum_{k=0}^{n} (-1)^k \binom{n}{k} = 0$ (for $n \geq 1$) |
