# auto_prove.py 使い方ガイド

`auto_prove.py` は、定理の文を渡すと Lean 4 の REPL を使って自動で証明を探し、
成功した証明を `LeanMathAtlas/ProvedTheorems.lean` に保存してくれるスクリプトです。

---

> [!WARNING]
> **自動証明できる定理には明確な限界があります。**
>
> フェーズ 2（イテラティブ BFS）でカバーできるもの:
>
> | 証明のパターン | 例 |
> |---|---|
> | `intro` + `exact` / `apply` の連鎖 | `P → Q → P` など単純な命題論理 |
> | `constructor` + 各ゴールを閉じる | `P ∧ Q` の証明 |
> | `left` / `right` + auto tactic | `P ∨ Q` の証明 |
>
> フェーズ 2 でも**見つかりません**:
>
> | 証明のパターン | 例 |
> |---|---|
> | Mathlib の補題を組み合わせる多ステップ証明 | `HasDerivAt.comp`、`Polynomial.dvd_iff_isRoot` など |
> | 帰納法 + 特定の補題が必要な証明 | `Finset.sum_range_succ` を `rw` してから `nlinarith` |
> | `convert`・`congr`・`field_simp` が必要な証明 | 型の不一致を吸収するケース |
>
> これらは VSCode の Lean InfoView でゴール状態を確認しながら**手動で書く**必要があります。
> `✗ proof not found` が出た場合は自動化の限界を超えているサインです。

---

## 目次

