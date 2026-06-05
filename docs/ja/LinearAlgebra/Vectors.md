# 内積・ノルム・コーシー・シュワルツ

対応する Lean ファイル: `LeanMathAtlas/LinearAlgebra/Vectors.lean`

## 内容

### 内積の基本性質
| 定理名 | 内容 |
|--------|------|
| `my_inner_comm` | 対称性: ⟪x, y⟫ = ⟪y, x⟫ |
| `my_inner_add_left` | 加法線形性: ⟪x + y, z⟫ = ⟪x, z⟫ + ⟪y, z⟫ |
| `my_inner_smul_left` | スカラー倍: ⟪c • x, y⟫ = c * ⟪x, y⟫ |
| `my_inner_self_nonneg` | 正定値性: ⟪x, x⟫ ≥ 0 |
| `my_inner_self_eq_zero` | ⟪x, x⟫ = 0 ↔ x = 0 |
| `my_inner_self_eq_norm_sq` | ⟪x, x⟫ = ‖x‖² |

### ノルムの基本性質
| 定理名 | 内容 |
|--------|------|
| `my_norm_nonneg` | ‖x‖ ≥ 0 |
| `my_norm_eq_zero` | ‖x‖ = 0 ↔ x = 0 |
| `my_norm_smul` | ‖c • x‖ = \|c\| * ‖x‖ |
| `my_norm_add_le` | 三角不等式: ‖x + y‖ ≤ ‖x‖ + ‖y‖ |
| `my_norm_neg` | ‖-x‖ = ‖x‖ |

### コーシー・シュワルツの不等式
| 定理名 | 内容 |
|--------|------|
| `cauchy_schwarz` | \|⟪x, y⟫\| ≤ ‖x‖ * ‖y‖ |
| `cauchy_schwarz_sq` | ⟪x, y⟫² ≤ ⟪x, x⟫ * ⟪y, y⟫ |

### ℝ² での具体例
| 定理名 | 内容 |
|--------|------|
| `e1_inner_e2` | 標準基底 e₁, e₂ は直交: ⟪e₁, e₂⟫ = 0 |
| `norm_e1`, `norm_e2` | ‖e₁‖ = ‖e₂‖ = 1 |

## 学習ポイント

- `InnerProductSpace ℝ E` は実数体 ℝ 上の内積空間。`EuclideanSpace ℝ (Fin n)` は ℝⁿ の具体例。
- Lean では内積を `inner x y` と書く（`𝕜 := ℝ` を明示することで実数の内積に固定）。
- コーシー・シュワルツの不等式は Mathlib に `abs_real_inner_le_norm` として収録されている。
- 三角不等式はコーシー・シュワルツから導出される（`norm_add_le` で直接使える）。
