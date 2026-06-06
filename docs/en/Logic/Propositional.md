# Propositional Logic

> **日本語で読む →** [Propositional.md](../../ja/Logic/Propositional.md)

Corresponding Lean file: `LeanMathAtlas/Logic/Propositional.lean`

## Contents

### Basic Tactics Reference
| Tactic | Role |
|-----------|------|
| `intro` | When the goal is `P → Q`, adds `P` as a hypothesis |
| `exact` | Closes the goal by providing a term that exactly matches it |
| `apply` | Transforms the goal backward |
| `constructor` | Splits a `∧` or `↔` goal |
| `obtain` / `rcases` | Destructs hypotheses / case splits |
| `left` / `right` | Selects the left or right branch of a `∨` goal |

### Proved Propositions
| Proposition | Description |
|------|------|
| `P → P` | Identity law |
| `P ∧ Q ↔ Q ∧ P` | Commutativity of conjunction |
| `P ∨ Q → Q ∨ P` | Commutativity of disjunction |
| Contrapositive | $(P \to Q) \to (\neg Q \to \neg P)$ |
| De Morgan | $\neg(P \lor Q) \to \neg P \land \neg Q$ |
| Distributive law | $P \land (Q \lor R) \to (P \land Q) \lor (P \land R)$ |
