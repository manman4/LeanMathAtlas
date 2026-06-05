# 難易度マップ

> **Read in English →** [ROADMAP.md](ROADMAP.md)

> **凡例**
> - ★☆☆ Beginner — 1タクティクの証明・基本的な帰納法
> - ★★☆ Intermediate — 複数ステップの証明・ライブラリ検索が必要
> - ★★★ Advanced — オリジナルの補題・Mathlib の深い利用

---

## Introduction

| モジュール | ファイル | トピック |
|----------|--------|--------|
| Tactics | [`Tactics.lean`](LeanMathAtlas/Tactics.lean) · [解説](docs/ja/Tactics.md) | `ring` `omega` `simp` など自動タクティクスの使い方 |
| Exercises | [`Exercises.lean`](LeanMathAtlas/Exercises.lean) | `sorry` を埋めて最初の証明を体験する — Lean 4 の雰囲気をつかむ入口 |

> **ここから始めよう。** まず [docs/ja/Tactics.md](docs/ja/Tactics.md) でタクティクスの使い分けを確認し、`Exercises.lean` の `sorry` を消していくことで証明スタイルに慣れることができます。

---

## ★☆☆ Beginner

| モジュール | ファイル | トピック |
|----------|--------|--------|
| 命題論理 | [`Logic/Propositional.lean`](LeanMathAtlas/Logic/Propositional.lean) · [解説](docs/ja/Logic/Propositional.md) | intro/elim, ∧ ∨ ¬ ↔, ド・モルガン |
| 自然数 | [`NumberTheory/NaturalNumbers.lean`](LeanMathAtlas/NumberTheory/NaturalNumbers.lean) · [解説](docs/ja/NumberTheory/NaturalNumbers.md) | 帰納法・算術の基本法則・偶奇 |
| 代数的恒等式 | [`Algebra/BasicIdentities.lean`](LeanMathAtlas/Algebra/BasicIdentities.lean) · [解説](docs/ja/Algebra/BasicIdentities.md) | 展開・因数分解・二次不等式・因数定理・剰余定理 |
| 数列・級数 | [`Algebra/Sequences.lean`](LeanMathAtlas/Algebra/Sequences.lean) · [解説](docs/ja/Algebra/Sequences.md) | 等差・等比数列、ガウス・平方和・立方和 |
| 三角関数 | [`Analysis/Trigonometry.lean`](LeanMathAtlas/Analysis/Trigonometry.lean) · [解説](docs/ja/Analysis/Trigonometry.md) | ピタゴラスの恒等式・加法定理・2倍角公式 |
| 二項定理 | [`Combinatorics/BinomialTheorem.lean`](LeanMathAtlas/Combinatorics/BinomialTheorem.lean) · [解説](docs/ja/Combinatorics/BinomialTheorem.md) | 二項係数・パスカルの三角形・二項定理 |

> 全 ★☆☆ モジュールは**実装済み**です。

---

## ★★☆ Intermediate

| モジュール | ファイル | トピック |
|----------|--------|--------|
| 素数と整除性 | [`NumberTheory/Primes.lean`](LeanMathAtlas/NumberTheory/Primes.lean) · [解説](docs/ja/NumberTheory/Primes.md) | `Nat.Prime`、GCD、互いに素、ユークリッドの定理 |
| 複素数 | [`Algebra/Complex.lean`](LeanMathAtlas/Algebra/Complex.lean) · [解説](docs/ja/Algebra/Complex.md) | `ℂ`、絶対値、共役、オイラーの公式、ド・モアブル |
| 微分 | [`Analysis/Derivatives.lean`](LeanMathAtlas/Analysis/Derivatives.lean) · [解説](docs/ja/Analysis/Derivatives.md) | `HasDerivAt`、和・積・合成微分、三角関数の微分 |
| 合同算術 | [`NumberTheory/Modular.lean`](LeanMathAtlas/NumberTheory/Modular.lean) · [解説](docs/ja/NumberTheory/Modular.md) | `ZMod`、フェルマーの小定理 |
| ベクトル | [`LinearAlgebra/Vectors.lean`](LeanMathAtlas/LinearAlgebra/Vectors.lean) · [解説](docs/ja/LinearAlgebra/Vectors.md) | 内積、ノルム、コーシー・シュワルツ不等式 |
| 極限と連続性 | [`Analysis/Limits.lean`](LeanMathAtlas/Analysis/Limits.lean) · [解説](docs/ja/Analysis/Limits.md) | ε-δ定義、`Filter.Tendsto` |

> 全 ★★☆ モジュールは**実装済み**です。

---

## ★★★ Advanced

| モジュール | ファイル | トピック |
|----------|--------|--------|
| 群論 | [`Algebra/Groups.lean`](LeanMathAtlas/Algebra/Groups.lean) · [解説](docs/ja/Algebra/Groups.md) | `Group`、部分群、ラグランジュの定理 |
| 環論 | [`Algebra/Rings.lean`](LeanMathAtlas/Algebra/Rings.lean) · [解説](docs/ja/Algebra/Rings.md) | `Ring`、イデアル、商環 |
| 積分論 | [`Analysis/Integration.lean`](LeanMathAtlas/Analysis/Integration.lean) · [解説](docs/ja/Analysis/Integration.md) | `MeasureTheory.integral`、微積分の基本定理 |
| 位相空間論 | [`Topology/Basic.lean`](LeanMathAtlas/Topology/Basic.lean) · [解説](docs/ja/Topology/Basic.md) | 開集合、コンパクト性、連結性 |

> 全 ★★★ モジュールは**実装済み**です。

---

## 自動証明された定理

`auto_prove.py` によって証明された定理は
[`LeanMathAtlas/ProvedTheorems.lean`](LeanMathAtlas/ProvedTheorems.lean) にまとめられています。
