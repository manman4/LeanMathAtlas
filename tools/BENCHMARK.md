# auto_prove.py 評価レポート

auto_prove.py の証明自動化精度を `benchmark.py` で計測した記録。

---

## 評価の目的

タクティクスの追加・変更が実際の精度にどう影響するかを定量的に把握する。

---

## 使用した問題セット（46 件）

`benchmark.py` に定義された 5 カテゴリ：

### logic（命題論理）— 16 件

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

### algebra（代数・算術）— 8 件

`(a+b)^2`, `(a-b)^2`, 差の積公式, `(a+b)^3`,
`a+b=b+a` (ℕ), `(a+b)+c=a+(b+c)` (ℕ), `n ≤ n+1`, `a ≤ b ∧ b ≤ a → a = b` (ℤ)

### induction（帰納法）— 2 件

ガウスの和 `2·∑k = n(n+1)`、平方和 `6·∑k² = n(n+1)(2n+1)`

### algebra（代数・算術）— 12 件

`(a+b)^2`, `(a-b)^2`, 差の積公式, `(a+b)^3`, `(a-b)^3`,
`a+b=b+a` (ℕ), `(a+b)+c=a+(b+c)` (ℕ), `n ≤ n+1`, `a ≤ b ∧ b ≤ a → a = b` (ℤ),
AM-GM 2変数 `2ab ≤ a²+b²`, `0 ≤ a²`, `ab = ba` (ℝ)

### induction（帰納法）— 5 件

ガウスの和 `2·∑k = n(n+1)`、平方和 `6·∑k² = n(n+1)(2n+1)`、
立方和 `4·∑k³ = (n(n+1))²`、等比和 `∑2^k + 1 = 2^(n+1)`、奇数和 `∑(2k+1) = n²`

### hard（多段 have）— 8 件

| 定理 | 内容 | 結果 |
|---|---|---|
| `bench_hard_deriv` | `HasDerivAt (2·sin) (2·cos a) a` | ✓ DERIV_TEMPLATES |
| `bench_hard_prime_inf` | `∀ n, ∃ p, n ≤ p ∧ Nat.Prime p` | ✓ exact? |
| `bench_hard_sqrt` | `√(a²) = a` | ✓ exact? |
| `bench_hard_cont_comp` | `Continuous f → Continuous g → Continuous (f∘g)` | ✓ fun_prop |
| `bench_hard_chain` | chain rule `sin(2x)` | ✗ mul_comm の向き不一致 |
| `bench_hard_irrational_sqrt2` | `Irrational √2` | ✓ exact? |
| `bench_hard_emod` | `a % b % c = a % c` (c∣b) | ✓ exact? |
| `bench_hard_card_filter` | `card {k < 2n \| k % 2 = 0} = n` | ✗ Finset 操作 |

### competition（競技数学）— 5 件

| 定理 | 内容 | 結果 |
|---|---|---|
| `bench_comp_cauchy_schwarz` | `(∑ fᵢgᵢ)² ≤ (∑ fᵢ²)(∑ gᵢ²)` | ✓ exact? |
| `bench_comp_wilson` | `(p-1)! ≡ -1 (mod p)` | ✗ haveI 後も exact? 未ヒット |
| `bench_comp_pigeonhole` | `m < n → f: Fin n → Fin m` は衝突する | ✓ FINTYPE_TEMPLATES |
| `bench_comp_fermat` | `a^p = a` in ZMod p | ✓ haveI Fact + exact? |
| `bench_comp_am_gm3` | `abc ≤ ((a+b+c)/3)³` | ✗ nlinarith witness が必要 |

---

## 精度変化の記録

### ver.1（初期実装）— 一発タクティクスのみ

フェーズ1のみ: `ring` / `omega` / `induction` テンプレート / `exact?` / `simp?`

| カテゴリ | 正解数 | 備考 |
|---|---|---|
| logic | 0/16 | `tauto` が未収録 |
| algebra | 8/8 | `ring` / `omega` で全件 |
| induction | 2/2 | テンプレートで全件 |
| hard | 0/2 | — |
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
| logic | 16/16 | `tauto` が全件解決（BFS 不要） |
| algebra | 8/8 | 変わらず |
| induction | 2/2 | 変わらず |
| hard | 1/2 | `bench_hard_prime_inf` → `exact fun n => Nat.exists_infinite_primes n` |
| **合計** | **27/28 (96%)** | |

> 全 142 件の推計を **~70〜75%** に上方修正（論理ファイルが 20% → 100%）

---

### ver.3（イテラティブ BFS 追加）— 2026-06-05

**変更内容**:
- フェーズ2として `prove_iterative()` を追加
- REPL の tactic mode（`{"tactic": t, "proofState": N}`）を使い、1タクティクスずつ適用
- BFS で深さ 6 / 時間 30 秒を上限に証明列を探索

**結果**: ver.2 と同じ 27/28（logic カテゴリは ver.2 の `tauto` がすでに全件解決しており BFS の出番なし）

---

### ver.4〜ver.5（問題セット拡張 + dry_run + HasDerivAt テンプレート）— 2026-06-06

**変更内容**:
- `dry_run=True` モード追加（ProvedTheorems.lean に書かずベンチマーク専用）
- `import Mathlib` を dry_run 時に使用（Tactic のみより広い補題にアクセス）
- DERIV_TEMPLATES 追加（HasDerivAt 系の一発証明）
- `fun_prop`, `norm_cast` 追加
- algebra×12, induction×5, hard×8 に拡張（計 41 件）

