# 式の展開・因数分解・多項式定理

対応する Lean ファイル: `LeanMathAtlas/Algebra/BasicIdentities.lean`

## 内容

### 数学 I — 式の展開
| 定理名 | 内容 |
|--------|------|
| `sq_sum` | $(a+b)^2 = a^2+2ab+b^2$ |
| `sq_diff` | $(a-b)^2 = a^2-2ab+b^2$ |
| `mul_sum_diff` | $(a+b)(a-b) = a^2-b^2$ |
| `cube_sum` | $(a+b)^3 = a^3+3a^2b+3ab^2+b^3$ |
| `cube_diff` | $(a-b)^3 = a^3-3a^2b+3ab^2-b^3$ |

### 数学 I — 因数分解
| 定理名 | 内容 |
|--------|------|
| `factor_diff_sq` | $a^2-b^2 = (a+b)(a-b)$ |
| `factor_sum_cubes` | $a^3+b^3 = (a+b)(a^2-ab+b^2)$ |
| `factor_diff_cubes` | $a^3-b^3 = (a-b)(a^2+ab+b^2)$ |

### 数学 I — 二次不等式
| 定理名 | 内容 |
|--------|------|
| `quadratic_pos_of_neg_disc` | $b^2-4ac < 0$ かつ $a>0$ なら $ax^2+bx+c>0$ |

### 数学 II — 多項式
| 定理名 | 内容 |
|--------|------|
| `factor_theorem` | 因数定理: $p(a)=0 \iff (X-a) \mid p(X)$ |
| `remainder_theorem` | 剰余定理: $(X-a)$ で割った余りは $p(a)$ |
