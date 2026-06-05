# 環論: 環・イデアル・商環

対応する Lean ファイル: `LeanMathAtlas/Algebra/Rings.lean`

## 内容

### 環の基本法則
| 定理名 | 内容 |
|--------|------|
| `my_mul_add` | 分配法則: a * (b + c) = a * b + a * c |
| `my_mul_comm` | 可換性: a * b = b * a |
| `my_mul_zero` | a * 0 = 0 |
| `my_neg_one_mul` | -1 * a = -a |
| `my_mul_one` | a * 1 = a |

### イデアル
| 定理名 | 内容 |
|--------|------|
| `my_ideal_add_mem` | イデアルは加法について閉じている |
| `my_ideal_mul_mem_left` | イデアルは左乗法について閉じている |
| `my_mem_span_singleton_self` | a ∈ (a)（a は自分自身が生成するイデアルに属する） |
| `my_span_one` | (1) = R |
| `my_span_singleton_eq_top` | (a) = R ↔ a は単元 |
| `my_exists_le_maximal` | 真のイデアルは極大イデアルに含まれる |

### 商環
| 定理名 | 内容 |
|--------|------|
| `my_quotient_eq_zero_iff` | mk I a = 0 ↔ a ∈ I |
| `my_quotient_mk_eq_iff` | mk I a = mk I b ↔ a - b ∈ I |

### 素イデアルと極大イデアルの対応
| 定理名 | 内容 |
|--------|------|
| `my_isPrime_iff_isDomain` | I が素イデアル ↔ R ⧸ I が整域 |
| `my_isMaximal_iff_isField` | I が極大イデアル ↔ R ⧸ I が体 |
| `my_isMaximal_isPrime` | 極大イデアル → 素イデアル |

### ℤ での具体例
| 定理名 | 内容 |
|--------|------|
| `span_five_isPrime` | 5ℤ は ℤ の素イデアル |
| `ker_intCast_eq_span` | ker(ℤ → ZMod n) = nℤ |

## 学習ポイント

- **イデアル (Ideal)**: 環 R の部分集合 I で、加法と左右乗法について閉じているもの。
  Lean では `Ideal R` 型で表され、`Submodule R R` として実装されている。

- **商環 (Quotient Ring)**: イデアル I による商を `R ⧸ I` と書く。
  `Ideal.Quotient.mk I : R →+* R ⧸ I` が標準射影。

- **重要な対応（環論の基本定理）**:
  ```
  I が素イデアル  ↔  R ⧸ I が整域
  I が極大イデアル ↔  R ⧸ I が体
  極大イデアル ⊂ 素イデアル（体は整域）
  ```

- **ℤ の例**:
  - `5ℤ` は素イデアル（5 が素数） → `ℤ/5ℤ ≅ ZMod 5` は体
  - `4ℤ` は素イデアルでない（4 = 2 × 2）→ `ZMod 4` に零因子あり（2 * 2 = 0）
  - `ker(ℤ → ZMod n) = nℤ`（第一同型定理: `ℤ/nℤ ≅ ZMod n`）

## 零因子の例

```
ZMod 4:  2 * 2 = 0,  2 ≠ 0  → 整域でない
ZMod 6:  3 * 2 = 0,  3 ≠ 0  → 整域でない
ZMod 5:  零因子なし           → 体（5 が素数）
```
