# Tactics Guide

> **日本語で読む →** [Tactics.md](../ja/Tactics.md)

Corresponding Lean file: `LeanMathAtlas/Tactics.lean`

In Lean 4, the instructions written after `by` are called **tactics**.
This file focuses on tactics that automatically complete proofs for you.

---

## Automated Proof Tactics

These tactics **inspect the shape of the goal and close it by performing internal automatic computation**.
The syntax is simply `by <tactic name>` — you do not need to write the computation steps yourself.

---

### `ring` — Algebraic Equalities

**What it does**: Automatically proves equalities that can be verified by algebraic computation,
such as commutativity, associativity, distributivity, expansion, and factorization.

```lean
example (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by ring
example (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2  := by ring
example (a b c : ℝ) : a * (b + c) = a*b + a*c       := by ring
```

**Applicable types**: Any type with a ring structure, such as `ℕ`, `ℤ`, `ℚ`, `ℝ`, `ℂ`, etc.

**Limitations**:
- Inequalities (`≤`, `<`)
- Natural number equalities involving division (`a * b = b * a` is solvable by `ring`, but `a / b` is not)

---

### `omega` — Arithmetic on Natural Numbers and Integers

**What it does**: Automatically proves **equalities and inequalities** over integers and natural numbers
using a linear arithmetic algorithm. Applicable within the scope of addition, subtraction, and constant multiples.

```lean
example (n : ℕ) : n + 0 = n               := by omega
example (n : ℕ) : n ≤ n + 1               := by omega
example (a b : ℤ) (h : a ≤ b) : a ≤ b + 1 := by omega
example (n : ℕ) (h : n ≥ 1) : n > 0       := by omega
```

**Applicable types**: `ℕ`, `ℤ`

**Limitations**:
- Inequalities involving multiplication or exponentiation (`n * m ≤ ...`, etc.) → use `linarith` or `nlinarith`
- Inequalities over reals or rationals → use `linarith`

---

### `simp` — Simplification with Known Lemmas

**What it does**: Applies simplification rules registered in Mathlib (`@[simp]` lemmas) one after another
to simplify the goal to `True` or a trivially obvious form.

```lean
example : ([] : List ℕ).length = 0 := by simp
example (n : ℕ) : n + 0 = n        := by simp
example : True                      := by simp
```

You can also add specific lemmas:

```lean
-- Using Finset.sum_range_succ as an additional simp rule
example : ∑ k ∈ Finset.range 3, k = 3 := by simp [Finset.sum_range_succ]
```

**Note**: It is not shown which lemmas were used, so it can be unclear why the proof went through.
Use `simp?` to find out which lemmas were applied.

```lean
example (n : ℕ) : n + 0 = n := by simp?
-- → Try this: simp only [Nat.add_zero]
```

---

### `decide` — Verification by Finite Computation

**What it does**: Proves propositions that reduce to a finite computation by actually carrying out the computation.

```lean
example : Nat.Prime 7       := by decide   -- checks whether 7 is prime by computation
example : ¬ Nat.Prime 4     := by decide   -- checks that 4 is not prime
example : 2 + 3 = 5         := by decide
```

**Note**: Do not use this for large numbers (computation time will explode).

---

### `norm_num` — Numerical Equalities and Inequalities

**What it does**: Proves equalities, inequalities, and primality tests involving concrete numerical values by computation.

```lean
example : (7 : ℤ) * 8 = 56       := by norm_num
example : (10 : ℕ) ≠ 11          := by norm_num
example : (2 : ℝ) > 0            := by norm_num
```

It handles larger numbers than `decide`.

---

### `linarith` / `nlinarith` — Inequalities

**What it does**: Derives inequalities from hypotheses.

| Tactic | Scope |
|---|---|
| `linarith` | Linear inequalities (addition and constant multiples only) |
| `nlinarith` | Nonlinear inequalities (involving multiplication and squaring) |

```lean
-- linarith: derives the conclusion from a combination of hypotheses
example (a b : ℝ) (h1 : a ≤ 3) (h2 : 3 ≤ b) : a ≤ b := by linarith

-- nlinarith: inequalities involving squares
example (a b : ℝ) : 2 * a * b ≤ a^2 + b^2 := by nlinarith [sq_nonneg (a - b)]
```

---

## Summary: Choosing the Right Tactic

```
Shape of the goal to prove
  │
  ├─ Equality ( = )
  │    ├─ Algebraic (expansion, factorization)      → ring
  │    ├─ Addition/subtraction over ℕ or ℤ          → omega
  │    └─ Concrete numerical values                 → norm_num / decide
  │
  └─ Inequality ( ≤ < ≥ > )
       ├─ Linear over ℕ or ℤ                        → omega
       ├─ Linear over ℝ                             → linarith
       └─ Nonlinear over ℝ (multiplication, squares)→ nlinarith
```

If any of these closes the goal, the proof is complete. A good order to try is `ring` → `omega` → `simp`.

---

## Manual Tactics (Reference)

When automated tactics cannot solve the goal, combine the following.

| Tactic | Role |
|---|---|
| `intro h` | For a goal `P → Q`, introduces `P` as hypothesis `h` |
| `exact h` | Closes the goal when hypothesis `h` exactly matches it |
| `apply f` | Applies lemma `f` to transform the goal |
| `rw [h]` | Rewrites the goal using equation `h` |
| `have h := ...` | Creates an auxiliary proposition mid-proof |
| `induction n with` | Induction on a natural number `n` |
| `obtain ⟨a, b⟩ := h` | Destructs `h` and extracts its components |
| `rcases h with ha \| hb` | Case-splits `h : P ∨ Q` |
| `constructor` | Splits `P ∧ Q` into two goals |
