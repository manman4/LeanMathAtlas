# auto_prove.py 評価レポート

auto_prove.py の証明自動化精度を `benchmark.py` で計測した記録。

---

## 評価の目的

タクティクスの追加・変更が実際の精度にどう影響するかを定量的に把握する。

---

## 使用した問題セット（28 件）

`benchmark.py` に定義された 4 カテゴリ：

### A) 論理（命題論理）— 16 件

| 定理 | 内容 |
|---|---|
| `bench_imp_id` | `P → P` |
| `bench_imp_weak` | `P → Q → P` |
| `bench_imp_trans` | `(P → Q) → (Q → R) → (P → R)` |
| `bench_and_intro` | `hp : P, hq : Q ⊢ P ∧ Q` |
| `bench_and_left` | `h : P ∧ Q ⊢ P` |
| `bench_and_right` | `h : P ∧ Q ⊢ Q` |
| `bench_and_comm` | `P ∧ Q → Q ∧ P` |
| `bench_or_inl` | `hp : P ⊢ P ∨ Q` |
| `bench_or_inr` | `hq : Q ⊢ P ∨ Q` |
| `bench_or_comm` | `P ∨ Q → Q ∨ P` |
| `bench_not_false` | `¬False` |
| `bench_contrapos` | `(P → Q) → (¬Q → ¬P)` |
| `bench_absurd_ex` | `P → ¬P → Q` |
| `bench_iff_refl` | `P ↔ P` |
| `bench_iff_mp` | `h : P ↔ Q, hp : P ⊢ Q` |
| `bench_demorgan` | `¬(P ∨ Q) → ¬P ∧ ¬Q` |

### B) 代数・算術 — 8 件

`(a+b)^2`, `(a-b)^2`, 差の積公式, `(a+b)^3`,
`a+b=b+a` (ℕ), `(a+b)+c=a+(b+c)` (ℕ), `n ≤ n+1`, `a ≤ b ∧ b ≤ a → a = b` (ℤ)

### C) 帰納法 — 2 件

ガウスの和 `2·∑k = n(n+1)`、平方和 `6·∑k² = n(n+1)(2n+1)`

### D) 難問（多段 have）— 2 件

| 定理 | 内容 | 期待結果 |
|---|---|---|
| `bench_hard_deriv` | `HasDerivAt (2·sin) (2·cos a) a` | ✗（have 多段が必要） |
| `bench_hard_prime_inf` | `∀ n, ∃ p, n ≤ p ∧ Nat.Prime p` | `exact?` で発見可能か検証 |

---

## 精度変化の記録

### ver.1（初期実装）— 一発タクティクスのみ

フェーズ1のみ: `ring` / `omega` / `induction` テンプレート / `exact?` / `simp?`

| カテゴリ | 正解数 | 備考 |
|---|---|---|
| A) 論理 | 0/16 | `tauto` が未収録 |
| B) 代数 | 8/8 | `ring` / `omega` で全件 |
| C) 帰納法 | 2/2 | テンプレートで全件 |
| D) 難問 | 0/2 | — |
| **合計** | **10/28 (36%)** | |

> 推計: 全 142 件で ~56%（論理ファイルを「ほぼ不可」と過小評価）

---

### ver.2（`tauto` 追加 + 検索タクティクス修正）— 2026-06-05

**変更内容**:
- `SIMPLE_TACTICS` に `tauto` を追加（元から含まれていた — `select_tactics` の通過を確認）
- `extract_try_this` の正規表現を修正（複数行 `Try this:\n  [apply] exact X` に対応）
- `exact?` / `simp?` が抽出失敗した場合はスキップ（`"exact?"` を proof として保存するバグ修正）

| カテゴリ | 正解数 | 備考 |
|---|---|---|
| A) 論理 | 16/16 | `tauto` が全件解決（BFS 不要） |
| B) 代数 | 8/8 | 変わらず |
| C) 帰納法 | 2/2 | 変わらず |
| D) 難問 | 1/2 | `bench_hard_prime_inf` → `exact fun n => Nat.exists_infinite_primes n` |
| **合計** | **27/28 (96%)** | |

> 全 142 件の推計を **~70〜75%** に上方修正（論理ファイルが 20% → 100%）

---

### ver.3（イテラティブ BFS 追加）— 2026-06-05 ← 現在

**変更内容**:
- フェーズ2として `prove_iterative()` を追加
- REPL の tactic mode（`{"tactic": t, "proofState": N}`）を使い、1タクティクスずつ適用
- BFS で深さ 6 / 時間 30 秒を上限に証明列を探索
- 空レスポンス `{}` を誤検知しないよう `goals = resp.get("goals")` で None チェック

**結果**: ver.2 と同じ 27/28（論理定理は ver.2 の `tauto` がすでに全件解決しており BFS の出番なし）

> BFS は「`tauto` / `simp` が届かない中間的な論理証明」に効果を発揮する想定だが、
> 今回のサンプルではフェーズ1が先に全件解決したため差が出なかった。

---

## 解けない壁（変わらず）

有名でない Mathlib 補題を名指しして組み合わせる証明は自動化不可：

```lean
-- Derivatives.lean 典型パターン
have hf : HasDerivAt (fun x => 2 * x) 2 a :=
  (hasDerivAt_id a).const_mul 2
have hg : HasDerivAt Real.sin (Real.cos (2 * a)) (2 * a) :=
  Real.hasDerivAt_sin (2 * a)
exact hg.comp a hf
```

これらは VSCode InfoView でゴール状態を確認しながら手動で書く必要がある。

---

## 計測結果の記録

`benchmark.py` に `--save <ラベル>` を渡すと、結果が [`bench_log.csv`](bench_log.csv) に自動追記される。

```bash
# 計測して結果を記録する
python3 benchmark.py --save "タクティク追加: aesop"

# 記録せず実行するだけ
python3 benchmark.py
```

`bench_log.csv` が精度変化の正本。BENCHMARK.md はその解釈・コンテキストを補足するドキュメント。

`test_hash` 列は問題セット（`ALL` リスト）の内容から自動計算される 8 文字のハッシュ。
**同じ `test_hash` の行だけが比較可能**。ハッシュが変わった場合は問題セットが変更されている。

初回は Mathlib のロードに約 80 秒かかる。キャッシュ済みの定理は即座に返る。
