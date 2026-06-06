# Contributing to LeanMathAtlas

> **日本語で読む →** [CONTRIBUTING.ja.md](CONTRIBUTING.ja.md)

## Setup

```bash
curl https://elan.lean-lang.org/elan-init.sh | sh
lake update
lake build
```

## Adding a new module

Place the Lean file under the appropriate subject directory:

```
LeanMathAtlas/
  Algebra/       — algebraic structures
  Analysis/      — calculus, limits, integration
  Combinatorics/ — counting, binomial theorem
  LinearAlgebra/ — vectors, matrices
  Logic/         — propositional and predicate logic
  NumberTheory/  — primes, modular arithmetic
  Topology/      — open sets, compactness
```

**Conventions:**
- Prefix custom theorem names with `my_` (e.g. `my_gcd_comm`).
- No `sorry` in proof files.
- Confirm `lake build` passes before submitting.

## Submitting a pull request

Open a PR against `main` with a description of what the module covers and why it fits the project. Maintainers will handle documentation and release logistics.
