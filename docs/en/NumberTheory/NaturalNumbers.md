# Arithmetic and Induction on Natural Numbers

> **日本語で読む →** [NaturalNumbers.md](../../ja/NumberTheory/NaturalNumbers.md)

Corresponding Lean file: `LeanMathAtlas/NumberTheory/NaturalNumbers.lean`

## Contents

### Basics of Induction
| Theorem name | Description |
|--------|------|
| `my_zero_add` | $0+n=n$ (manual proof by induction) |
| `my_add_assoc` | $(a+b)+c = a+(b+c)$ (associativity, by induction) |
| `my_add_comm` | $a+b=b+a$ (commutativity, by induction) |

### Applications of Induction
| Theorem name | Description |
|--------|------|
| `double_eq_two_mul` | $n+n=2n$ |
| `my_zero_le` | $0 \leq n$ |

### Even and Odd Numbers
| Theorem name | Description |
|--------|------|
| `even_add_even` | even + even = even |

## Learning Points

Using Lean's `induction n with | zero => ... | succ k ih => ...` syntax,
the base case and inductive step of mathematical induction are written directly.  
The `omega` tactic automatically solves linear arithmetic over natural numbers and integers.
