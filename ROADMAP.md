# Difficulty Map

> **日本語で読む →** [ROADMAP.ja.md](ROADMAP.ja.md)

> **Legend**
> - ★☆☆ Beginner — single-tactic proofs, basic induction
> - ★★☆ Intermediate — multi-step proofs, library search required
> - ★★★ Advanced — original lemmas, deep Mathlib usage

---

## Introduction

| Module | File | Topics |
|--------|------|--------|
| Tactics | [`Tactics.lean`](LeanMathAtlas/Tactics.lean) | `ring`, `omega`, `simp`, and other automation tactics |
| Exercises | [`Exercises.lean`](LeanMathAtlas/Exercises.lean) | Replace each `sorry` with a real proof — the fastest way into Lean 4 |

> **Start here.** Open `Exercises.lean` and fill in the `sorry` holes to get a feel for Lean 4 proof style.

---

## ★☆☆ Beginner

| Module | File | Topics |
|--------|------|--------|
| Propositional Logic | [`Logic/Propositional.lean`](LeanMathAtlas/Logic/Propositional.lean) | intro/elim, ∧ ∨ ¬ ↔, De Morgan |
| Natural Numbers | [`NumberTheory/NaturalNumbers.lean`](LeanMathAtlas/NumberTheory/NaturalNumbers.lean) | induction, arithmetic laws, parity |
| Algebraic Identities | [`Algebra/BasicIdentities.lean`](LeanMathAtlas/Algebra/BasicIdentities.lean) | expansion, factoring, quadratic inequalities, factor/remainder theorems |
| Sequences & Series | [`Algebra/Sequences.lean`](LeanMathAtlas/Algebra/Sequences.lean) | arithmetic/geometric sequences, Gauss, sum of squares/cubes |
| Trigonometry | [`Analysis/Trigonometry.lean`](LeanMathAtlas/Analysis/Trigonometry.lean) | Pythagorean identity, addition formulas, double-angle formulas |
| Binomial Theorem | [`Combinatorics/BinomialTheorem.lean`](LeanMathAtlas/Combinatorics/BinomialTheorem.lean) | binomial coefficients, Pascal's triangle, binomial theorem |

---

## ★★☆ Intermediate

| Module | File | Topics |
|--------|------|--------|
| Primes & Divisibility | [`NumberTheory/Primes.lean`](LeanMathAtlas/NumberTheory/Primes.lean) | `Nat.Prime`, GCD, coprimality, Euclid's theorem |
| Complex Numbers | [`Algebra/Complex.lean`](LeanMathAtlas/Algebra/Complex.lean) | `ℂ`, modulus, conjugate, Euler's formula, de Moivre |
| Derivatives | [`Analysis/Derivatives.lean`](LeanMathAtlas/Analysis/Derivatives.lean) | `HasDerivAt`, sum/product/chain rules, trig derivatives |
| Modular Arithmetic | [`NumberTheory/Modular.lean`](LeanMathAtlas/NumberTheory/Modular.lean) | `ZMod`, Fermat's little theorem |
| Vectors | [`LinearAlgebra/Vectors.lean`](LeanMathAtlas/LinearAlgebra/Vectors.lean) | inner product, norm, Cauchy–Schwarz |
| Limits & Continuity | [`Analysis/Limits.lean`](LeanMathAtlas/Analysis/Limits.lean) | ε-δ definition, `Filter.Tendsto` |

> All ★★☆ modules are **implemented**.

---

## ★★★ Advanced

| Module | File | Topics |
|--------|------|--------|
| Group Theory | [`Algebra/Groups.lean`](LeanMathAtlas/Algebra/Groups.lean) | `Group`, subgroups, Lagrange's theorem |
| Ring Theory | [`Algebra/Rings.lean`](LeanMathAtlas/Algebra/Rings.lean) | `Ring`, ideals, quotient rings |
| Integration | [`Analysis/Integration.lean`](LeanMathAtlas/Analysis/Integration.lean) | `MeasureTheory.integral`, fundamental theorem |
| Topology | [`Topology/Basic.lean`](LeanMathAtlas/Topology/Basic.lean) | open sets, compactness, connectedness |

> All ★★★ modules are **implemented**.

---

## Auto-proved theorems

Theorems successfully proved by `auto_prove.py` are collected in
[`LeanMathAtlas/ProvedTheorems.lean`](LeanMathAtlas/ProvedTheorems.lean).
