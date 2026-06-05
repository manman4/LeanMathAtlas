# 場合の数・二項定理

対応する Lean ファイル: `StudyLean4/Combinatorics/BinomialTheorem.lean`

## 内容

### 数学 A — 組み合わせの性質
| 定理名 | 内容 |
|--------|------|
| `choose_zero` | $\binom{n}{0} = 1$ |
| `choose_self` | $\binom{n}{n} = 1$ |
| `choose_one` | $\binom{n}{1} = n$ |
| `choose_symm` | $\binom{n}{k} = \binom{n}{n-k}$（対称性） |
| `pascal` | $\binom{n}{k} + \binom{n}{k+1} = \binom{n+1}{k+1}$（パスカルの三角形） |

### 数学 II — 二項定理
| 定理名 | 内容 |
|--------|------|
| `binomial_theorem` | $(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}$ |
| `sum_choose_eq_pow2` | $\sum_{k=0}^{n} \binom{n}{k} = 2^n$ |
| `alternating_sum_choose` | $\sum_{k=0}^{n} (-1)^k \binom{n}{k} = 0$（$n \geq 1$） |
