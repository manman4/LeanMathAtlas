# 合同式とフェルマーの小定理

対応する Lean ファイル: `LeanMathAtlas/NumberTheory/Modular.lean`

## 内容

### ZMod の基本
| 定理名 | 内容 |
|--------|------|
| `zmod_self` | `(n : ZMod n) = 0`（n は 0 と合同） |
| `cong_add`, `cong_mul` | 合同式の加法・乗法 |
| `cong_iff_dvd` | `(a : ZMod n) = b ↔ n ∣ b - a` |

### 素数 mod での性質
| 定理名 | 内容 |
|--------|------|
| `zmod_prime_inv` | 素数 p を法とするとき非ゼロ元は可逆 |

### フェルマーの小定理
| 定理名 | 内容 |
|--------|------|
| `fermat_little` | p 素数, a ≢ 0 (mod p) ⟹ a^(p-1) ≡ 1 (mod p) |
| `fermat_little_all` | 系: すべての a に対して a^p ≡ a (mod p) |

## 学習ポイント

- `ZMod n` は整数を n で割った余りの型（ℤ/nℤ）。`decide` で具体的な計算を検証できる。
- `[Fact (Nat.Prime p)]` インスタンスを宣言すると `ZMod p` が体（Field）として扱われる。
- フェルマーの小定理は Mathlib に `ZMod.pow_card_sub_one_eq_one` として収録されている。
- 系 `a^p ≡ a` は a = 0 の場合も成り立つ（場合分けで証明）。
