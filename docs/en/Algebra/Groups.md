# Group Theory: Groups, Subgroups, and Lagrange's Theorem

> **日本語で読む →** [Groups.md](../../ja/Algebra/Groups.md)

Corresponding Lean file: `LeanMathAtlas/Algebra/Groups.lean`

## Contents

### Basic Group Laws
| Theorem Name | Statement |
|--------|------|
| `my_mul_one` | Right identity: a * 1 = a |
| `my_one_mul` | Left identity: 1 * a = a |
| `my_mul_inv_cancel` | Right inverse: a * a⁻¹ = 1 |
| `my_inv_mul_cancel` | Left inverse: a⁻¹ * a = 1 |
| `my_inv_inv` | Inverse of inverse: (a⁻¹)⁻¹ = a |
| `my_mul_inv_rev` | Inverse of product: (a * b)⁻¹ = b⁻¹ * a⁻¹ |
| `my_mul_left_cancel` | Left cancellation: a * b = a * c → b = c |
| `my_mul_right_cancel` | Right cancellation: a * b = c * b → a = c |
| `my_one_unique` | Uniqueness of the identity element |
| `my_eq_inv_mul_of_mul_eq` | Solution to a * x = b: x = a⁻¹ * b |

### Subgroups
| Theorem Name | Statement |
|--------|------|
| `my_subgroup_one` | A subgroup contains the identity element |
| `my_subgroup_mul` | A subgroup is closed under multiplication |
| `my_subgroup_inv` | A subgroup is closed under taking inverses |
| `my_subgroup_inter` | The intersection of subgroups is a subgroup |

### Lagrange's Theorem
| Theorem Name | Statement |
|--------|------|
| `lagrange` | \|H\| ∣ \|G\| (Nat.card version) |
| `lagrange_index` | \|H\| * [G:H] = \|G\| (relation to index) |

### Order of Elements
| Theorem Name | Statement |
|--------|------|
| `my_pow_orderOf_eq_one` | a^(orderOf a) = 1 |
| `my_orderOf_dvd_of_pow_eq_one` | a^n = 1 → orderOf a ∣ n |
| `my_orderOf_dvd_card` | orderOf a ∣ \|G\| (corollary of Lagrange's theorem) |
| `my_pow_card_eq_one` | a^\|G\| = 1 |

## Learning Points

- `Group G` is the type class for multiplicative groups. `AddGroup G` is its additive counterpart. `ZMod n` implements `AddGroup` as an additive group.
- `Subgroup G` is the type representing a subgroup. It is defined by satisfying the three conditions: identity, closure under multiplication, and closure under inverses.
- Lagrange's theorem: for a subgroup H of a finite group G, `Nat.card H ∣ Nat.card G` holds.
  - In Mathlib this is recorded as `Subgroup.card_subgroup_dvd_card`.
  - The key idea of the proof is the "partition into left cosets": G = H · g₁ ∪ H · g₂ ∪ … (disjoint union).
- `orderOf a` is the smallest positive integer satisfying `a^n = 1`. As a corollary of Lagrange's theorem, `orderOf a ∣ Fintype.card G`.
- `addOrderOf` is the corresponding concept for additive groups. In `ZMod n`, `ZMod.addOrderOf_coe` gives `addOrderOf (a : ZMod n) = n / gcd(n, a)`.

## Concrete Examples

```
Additive orders in ZMod 6:
  addOrderOf 1 = 6   (generator)
  addOrderOf 2 = 3   (6 / gcd(6,2) = 6/2 = 3)
  addOrderOf 3 = 2   (6 / gcd(6,3) = 6/3 = 2)

Verification of Lagrange's corollary:
  3 ∣ 6 ✓  (addOrderOf 2 = 3, |ZMod 6| = 6)
```
