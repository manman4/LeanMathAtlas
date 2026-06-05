# Difficulty Map

> **Legend**
> - ★☆☆ Beginner — single-tactic proofs, basic induction
> - ★★☆ Intermediate — multi-step proofs, library search required
> - ★★★ Advanced — original lemmas, deep Mathlib usage

---

## Introduction

| Module | File | Topics |
|--------|------|--------|
| Tactics | [`Tactics.lean`](LeanMathAtlas/Tactics.lean) · [解説](docs/ja/Tactics.md) | `ring` `omega` `simp` など自動タクティクスの使い方 |
| Exercises | [`Exercises.lean`](LeanMathAtlas/Exercises.lean) | `sorry` を埋めて最初の証明を体験する — Lean 4 の雰囲気をつかむ入口 |

> **Start here.** まず [docs/ja/Tactics.md](docs/ja/Tactics.md) でタクティクスの使い分けを確認し、`Exercises.lean` の `sorry` を消していくことで証明スタイルに慣れることができます。

---

## ★☆☆ Beginner

| Module | File | Topics |
|--------|------|--------|
| Propositional Logic | `Logic/Propositional.lean` | intro/elim, ∧ ∨ ¬ ↔, De Morgan |
| Natural Numbers | `NumberTheory/NaturalNumbers.lean` | induction, arithmetic laws, parity |
| Algebraic Identities | `Algebra/BasicIdentities.lean` | expansion, factoring, quadratic inequalities, factor/remainder theorems |
| Sequences & Series | `Algebra/Sequences.lean` | arithmetic/geometric sequences, Gauss, sum of squares/cubes |
| Trigonometry | `Analysis/Trigonometry.lean` | Pythagorean identity, addition formulas, double-angle formulas |
| Binomial Theorem | `Combinatorics/BinomialTheorem.lean` | binomial coefficients, Pascal's triangle, binomial theorem |

---

## ★★☆ Intermediate

| Module | File | Topics |
|--------|------|--------|
| Primes & Divisibility | [`NumberTheory/Primes.lean`](LeanMathAtlas/NumberTheory/Primes.lean) | `Nat.Prime`, GCD, coprimality, Euclid's theorem |
| Complex Numbers | [`Algebra/Complex.lean`](LeanMathAtlas/Algebra/Complex.lean) | `ℂ`, modulus, conjugate, Euler's formula, de Moivre |
| Derivatives | [`Analysis/Derivatives.lean`](LeanMathAtlas/Analysis/Derivatives.lean) | `HasDerivAt`, sum/product/chain rules, trig derivatives |
| Modular Arithmetic | [`NumberTheory/Modular.lean`](LeanMathAtlas/NumberTheory/Modular.lean) · [解説](docs/ja/NumberTheory/Modular.md) | `ZMod`, Fermat's little theorem |
| Vectors | [`LinearAlgebra/Vectors.lean`](LeanMathAtlas/LinearAlgebra/Vectors.lean) · [解説](docs/ja/LinearAlgebra/Vectors.md) | inner product, norm, Cauchy–Schwarz |
| Limits & Continuity | [`Analysis/Limits.lean`](LeanMathAtlas/Analysis/Limits.lean) · [解説](docs/ja/Analysis/Limits.md) | ε-δ definition, `Filter.Tendsto` |

> All ★★☆ modules are **implemented**. ★★★ modules are planned.

---

## ★★★ Advanced

| Module | File | Topics |
|--------|------|--------|
| Group Theory | [`Algebra/Groups.lean`](LeanMathAtlas/Algebra/Groups.lean) · [解説](docs/ja/Algebra/Groups.md) | `Group`, subgroups, Lagrange's theorem |
| Ring Theory | [`Algebra/Rings.lean`](LeanMathAtlas/Algebra/Rings.lean) · [解説](docs/ja/Algebra/Rings.md) | `Ring`, ideals, quotient rings |
| Integration | `Analysis/Integration.lean` | `MeasureTheory.integral`, fundamental theorem |
| Topology | [`Topology/Basic.lean`](LeanMathAtlas/Topology/Basic.lean) · [解説](docs/ja/Topology/Basic.md) | open sets, compactness, connectedness |

> All ★★★ modules are **planned**.

---

## Auto-proved theorems

Theorems successfully proved by `auto_prove.py` are collected in
[`LeanMathAtlas/ProvedTheorems.lean`](LeanMathAtlas/ProvedTheorems.lean).
