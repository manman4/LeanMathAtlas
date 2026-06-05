# 命題論理

対応する Lean ファイル: `LeanMathAtlas/Logic/Propositional.lean`

## 内容

### 基本タクティク一覧
| タクティク | 役割 |
|-----------|------|
| `intro` | ゴールが `P → Q` のとき `P` を仮定に追加 |
| `exact` | ゴールに完全一致する項を与えて証明完了 |
| `apply` | ゴールを後ろ向きに変換 |
| `constructor` | `∧` や `↔` のゴールを分割 |
| `obtain` / `rcases` | 仮定を分解・場合分け |
| `left` / `right` | `∨` ゴールの左右を選択 |

### 証明した命題
| 命題 | 内容 |
|------|------|
| `P → P` | 同一律 |
| `P ∧ Q ↔ Q ∧ P` | 論理積の交換法則 |
| `P ∨ Q → Q ∨ P` | 論理和の交換法則 |
| 対偶 | $(P \to Q) \to (\neg Q \to \neg P)$ |
| ド・モルガン | $\neg(P \lor Q) \to \neg P \land \neg Q$ |
| 分配法則 | $P \land (Q \lor R) \to (P \land Q) \lor (P \land R)$ |
