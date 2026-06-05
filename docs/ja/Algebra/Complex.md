# 複素数

対応する Lean ファイル: `LeanMathAtlas/Algebra/Complex.lean`

## 内容

### 基本演算
| 定理名 | 内容 |
|--------|------|
| `I_sq` | $i^2 = -1$ |

### 絶対値（モジュラス）
| 定理名 | 内容 |
|--------|------|
| `normSq_eq_sq` | $\|z\|_{\text{sq}} = \text{re}(z)^2 + \text{im}(z)^2$ |
| `abs_sq` | $\|z\|^2 = \text{normSq}(z)$ |
| `my_abs_mul` | $|zw| = |z||w|$（積の絶対値） |
| `my_abs_add` | $|z+w| \leq |z| + |w|$（三角不等式） |

### 共役複素数
| 定理名 | 内容 |
|--------|------|
| `conj_conj` | $\overline{\overline{z}} = z$（二重共役） |
| `conj_add` | $\overline{z+w} = \overline{z} + \overline{w}$ |
| `conj_mul` | $\overline{zw} = \overline{z}\,\overline{w}$ |
| `mul_conj'` | $z \cdot \overline{z} = \|z\|^2$ |

### オイラーの公式・ド・モアブルの定理
| 定理名 | 内容 |
|--------|------|
| `euler_formula` | $e^{i\theta} = \cos\theta + i\sin\theta$ |
| `abs_exp_I` | $|e^{i\theta}| = 1$（単位円上） |
| `de_moivre` | $(e^{i\theta})^n = e^{in\theta}$（ド・モアブルの定理） |

## 学習ポイント

- Lean における共役は `star z`（または `conj z`）で表す。型クラス `Star` の一例。
- `Complex.normSq` は $\text{re}^2 + \text{im}^2$ の整数値計算に便利（sqrt を避けられる）。
- `Complex.abs` は $\sqrt{\text{normSq}}$ として定義される。
- オイラーの公式から `de_moivre` は `exp_nat_mul` と `ring` で導ける。
