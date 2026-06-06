# 極限と連続性

> **Read in English →** [Limits.md](../../en/Analysis/Limits.md)

対応する Lean ファイル: `LeanMathAtlas/Analysis/Limits.lean`

## 内容

### ε-δ と Filter.Tendsto の等価性
| 定理名 | 内容 |
|--------|------|
| `tendsto_iff_eps_delta` | `Filter.Tendsto f (𝓝 a) (𝓝 b) ↔ ∀ε>0, ∃δ>0, \|x-a\|<δ → \|f x-b\|<ε` |
| `tendsto_of_eps_delta` | ε-δ 条件から Filter.Tendsto を構成 |

### 基本的な極限
| 定理名 | 内容 |
|--------|------|
| `my_tendsto_const` | lim c = c（定数関数） |
| `my_tendsto_id` | lim x = a（恒等関数） |
| `tendsto_linear` | lim (mx + b) = ma + b |
| `tendsto_sq` | lim x² = a² |

### 極限の演算法則
| 定理名 | 内容 |
|--------|------|
| `my_tendsto_add` | lim(f + g) = lim f + lim g |
| `my_tendsto_const_mul` | lim(c·f) = c·lim f |
| `my_tendsto_mul` | lim(f·g) = lim f · lim g |
| `my_tendsto_comp` | 合成関数の極限（連鎖律） |

### 連続性・はさみうち
| 定理名 | 内容 |
|--------|------|
| `continuousAt_iff_tendsto` | `ContinuousAt f a ↔ Tendsto f (𝓝 a) (𝓝 (f a))` |
| `continuous_poly` | 多項式 x² + 3x + 1 は連続 |
| `squeeze_tendsto` | はさみうちの定理 |

## 学習ポイント

- `𝓝 a`（`nhds a`）は点 a の近傍フィルター。「a に十分近い点全体」を抽象化したもの。
- `Filter.Tendsto f l₁ l₂` は「f がフィルター l₁ を l₂ に写す」という抽象的な極限の定義。
- `Metric.tendsto_nhds_nhds` を使うと距離空間での ε-δ 表示に変換できる。
- `∀ᶠ x in 𝓝 a, P x`（`Filter.Eventually`）は「a の近傍でほぼすべての x について P x が成立」を意味する。
- はさみうちの定理は `tendsto_of_tendsto_of_tendsto_of_le_of_le'`（`'` 付き）を使う（`∀ᶠ` 版）。