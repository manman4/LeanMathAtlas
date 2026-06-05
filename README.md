# LeanMathAtlas

A collection of Lean 4 theorem proofs organized by mathematical subject.
Proofs are verified by the Lean compiler and accumulated in
`LeanMathAtlas/ProvedTheorems.lean` via an automated prover (`auto_prove.py`).

## Contents

```
LeanMathAtlas/
  Algebra/
    BasicIdentities.lean   # Expansion, factoring, quadratic inequalities, factor/remainder theorems
    Sequences.lean         # Arithmetic/geometric sequences, summation formulas (Gauss, squares, cubes)
  Analysis/
    Trigonometry.lean      # Pythagorean identity, addition formulas, double-angle formulas
  Combinatorics/
    BinomialTheorem.lean   # Binomial coefficients, Pascal's triangle, binomial theorem
  NumberTheory/
    NaturalNumbers.lean    # Induction, basic arithmetic laws, parity
  Logic/
    Propositional.lean     # Intro/elim rules, De Morgan's laws, tautologies
  ProvedTheorems.lean      # Auto-generated: theorems proved by auto_prove.py

docs/ja/                   # Japanese explanations (one Markdown file per module)
tools/
  auto_prove.py            # Automated theorem prover via Lean REPL
  benchmark.py             # Accuracy benchmark
```

## Requirements

| Tool | Version |
|------|---------|
| Lean 4 | `v4.27.0` (see `lean-toolchain`) |
| Mathlib | `v4.27.0` |
| Python | 3.11+ |

### Install Lean / elan

```bash
curl https://elan.lean-lang.org/elan-init.sh | sh
```

### Fetch dependencies

```bash
lake update
```

This downloads Mathlib and the REPL package (~several minutes on first run).

### Build

```bash
lake build
```

## [Difficulty Map →](ROADMAP.md)

## How to study

### 1. Start with the exercises (introduction)

`LeanMathAtlas/Exercises.lean` contains 10 holes marked `sorry`.
Open the file and replace each `sorry` with a valid tactic proof —
this is the fastest way to get a feel for Lean 4.

```bash
code LeanMathAtlas/Exercises.lean
```

```lean
-- before
example (P Q : Prop) (hp : P) (_hq : Q) : P := by
  sorry

-- after
example (P Q : Prop) (hp : P) (_hq : Q) : P := by
  exact hp
```

Place the cursor on a `sorry` to see the current goal in the Lean InfoView panel.

### 2. Read the proof files

Each file under `LeanMathAtlas/` focuses on one topic.
Open a file in VS Code with the Lean 4 extension — hover over any term to see
its type.

```bash
code LeanMathAtlas/Algebra/BasicIdentities.lean
```

Japanese notes explaining each theorem in terms of standard curricula are in
`docs/ja/<Subject>/<File>.md`.

### 3. Run the automated prover

> Detailed guide: [AUTO_PROVE.md](tools/AUTO_PROVE.md)

`tools/auto_prove.py` takes a theorem statement, tries a set of tactics via the Lean
REPL, and saves any successful proof to `ProvedTheorems.lean`.

```bash
# Run the built-in test suite (7 theorems)
python3 tools/auto_prove.py

# Prove a custom theorem
python3 tools/auto_prove.py "theorem my_thm (a b : ℝ) : (a - b)^2 ≥ 0"
```

Proved theorems are cached in `.proof_index.json` — subsequent runs return
instantly for already-proved statements.

## License

[MIT License](LICENSE)

> **Note on dependencies**: This repository imports
> [Mathlib](https://github.com/leanprover-community/mathlib4) (Apache 2.0)
> and the [Lean REPL](https://github.com/leanprover-community/repl) (Apache 2.0).
> Those licenses apply to their respective packages.