**結果**: 39/41 → 最終 **39/41 (95%)** (test_hash: 14d89aa3)

---

### ver.6（competition カテゴリ追加）— 2026-06-06

**変更内容**: competition×2（Cauchy-Schwarz, Wilson）追加、bench_log に competition 列

**結果**: 40/43 (93%)、Cauchy-Schwarz は `Finset.sum_mul_sq_le_sq_mul_sq` で自動解決

---

### ver.7（competition×5 に拡張）— 2026-06-06

**変更内容**: Pigeonhole, Fermat, AM-GM 3変数 を追加（計 46 件）

**結果**: 40/46 (87%)（Fermat は未解決）

---

### ver.8（haveI Fact typeclass 追加）— 2026-06-06

**変更内容**: フェーズ 1.5 として `haveI : Fact (Nat.Prime p) := ⟨hp⟩` 前置 + `exact?` を追加

**結果**: **41/46 (89%)**、`bench_comp_fermat` が解決（ZMod.pow_card）

---

### ver.9（FINTYPE_TEMPLATES + Phase 1.5 拡張 + Phase 1.6 apply? 追加）— 2026-06-06

**変更内容**:
- FINTYPE_TEMPLATES 追加: `apply Fintype.exists_ne_map_eq_of_card_lt` + `simp [Fintype.card_fin, *]`
  - `∃ + Fin` ゴールに対して DERIV_TEMPLATES と同様に Phase 1 で試す
- Phase 1.5 拡張: `exact?`/`simp?` だけでなく SIMPLE_TACTICS（`simp`, `norm_num` 等）も試す
- Phase 1.5 堅牢化: `exact?` 結果をエラー有りでも "Try this:" 抽出して個別検証
- Phase 1.5 バグ修正: SIMPLE_TACTICS 成功時の stored proof に preamble を含める
- Phase 1.6 追加: `apply?`/`refine?` → extracted suggestion + `all_goals <closer>` で残ゴールを閉じる汎用フェーズ
- STEP_TACTICS に `Fintype.exists_ne_map_eq_of_card_lt`, `simp [Fintype.card_fin]` を追加

**結果**: **42/46 (91%)**、`bench_comp_pigeonhole` が解決（apply Fintype.exists_ne_map_eq_of_card_lt + simp [Fintype.card_fin, *]）

---

## 現在の未解決問題（2026-06-06 時点）

| 定理 | 失敗理由 | 次のアプローチ案 |
|---|---|---|
| `bench_hard_chain` | sin(2x) の chain rule で `_` 型推論が失敗（convert テンプレート動かず） | 明示的な定数を使ったテンプレート |
| `bench_hard_card_filter` | Finset.card の帰納法が必要 | 専用テンプレート |
| `bench_comp_wilson` | `haveI` 後も `exact?` が `ZMod.wilsons_lemma` を見つけない（exact? タイムアウト疑い） | Mathlib 内検索・代替アプローチ |
| `bench_comp_am_gm3` | `nlinarith` に witness `(a-b)^2` 系が必要 | nlinarith witness 自動生成 |

---

## 解けない壁（原則）

有名でない Mathlib 補題を名指しして組み合わせる証明は自動化不可：

```lean
-- chain rule 典型パターン（mul_comm の向きが一致しないと失敗）
have hf : HasDerivAt (fun x => 2 * x) 2 a := (hasDerivAt_id a).const_mul 2
have hg : HasDerivAt Real.sin (Real.cos (2 * a)) (2 * a) := Real.hasDerivAt_sin _
exact hg.comp a hf
```

---

## 計測結果の記録

`benchmark.py` に `--save <ラベル>` を渡すと、結果が [`bench_log.csv`](bench_log.csv) に自動追記される。

```bash
# 計測して結果を記録する
python3 benchmark.py --save "タクティク追加: aesop"

# suite 名を指定して記録する（デフォルトは "core"）
python3 benchmark.py --save "harder set v1" --suite "hard_v2"

# 記録せず実行するだけ
python3 benchmark.py
```

`bench_log.csv` が精度変化の正本。BENCHMARK.md はその解釈・コンテキストを補足するドキュメント。

`test_hash` 列は問題セット（`ALL` リスト）の内容から自動計算される 8 文字のハッシュ。
**同じ `test_hash` の行だけが比較可能**。ハッシュが変わった場合は問題セットが変更されている。

`elapsed_sec` 列は定理ごとの証明探索時間の**累計**（壁時計ではなく各定理の solve_time の和）。
マシン依存の値だが同一マシン内でのトレンド比較に有用。

### ベンチマークキャッシュ（`.bench_cache.json`）

成功した証明は `.bench_cache.json` に `stmt_hash → {proof, solve_time_sec}` の形式で保存される。
2 回目以降は成功済み定理の Lean 再評価をスキップするため、**未解決問題のみ再試行**される。

- 未解決問題が残る限り Lean 起動（~80s）は避けられない
- 全問解決後の 2 回目は数秒で完了する（理想状態）
- `--clear-cache` フラグで強制再実行可能

初回は Mathlib のロードに約 80 秒かかる。BFS タイムアウトは現在 10 秒（30 秒から短縮済み）。
