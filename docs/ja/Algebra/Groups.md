# 群論: 群・部分群・ラグランジュの定理

> **Read in English →** [Groups.md](../../en/Algebra/Groups.md)

対応する Lean ファイル: `LeanMathAtlas/Algebra/Groups.lean`

## 内容

### 群の基本法則
| 定理名 | 内容 |
|--------|------|
| `my_mul_one` | 右単位元: a * 1 = a |
| `my_one_mul` | 左単位元: 1 * a = a |
| `my_mul_inv_cancel` | 右逆元: a * a⁻¹ = 1 |
| `my_inv_mul_cancel` | 左逆元: a⁻¹ * a = 1 |
| `my_inv_inv` | 逆元の逆元: (a⁻¹)⁻¹ = a |
| `my_mul_inv_rev` | 積の逆元: (a * b)⁻¹ = b⁻¹ * a⁻¹ |
| `my_mul_left_cancel` | 左消去法則: a * b = a * c → b = c |
| `my_mul_right_cancel` | 右消去法則: a * b = c * b → a = c |
| `my_one_unique` | 単位元の一意性 |
| `my_eq_inv_mul_of_mul_eq` | 方程式 a * x = b の解: x = a⁻¹ * b |

### 部分群 (Subgroup)
| 定理名 | 内容 |
|--------|------|
| `my_subgroup_one` | 部分群は単位元を含む |
| `my_subgroup_mul` | 部分群は積について閉じている |
| `my_subgroup_inv` | 部分群は逆元について閉じている |
| `my_subgroup_inter` | 共通部分も部分群 |

### ラグランジュの定理
| 定理名 | 内容 |
|--------|------|
| `lagrange` | \|H\| ∣ \|G\|（Nat.card 版） |
| `lagrange_index` | \|H\| * [G:H] = \|G\|（指数との関係） |

### 元の位数 (Order of Elements)
| 定理名 | 内容 |
|--------|------|
| `my_pow_orderOf_eq_one` | a^(orderOf a) = 1 |
| `my_orderOf_dvd_of_pow_eq_one` | a^n = 1 → orderOf a ∣ n |
| `my_orderOf_dvd_card` | orderOf a ∣ \|G\|（ラグランジュの系） |
| `my_pow_card_eq_one` | a^\|G\| = 1 |

## 学習ポイント

- `Group G` は乗法群の型クラス。`AddGroup G` が加法群。`ZMod n` は加法群として `AddGroup` を実装している。
- `Subgroup G` は部分群を表す型。単位元・積・逆元の三条件を満たすことで定義される。
- ラグランジュの定理: 有限群 G の部分群 H について `Nat.card H ∣ Nat.card G` が成立。
  - Mathlib では `Subgroup.card_subgroup_dvd_card` として収録されている。
  - 証明の核心は「左剰余類の分割」: G = H · g₁ ∪ H · g₂ ∪ … (disjoint union)
- `orderOf a` は `a^n = 1` を満たす最小の正整数。ラグランジュの定理の系として `orderOf a ∣ Fintype.card G`。
- `addOrderOf` は加法群での対応概念。`ZMod n` では `ZMod.addOrderOf_coe` により `addOrderOf (a : ZMod n) = n / gcd(n, a)` が成立。

## 具体例

```
ZMod 6 の加法位数:
  addOrderOf 1 = 6   (生成元)
  addOrderOf 2 = 3   (6 / gcd(6,2) = 6/2 = 3)
  addOrderOf 3 = 2   (6 / gcd(6,3) = 6/3 = 2)

ラグランジュの系の確認:
  3 ∣ 6 ✓  (addOrderOf 2 = 3, |ZMod 6| = 6)
```