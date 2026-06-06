# Contributing to LeanMathAtlas

Thank you for your interest in contributing. This guide explains how to add a new module or fix an existing one.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Lean 4 / elan | `v4.27.0` (see `lean-toolchain`) |
| Mathlib | `v4.27.0` |

```bash
# Install elan (Lean version manager)
curl https://elan.lean-lang.org/elan-init.sh | sh

# Fetch Mathlib and other dependencies
lake update

# Verify the build passes
lake build
```

---

## Adding a new module

### 1. Create the Lean file

Place the file under the appropriate subject directory:

```
LeanMathAtlas/
  Algebra/       — ring-theoretic and algebraic topics
  Analysis/      — calculus, limits, integration
  Combinatorics/ — counting, binomial theorem
  LinearAlgebra/ — vectors, matrices
  Logic/         — propositional and predicate logic
  NumberTheory/  — primes, modular arithmetic
  Topology/      — open sets, compactness
```

Name the file after the topic, e.g. `LeanMathAtlas/NumberTheory/ChineseRemainder.lean`.

**Conventions:**
- Begin with a `/-! ... -/` doc comment describing the module.
- Prefix custom theorem names with `my_` (e.g. `my_gcd_comm`).
- Every theorem must compile — no `sorry` in non-exercise files.

### 2. Register the import

Add the new module to `LeanMathAtlas.lean`:

```lean
import LeanMathAtlas.NumberTheory.ChineseRemainder
```

Confirm the full build still passes:

```bash
lake build
```

### 3. Write the documentation

Create matching notes files for both languages:

- `docs/ja/<Subject>/<Topic>.md` — Japanese explanation
- `docs/en/<Subject>/<Topic>.md` — English explanation

Each file should cover:
- A table of theorems proved in the module
- Key learning points / intuition
- Concrete examples

Add a cross-link at the top of each file pointing to the other language:

```markdown
# Title

> **Read in English →** [Topic.md](../../en/Subject/Topic.md)
```

```markdown
# タイトル

> **Read in English →** [Topic.md](../../en/Subject/Topic.md)

> **日本語で読む →** [Topic.md](../../ja/Subject/Topic.md)
```

### 4. Update ROADMAP and CHANGELOG

**ROADMAP.md** — add a row to the appropriate difficulty section:

```markdown
| Topic Name | [`Subject/Topic.lean`](LeanMathAtlas/Subject/Topic.lean) · [Notes](docs/en/Subject/Topic.md) | brief description |
```

**ROADMAP.ja.md** — add the same row in Japanese with a `[解説]` link:

```markdown
| トピック名 | [`Subject/Topic.lean`](LeanMathAtlas/Subject/Topic.lean) · [解説](docs/ja/Subject/Topic.md) | 概要 |
```

**CHANGELOG.md** — add an entry at the top of the table:

```markdown
| 0.x.y | YYYY-MM-DD | Add <Topic> (<brief description>) |
```

---

## Difficulty levels

| Level | Meaning | Examples |
|-------|---------|---------|
| ★☆☆ Beginner | Single-tactic proofs, basic induction | `rfl`, `ring`, `omega`, `induction` |
| ★★☆ Intermediate | Multi-step proofs, Mathlib search required | `HasDerivAt`, `Nat.Prime`, `ZMod` |
| ★★★ Advanced | Original lemmas, deep Mathlib usage | `Ideal`, `MeasureTheory`, `TopologicalSpace` |

---

## Submitting a pull request

1. Fork the repository and create a branch from `main`.
2. Make your changes following the steps above.
3. Run `lake build` and confirm it passes with no errors.
4. Open a pull request with a clear description of what was added and why.
