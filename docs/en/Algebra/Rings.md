# Ring Theory: Rings, Ideals, and Quotient Rings

> **日本語で読む →** [Rings.md](../../ja/Algebra/Rings.md)

Corresponding Lean file: `LeanMathAtlas/Algebra/Rings.lean`

## Contents

### Basic Ring Laws
| Theorem Name | Statement |
|--------|------|
| `my_mul_add` | Distributive law: a * (b + c) = a * b + a * c |
| `my_mul_comm` | Commutativity: a * b = b * a |
| `my_mul_zero` | a * 0 = 0 |
| `my_neg_one_mul` | -1 * a = -a |
| `my_mul_one` | a * 1 = a |

### Ideals
| Theorem Name | Statement |
|--------|------|
| `my_ideal_add_mem` | An ideal is closed under addition |
| `my_ideal_mul_mem_left` | An ideal is closed under left multiplication |
| `my_mem_span_singleton_self` | a ∈ (a) (a belongs to the ideal it generates) |
| `my_span_one` | (1) = R |
| `my_span_singleton_eq_top` | (a) = R ↔ a is a unit |
| `my_exists_le_maximal` | Every proper ideal is contained in a maximal ideal |

### Quotient Rings
| Theorem Name | Statement |
|--------|------|
| `my_quotient_eq_zero_iff` | mk I a = 0 ↔ a ∈ I |
| `my_quotient_mk_eq_iff` | mk I a = mk I b ↔ a - b ∈ I |

### Correspondence Between Prime and Maximal Ideals
| Theorem Name | Statement |
|--------|------|
| `my_isPrime_iff_isDomain` | I is a prime ideal ↔ R ⧸ I is an integral domain |
| `my_isMaximal_iff_isField` | I is a maximal ideal ↔ R ⧸ I is a field |
| `my_isMaximal_isPrime` | Maximal ideal → prime ideal |

### Concrete Examples in ℤ
| Theorem Name | Statement |
|--------|------|
| `span_five_isPrime` | 5ℤ is a prime ideal of ℤ |
| `ker_intCast_eq_span` | ker(ℤ → ZMod n) = nℤ |

## Learning Points

- **Ideal**: A subset I of a ring R that is closed under addition and left/right multiplication.
  In Lean it is represented by the type `Ideal R`, implemented as `Submodule R R`.

- **Quotient Ring**: The quotient by an ideal I is written `R ⧸ I`.
  `Ideal.Quotient.mk I : R →+* R ⧸ I` is the canonical projection.

- **Key Correspondence (Fundamental Theorem of Ring Theory)**:
  ```
  I is a prime ideal   ↔  R ⧸ I is an integral domain
  I is a maximal ideal ↔  R ⧸ I is a field
  Maximal ideal ⊂ Prime ideal  (every field is an integral domain)
  ```

- **Examples in ℤ**:
  - `5ℤ` is a prime ideal (5 is prime) → `ℤ/5ℤ ≅ ZMod 5` is a field
  - `4ℤ` is not a prime ideal (4 = 2 × 2) → `ZMod 4` has zero divisors (2 * 2 = 0)
  - `ker(ℤ → ZMod n) = nℤ` (First isomorphism theorem: `ℤ/nℤ ≅ ZMod n`)

## Examples of Zero Divisors

```
ZMod 4:  2 * 2 = 0,  2 ≠ 0  → not an integral domain
ZMod 6:  3 * 2 = 0,  3 ≠ 0  → not an integral domain
ZMod 5:  no zero divisors    → a field (5 is prime)
```
