# 位相空間: 開集合・コンパクト性・連結性

対応する Lean ファイル: `LeanMathAtlas/Topology/Basic.lean`

## 内容

### 開集合と閉集合
| 定理名 | 内容 |
|--------|------|
| `my_isOpen_univ` | 全体集合は開 |
| `my_isOpen_empty` | 空集合は開 |
| `my_isOpen_inter` | 開集合の有限交差は開 |
| `my_isOpen_iUnion` | 開集合の任意合併は開 |
| `my_isClosed_compl_iff` | s が開 ↔ sᶜ が閉（双対性） |
| `my_isClosed_union` | 閉集合の有限合併は閉 |
| `my_isClosed_iInter` | 閉集合の任意交差は閉 |

### 連続写像
| 定理名 | 内容 |
|--------|------|
| `my_isOpen_preimage` | 連続写像の開集合の逆像は開 |
| `my_continuous_comp` | 連続写像の合成は連続 |
| `my_continuous_id` | 恒等写像は連続 |
| `my_continuous_const` | 定数写像は連続 |

### コンパクト集合
| 定理名 | 内容 |
|--------|------|
| `my_isCompact_elim_finite_subcover` | 有限被覆性: 任意の開被覆は有限部分被覆を持つ |
| `my_isCompact_inter_right` | コンパクト ∩ 閉 = コンパクト |
| `my_isCompact_of_isClosed_subset` | コンパクト集合の閉部分集合はコンパクト |
| `my_isCompact_image` | 連続写像によるコンパクト集合の像はコンパクト |

### 連結集合
| 定理名 | 内容 |
|--------|------|
| `my_isConnected_singleton` | 単元集合は連結 |
| `my_isConnected_union` | 共通点を持つ連結集合の合併は連結 |
| `my_isConnected_image` | 連続写像による連結集合の像は連結 |
| `my_isConnected_univ` | 連結空間全体は連結 |

## 学習ポイント

- 位相空間の定義は「開集合族」による公理的アプローチ:
  - 全体集合・空集合は開
  - 任意合併は開（無限でもOK）
  - 有限交差は開
  - 閉集合は開集合の補集合として定義される

- **開と閉の非対称性**:
  - 無限合併の開集合 → 開（OK）
  - 無限合併の閉集合 → 閉とは限らない（例: ⋃ₙ [1/n, 1] = (0, 1]）
  - 有限交差の閉集合 → 閉（OK）
  - 無限交差の開集合 → 開とは限らない（例: ⋂ₙ (-1/n, 1/n) = {0}）

- **コンパクト集合**: ハイネ・ボレルの定理 — ℝⁿ では「有界閉集合 = コンパクト」。Lean では開被覆による一般的定義を使用。

- **連結集合**: 空でない集合が2つの交わらない開集合に分割できないもの。区間の連結性は中間値の定理の基礎。

## 具体例

```
ℝ での重要な事実:
  isCompact_Icc  : IsCompact (Icc a b)   -- [a,b] はコンパクト
  isConnected_Icc : IsConnected (Icc a b) -- [a,b] は連結 (a ≤ b)
  ConnectedSpace ℝ                       -- ℝ は連結空間

応用:
  sin の像 sin([0, π]) はコンパクトかつ連結 ✓
  [0,1] ∩ [1/2, 2] = [1/2, 1] はコンパクト ✓
```
