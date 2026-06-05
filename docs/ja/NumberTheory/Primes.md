# 素数と整除性

対応する Lean ファイル: `StudyLean4/NumberTheory/Primes.lean`

## 内容

### 素数の例と基本性質
| 定理名 | 内容 |
|--------|------|
| `two_prime`, `three_prime`, ... | 2, 3, 5, 7 が素数 (`decide` で自動確認) |
| `prime_ge_two` | すべての素数は 2 以上 |
| `prime_divisors` | 素数 p の約数は 1 か p のみ |
| `prime_odd_or_two` | 2 以外の素数は奇数 |

### 最大公約数 (GCD)
| 定理名 | 内容 |
|--------|------|
| `my_gcd_dvd_left`, `my_gcd_dvd_right` | gcd は両方を割り切る |
| `my_dvd_gcd` | 公約数の中で最大（最大公約数性） |
| `my_gcd_comm` | gcd の交換法則 |
| `my_gcd_zero_right` | gcd(a, 0) = a |
| `my_gcd_self` | gcd(a, a) = a |

### 互いに素
| 定理名 | 内容 |
|--------|------|
| `coprime_succ` | 連続する整数は互いに素（証明: gcd が 1 を割り切る） |
| `prime_coprime_of_not_dvd` | p が a を割り切らないなら gcd(p, a) = 1 |
| `coprime_dvd_of_dvd_mul` | ガウスの補題: gcd(k,n)=1 かつ k|mn ⟹ k|m |

### ユークリッドの定理
| 定理名 | 内容 |
|--------|------|
| `exists_prime_ge` | 任意の n に対して n 以上の素数が存在する（無限個の素数） |

## 学習ポイント

- `decide` タクティクは命題を有限計算で自動検証する。素数判定に使える。
- `Nat.Coprime a b` の定義は `Nat.gcd a b = 1` に展開される。
- `coprime_succ` の証明は「gcd(n, n+1) は (n+1)-n = 1 を割り切る」という初等的アイデア。