1. [何をしてくれるのか](#1-何をしてくれるのか)
2. [事前準備](#2-事前準備)
3. [基本的な使い方](#3-基本的な使い方)
4. [実行結果の見方](#4-実行結果の見方)
5. [自分で定理を渡す](#5-自分で定理を渡す)
6. [どんな定理が証明できるか](#6-どんな定理が証明できるか)
7. [キャッシュの仕組み](#7-キャッシュの仕組み)
8. [証明の保存先](#8-証明の保存先)
9. [制限事項](#9-制限事項)
10. [よくある質問](#10-よくある質問)
11. [自動化の限界](#11-自動化の限界)

---

## 1. 何をしてくれるのか

```
定理の文を入力  →  タクティクスを自動で試す  →  証明を ProvedTheorems.lean に保存
```

内部では次の流れで動いています。

```
auto_prove.py
  │
  ├─ lake exe repl を起動（Lean 4 の対話シェル）
  │
  ├─ sorry でゴール状態を取得
  │    例: ⊢ 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)
  │
  ├─【フェーズ 1】ゴールに合うタクティクスを一発で試す
  │    rfl → ring → omega → exact? / simp? など
  │
  ├─【フェーズ 2】失敗したらイテラティブ BFS（時間制限付き）
  │    1タクティクスずつ適用 → 途中ゴールを見て次を選ぶ
  │    intro h → exact h / constructor → left → ... など
  │    (最大 30 秒 / 深さ 6 ステップ)
  │
  └─ 成功したら ProvedTheorems.lean に追記して終了
```

---

## 2. 事前準備

### 依存ツールの確認

```bash
# Python 3.11 以上
python3 --version

# Lean 4 / lake
lean --version
lake --version
```

### 初回ビルド（初回のみ・数分かかる）

```bash
# プロジェクトのルートで実行
lake build
```

Mathlib のキャッシュがない場合は `lake exe cache get` を先に実行してください。

---

## 3. 基本的な使い方

### 組み込みテストを実行する

引数なしで実行すると、スクリプトに内蔵された 7 つのテスト定理を証明します。

```bash
python3 auto_prove.py
```

**出力例：**

```
[run] 7 theorems (0 cached / 7 uncached)
  [repl] Loading Mathlib + ProvedTheorems (~80s)...

────────────────────────────────────────────────────────────
target: theorem t1 : (1:ℕ) + 1 = 2
  goal: ⊢ 1 + 1 = 2
  ✓ by
    rfl

────────────────────────────────────────────────────────────
target: theorem t6 (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)
  goal: ⊢ 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)
  ✓ by
    induction n with
      | zero => simp
      | succ m ih => nlinarith [ih]

────────────────────────────────────────────────────────────
total: 7 passed / 0 failed / 62.6s
  → saved to LeanMathAtlas/ProvedTheorems.lean
```

> **メモ**: 初回は Lean REPL の起動と Mathlib のロードに **約 80 秒** かかります。
> 2 回目以降はキャッシュのおかげで既証明の定理をスキップするので速くなります。

---

## 4. 実行結果の見方

各定理について次の情報が表示されます。

| 表示 | 意味 |
|------|------|
| `target:` | 入力した定理の文 |
| `goal:` | Lean が認識したゴール状態（`⊢` 以降が証明すべき命題） |
| `✓ by ...` | 成功したタクティクス |
| `✗ proof not found` | すべてのタクティクスを試したが証明できなかった |

最後の行に合計の成功数・失敗数・実行時間が出ます。

---

## 5. 自分で定理を渡す

### コマンドライン引数で渡す

```bash
python3 auto_prove.py "theorem my_thm (a b : ℝ) : (a - b)^2 ≥ 0"
```

- ダブルクォートで囲んで渡してください。
- `theorem 名前` の形式で書く必要があります。

**渡せる形式の例：**

```bash
# 自然数の等式
python3 auto_prove.py "theorem add_comm_ex (a b : ℕ) : a + b = b + a"

# 整数の代数
python3 auto_prove.py "theorem sq_diff (a b : ℤ) : a^2 - b^2 = (a + b) * (a - b)"

# 実数の不等式
python3 auto_prove.py "theorem am_gm_sq (a b : ℝ) : 2 * a * b ≤ a^2 + b^2"

# Σ を使った公式（帰納法で証明）
python3 auto_prove.py "theorem sum_cubes (n : ℕ) : 4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2"
```

### 複数の定理をまとめて渡す

現在のスクリプトはコマンドライン引数を 1 つしか受け取りません。
複数まとめて試したい場合は、スクリプト末尾の `TESTS` リストに追記して引数なしで実行する方法が手軽です。

```python
# auto_prove.py の TESTS リストに追記
TESTS = [
    ...
    "theorem my_thm1 (n : ℕ) : n * 2 = 2 * n",
    "theorem my_thm2 (a b : ℝ) : a^2 + b^2 ≥ 0",
]
```

---

## 6. どんな定理が証明できるか

スクリプトは以下のタクティクスを自動で試します。

### シンプルなタクティクス

| タクティクス | 得意な定理の種類 |
|-------------|----------------|
| `rfl` | 定義上自明な等式（`1 + 1 = 2` など） |
| `ring` | 可換環の等式（展開・因数分解） |
| `omega` | 自然数・整数の線形算術 |
| `simp` | 既知の補題で簡約できるもの |
| `norm_num` | 数値計算で確かめられる等式・不等式 |
| `decide` | 有限の計算で確かめられるもの |
| `linarith` | 線形不等式 |
| `nlinarith` | 非線形不等式（二乗が絡むものなど） |
| `aesop` | 論理・集合論的な命題 |

### 帰納法タクティクス

`∑`（`Finset.sum`）が含まれる定理や数列の公式には帰納法を自動で適用します。

```
induction n with
  | zero => simp
  | succ m ih => nlinarith [ih]
```

### 検索タクティクス（最後の手段）

上記のすべてが失敗した場合に限り、Mathlib 全体を検索する `exact?` / `simp?` を試します。

| タクティクス | 動作 |
|-------------|------|
| `exact?` | ゴールに完全一致する Mathlib 補題を検索し、`exact 補題名` を返す |
| `simp?` | `simp` が使う補題を特定し、`simp only [...]` を返す |

これらは成功すると「Try this: exact ...」のような具体的な証明を報告します。
スクリプトはその内容を解析して `ProvedTheorems.lean` に保存します。

```
# exact? が見つけた場合の保存例
theorem my_thm (n : ℕ) : n + 0 = n := by
  exact Nat.add_zero n      ← "exact?" ではなく具体的な補題名で保存される
```

> **注意**: `exact?` / `simp?` は Mathlib 全体を検索するため、1 回あたり **数十秒**かかることがあります。

### ゴールによる自動選択

ゴール文字列を見て使うタクティクスを絞り込みます（検索タクティクスは常に末尾に追加）。

| ゴールの特徴 | 試すタクティクス（順番に） |
|-------------|----------------|
| `∑` や `Finset` を含む | 帰納法 → `exact?` → `simp?` |
| `^`（べき乗）を含む | `ring`, `nlinarith`, 帰納法 → `exact?` → `simp?` |
| `ℝ` や `ℚ` を含む | `ring`, `linarith`, `norm_num`, `nlinarith` → `exact?` → `simp?` |
| `ℕ` や `ℤ` を含む | `omega`, `simp`, `rfl`, `decide`, `ring`, `norm_num` → `exact?` → `simp?` |
| その他 | すべて → `exact?` → `simp?` |

---

## 7. キャッシュの仕組み

一度証明に成功した定理は `.proof_index.json` に記録されます。

```
.proof_index.json
{
  "a1b2c3d4e5f6a7b8": "t1",   ← SHA-256 ハッシュの先頭 16 文字 → Lean の定理名
  ...
}
```

**同じ定理を再度渡した場合** は REPL を起動せず即座に「キャッシュ済み」として扱います。

```
[run] 7 theorems (7 cached / 0 uncached)
total: 7 passed / 0 failed / 0.0s
```

キャッシュをリセットしたい場合は `.proof_index.json` を削除してください。

```bash
rm .proof_index.json
```

---

## 8. 証明の保存先

証明に成功した定理は `LeanMathAtlas/ProvedTheorems.lean` に自動で追記されます。

```lean
-- stmt: theorem t4 (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2
-- goal:
--   ⊢ (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2
-- added: 2026-06-05
theorem t4 (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by
  ring
```

このファイルは Lean コンパイラが型検査しているので、保存された証明の**正しさは Lean が保証**しています。

> `lake build` を実行すると `ProvedTheorems.lean` もコンパイルされ、エラーがあれば検出されます。

---

## 9. 制限事項

- **仮定が多い定理は苦手**  
  `∀ x, f x > 0` のような量化子や複雑な仮定が絡む定理は、現在のタクティクスリストでは証明できないことが多いです。

- **Mathlib の補題を直接使う定理は非対応**  
  `exact Nat.prime_def_lt_prime.mpr ...` のような特定の Mathlib 補題を名指しする証明は自動生成できません。

- **初回起動は遅い**  
  Lean REPL の起動と Mathlib の読み込みに **約 80 秒** かかります。これは避けられません。

- **証明が見つからない場合の対処**  
  `✗ proof not found` が出た場合は、手動で VSCode の Lean InfoView を使ってゴールを確認し、適切なタクティクスを探してください。

---

## 10. よくある質問

### Q. 実行したら `lake build` が始まって時間がかかる

**A.** 初回は `LeanMathAtlas.ProvedTheorems` のビルドが必要です。以降はキャッシュされます。

### Q. `✗ proof not found` になった

**A.** 現在のタクティクスリストで対応できない定理です。以下を試してください。
1. VSCode で `sorry` を書いてゴール状態を手動で確認する
2. `ring_nf` / `simp?` / `exact?` で候補を検索する
3. Mathlib の該当モジュールの補題を探す

### Q. `.proof_index.json` が壊れた

**A.** 安全に削除できます。次回実行時に再生成されます。

```bash
rm .proof_index.json
```

### Q. 別のプロジェクトで使いたい

**A.** `LEAN_WORKDIR` 環境変数でプロジェクトルートを指定できます。

```bash
LEAN_WORKDIR=/path/to/my_project python3 auto_prove.py "theorem ..."
```

---

## 11. 自動化の限界

`✗ proof not found` が出た場合は自動化の限界を超えています。
以下のような証明は手動で書く必要があります。

```lean
-- 解けない典型例: Mathlib の補題を組み合わせる多段証明
have hf : HasDerivAt (fun x => 2 * x) 2 a := ...
have hg : HasDerivAt Real.sin (Real.cos (2 * a)) (2 * a) := ...
exact hg.comp a hf
```

計測結果（問題セット・バージョン別の精度変化）は [BENCHMARK.md](BENCHMARK.md) を参照してください。

---

## 技術メモ（開発者向け）

- REPL プロトコル: JSON コマンドを `\n\n` 区切りで送受信
- 名前衝突の回避: `theorem foo` → `example` に変換して REPL に送信（重複宣言エラーを防ぐ）
- pickle は使わない: unpickle 後に `ring` などの `[init]` 属性タクティクスがクラッシュするため
- 拡張アイデア: Claude API でゴール状態からタクティクスを推論する、LeanDojo 連携でデータベース検索

---

## 改善を追加するときの基準

タクティクスやテンプレートを追加する際は、**汎用性があるかどうか**を必ず確認すること。

| 追加してよい | 追加しない |
|---|---|
| `ring`、`omega`、`fun_prop` のように、ゴールの構造に関係なく広く使えるもの | 特定の定理名・変数名・定数をハードコードしたもの |
| `exact (Real.hasDerivAt_sin _).const_mul _` のように、`_` で型推論に任せて広いクラスをカバーできるもの | `a` や `2` を直書きして1問だけ解けるもの |
| ゴール文字列のパターン（`Continuous`、`HasDerivAt` など）で適用範囲を限定したタクティクス | 特定の benchmark 問題に合わせて作ったワンオフの証明列 |

**判断基準の目安**: 「このタクティクスは、今ある問題セット以外の新しい定理にも適用できるか？」を問うこと。答えが No なら、それは改善ではなくテストへの過学習。

`benchmark.py` の `hard` カテゴリに解けない問題が残っていても、汎用性のない対処でスコアを上げるより、限界として記録しておく方が正直な評価につながる。
