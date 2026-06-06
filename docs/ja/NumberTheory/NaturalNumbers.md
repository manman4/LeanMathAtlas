# 自然数の算術・帰納法

> **Read in English →** [NaturalNumbers.md](../../en/NumberTheory/NaturalNumbers.md)

対応する Lean ファイル: `LeanMathAtlas/NumberTheory/NaturalNumbers.lean`

## 内容

### 帰納法の基本
| 定理名 | 内容 |
|--------|------|
| `my_zero_add` | $0+n=n$（帰納法による手動証明） |
| `my_add_assoc` | $(a+b)+c = a+(b+c)$（結合法則、帰納法） |
| `my_add_comm` | $a+b=b+a$（交換法則、帰納法） |

### 帰納法の応用
| 定理名 | 内容 |
|--------|------|
| `double_eq_two_mul` | $n+n=2n$ |
| `my_zero_le` | $0 \leq n$ |

### 偶数・奇数
| 定理名 | 内容 |
|--------|------|
| `even_add_even` | 偶数＋偶数＝偶数 |

## 学習ポイント

Lean の `induction n with | zero => ... | succ k ih => ...` 構文を使って、
数学的帰納法の基底・帰納段階を直接記述します。  
`omega` タクティクは自然数・整数の線形算術を自動解決します。