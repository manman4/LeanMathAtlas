# Changelog

All notable changes to this project will be documented in this file.

---

## [Unreleased] — develop/v0.0.3

### Changed
- Moved tooling (`auto_prove.py`, `benchmark.py`, `AUTO_PROVE.md`, `BENCHMARK.md`) into `tools/` directory
- Updated all markdown files to reflect new `tools/` structure

---

## [0.0.2] — 2026-06-06

### Added
- Lean 4 proof files for all ★☆☆ Beginner modules:
  - `Algebra/BasicIdentities.lean` — expansion, factoring, quadratic inequalities
  - `Algebra/Sequences.lean` — arithmetic/geometric sequences, Gauss, sum of squares/cubes
  - `Analysis/Trigonometry.lean` — Pythagorean identity, addition/double-angle formulas
  - `Combinatorics/BinomialTheorem.lean` — binomial coefficients, Pascal's triangle
  - `NumberTheory/NaturalNumbers.lean` — induction, arithmetic laws, parity
  - `Logic/Propositional.lean` — intro/elim rules, De Morgan's laws, tautologies
- Lean 4 proof files for 3/6 ★★☆ Intermediate modules:
  - `NumberTheory/Primes.lean` — `Nat.Prime`, GCD, Euclid's theorem
  - `Algebra/Complex.lean` — `ℂ`, modulus, conjugate, Euler's formula, de Moivre
  - `Analysis/Derivatives.lean` — `HasDerivAt`, sum/product/chain rules, trig derivatives
- `Basic.lean`, `Tactics.lean`, `Exercises.lean`, `ProvedTheorems.lean`
- `auto_prove.py` — automated theorem prover via Lean REPL
- `benchmark.py` — accuracy benchmark
- `AUTO_PROVE.md` — detailed usage guide for auto_prove.py
- Japanese explanation docs (`docs/ja/`) for all implemented modules
- `README.ja.md` — Japanese README

---

## [0.0.1] — 2026-06-06

### Added
- `README.md` and `ROADMAP.md` (difficulty map: ★☆☆ / ★★☆ / ★★★)
- `.gitignore` for Lean 4 / Lake build artifacts, secrets, editor files
- `.claude/settings.json` — Claude Code security settings for public repo
  - `PreToolUse` hook (`.claude/hooks/check-cmd.sh`) blocking force-push, `rm -rf`, download-to-execute pipelines, and secret file access
- Local pre-commit hook (`.git/hooks/pre-commit`) blocking personal name strings
