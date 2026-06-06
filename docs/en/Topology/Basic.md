# Topological Spaces: Open Sets, Compactness, and Connectedness

> **日本語で読む →** [Basic.md](../../ja/Topology/Basic.md)

Corresponding Lean file: `LeanMathAtlas/Topology/Basic.lean`

## Contents

### Open and Closed Sets
| Theorem name | Description |
|--------|------|
| `my_isOpen_univ` | The whole space is open |
| `my_isOpen_empty` | The empty set is open |
| `my_isOpen_inter` | A finite intersection of open sets is open |
| `my_isOpen_iUnion` | An arbitrary union of open sets is open |
| `my_isClosed_compl_iff` | s is open ↔ sᶜ is closed (duality) |
| `my_isClosed_union` | A finite union of closed sets is closed |
| `my_isClosed_iInter` | An arbitrary intersection of closed sets is closed |

### Continuous Maps
| Theorem name | Description |
|--------|------|
| `my_isOpen_preimage` | The preimage of an open set under a continuous map is open |
| `my_continuous_comp` | The composition of continuous maps is continuous |
| `my_continuous_id` | The identity map is continuous |
| `my_continuous_const` | A constant map is continuous |

### Compact Sets
| Theorem name | Description |
|--------|------|
| `my_isCompact_elim_finite_subcover` | Finite cover property: every open cover has a finite subcover |
| `my_isCompact_inter_right` | Compact ∩ Closed = Compact |
| `my_isCompact_of_isClosed_subset` | A closed subset of a compact set is compact |
| `my_isCompact_image` | The image of a compact set under a continuous map is compact |

### Connected Sets
| Theorem name | Description |
|--------|------|
| `my_isConnected_singleton` | A singleton is connected |
| `my_isConnected_union` | The union of connected sets with a common point is connected |
| `my_isConnected_image` | The image of a connected set under a continuous map is connected |
| `my_isConnected_univ` | The whole connected space is connected |

## Learning Points

- The definition of a topological space uses an axiomatic approach via a family of open sets:
  - The whole space and the empty set are open
  - Arbitrary unions are open (including infinite unions)
  - Finite intersections are open
  - Closed sets are defined as complements of open sets

- **Asymmetry between open and closed sets**:
  - Infinite union of open sets → open (OK)
  - Infinite union of closed sets → not necessarily closed (e.g., ⋃ₙ [1/n, 1] = (0, 1])
  - Finite intersection of closed sets → closed (OK)
  - Infinite intersection of open sets → not necessarily open (e.g., ⋂ₙ (-1/n, 1/n) = {0})

- **Compact sets**: Heine-Borel theorem — in ℝⁿ, "bounded and closed = compact". Lean uses the general definition via open covers.

- **Connected sets**: A nonempty set that cannot be split into two disjoint open sets. Connectedness of intervals is the basis of the Intermediate Value Theorem.

## Concrete Examples

```
Important facts in ℝ:
  isCompact_Icc  : IsCompact (Icc a b)   -- [a,b] is compact
  isConnected_Icc : IsConnected (Icc a b) -- [a,b] is connected (a ≤ b)
  ConnectedSpace ℝ                       -- ℝ is a connected space

Applications:
  The image sin([0, π]) of sin is both compact and connected ✓
  [0,1] ∩ [1/2, 2] = [1/2, 1] is compact ✓
```
