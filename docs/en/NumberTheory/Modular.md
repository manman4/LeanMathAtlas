# Congruences and Fermat's Little Theorem

> **日本語で読む →** [Modular.md](../../ja/NumberTheory/Modular.md)

Corresponding Lean file: `LeanMathAtlas/NumberTheory/Modular.lean`

## Contents

### Basics of ZMod
| Theorem name | Description |
|--------|------|
| `zmod_self` | `(n : ZMod n) = 0` (n is congruent to 0) |
| `cong_add`, `cong_mul` | Addition and multiplication of congruences |
| `cong_iff_dvd` | `(a : ZMod n) = b ↔ n ∣ b - a` |

### Properties modulo a prime
| Theorem name | Description |
|--------|------|
| `zmod_prime_inv` | Nonzero elements are invertible modulo a prime p |

### Fermat's Little Theorem
| Theorem name | Description |
|--------|------|
| `fermat_little` | p prime, a ≢ 0 (mod p) ⟹ a^(p-1) ≡ 1 (mod p) |
| `fermat_little_all` | Corollary: for all a, a^p ≡ a (mod p) |

## Learning Points

- `ZMod n` is the type of integers modulo n (ℤ/nℤ). Concrete computations can be verified with `decide`.
- Declaring a `[Fact (Nat.Prime p)]` instance allows `ZMod p` to be treated as a field (Field).
- Fermat's Little Theorem is available in Mathlib as `ZMod.pow_card_sub_one_eq_one`.
- The corollary `a^p ≡ a` also holds when a = 0 (proved by case analysis).
