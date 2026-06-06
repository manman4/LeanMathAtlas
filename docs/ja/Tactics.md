# タクティクスガイド

> **Read in English →** [Tactics.md](../en/Tactics.md)

対応する Lean ファイル: `LeanMathAtlas/Tactics.lean`

Lean 4 で証明を書くとき、`by` の後ろに書く命令を **タクティクス** といいます。
このファイルでは「自動で証明を完成させてくれるタクティクス」を中心に説明します。

---

## 自動証明タクティクス

これらは**ゴールの形を見て、内部で自動計算して証明を閉じてくれる**タクティクスです。
書き方は `by タクティクス名` だけ——自分で計算ステップを書く必要がありません。

---

### `ring` — 代数の等式

**何をするか**: 交換法則・結合法則・分配法則・展開・因数分解など、
代数の計算で確かめられる等式を自動証明します。

```lean
example (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by ring
example (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2  := by ring
example (a b c : ℝ) : a * (b + c) = a*b + a*c       := by ring
```

**使える型**: `ℕ` `ℤ` `ℚ` `ℝ` `ℂ` など、環の構造を持つもの全般

**できないこと**:
- 不等式（`≤` `<`）
- 掛け算・割り算が絡む自然数の等式（`a * b = b * a` は `ring` で解けるが `a / b` は不可）

---

### `omega` — 自然数・整数の算術

**何をするか**: 整数・自然数の**等式と不等式**を線形算術のアルゴリズムで自動証明します。
足し算・引き算・定数倍の範囲で使えます。

```lean
example (n : ℕ) : n + 0 = n               := by omega
example (n : ℕ) : n ≤ n + 1               := by omega
example (a b : ℤ) (h : a ≤ b) : a ≤ b + 1 := by omega
example (n : ℕ) (h : n ≥ 1) : n > 0       := by omega
```

**使える型**: `ℕ` `ℤ`

**できないこと**:
- 掛け算・べき乗が絡む不等式（`n * m ≤ ...` など）→ `linarith` や `nlinarith` を使う
- 実数・有理数の不等式 → `linarith` を使う

---

### `simp` — 既知の補題で式を簡略化

**何をするか**: Mathlib に登録された簡略化ルール（`@[simp]` 補題）を次々と適用して
ゴールを `True` または自明な形まで簡略化します。

```lean
example : ([] : List ℕ).length = 0 := by simp
example (n : ℕ) : n + 0 = n        := by simp
example : True                      := by simp
```

特定の補題を追加することもできます：

```lean
-- Finset.sum_range_succ を simp のルールに加えて使う
example : ∑ k ∈ Finset.range 3, k = 3 := by simp [Finset.sum_range_succ]
```

**注意**: どの補題が使われたか表示されないため、なぜ通ったか不明になりがちです。
`simp?` を使うとどの補題が効いたか教えてくれます。

```lean
example (n : ℕ) : n + 0 = n := by simp?
-- → Try this: simp only [Nat.add_zero]
```

---

### `decide` — 有限の計算で確かめる

**何をするか**: 有限の計算に落とし込める命題を、実際に計算して証明します。

```lean
example : Nat.Prime 7       := by decide   -- 7 が素数かどうか計算して確認
example : ¬ Nat.Prime 4     := by decide   -- 4 が素数でないことを確認
example : 2 + 3 = 5         := by decide
```

**注意**: 大きな数には使わないでください（計算時間が爆発します）。

---

### `norm_num` — 数値の等式・不等式

**何をするか**: 具体的な数値が絡む等式・不等式・素数判定などを計算して証明します。

```lean
example : (7 : ℤ) * 8 = 56       := by norm_num
example : (10 : ℕ) ≠ 11          := by norm_num
example : (2 : ℝ) > 0            := by norm_num
```

`decide` より大きな数にも対応しています。

---

### `linarith` / `nlinarith` — 不等式

**何をするか**: 仮定から不等式を導きます。

| タクティクス | 対象 |
|---|---|
| `linarith` | 線形不等式（足し算・定数倍のみ） |
| `nlinarith` | 非線形不等式（掛け算・二乗を含む） |

```lean
-- linarith: 仮定の組み合わせで結論を導く
example (a b : ℝ) (h1 : a ≤ 3) (h2 : 3 ≤ b) : a ≤ b := by linarith

-- nlinarith: 二乗が絡む不等式
example (a b : ℝ) : 2 * a * b ≤ a^2 + b^2 := by nlinarith [sq_nonneg (a - b)]
```

---

## 使い分けのまとめ

```
証明したいゴールの形
  │
  ├─ 等式（= ）
  │    ├─ 代数（展開・因数分解）         → ring
  │    ├─ 自然数・整数の足し算・引き算    → omega
  │    └─ 具体的な数値                  → norm_num / decide
  │
  └─ 不等式（≤ < ≥ > ）
       ├─ 自然数・整数の線形            → omega
       ├─ 実数の線形                   → linarith
       └─ 実数の非線形（掛け算・二乗）   → nlinarith
```

どれも通れば証明完了です。まず `ring` → `omega` → `simp` の順に試してみるのが効率的です。

---

## 手動タクティクス（参考）

自動タクティクスで解けない場合は、以下を組み合わせます。

| タクティクス | 役割 |
|---|---|
| `intro h` | `P → Q` のゴールで `P` を仮定として取り込む |
| `exact h` | 仮定 `h` がゴールと完全一致するとき閉じる |
| `apply f` | 補題 `f` を適用してゴールを変換する |
| `rw [h]` | 等式 `h` でゴールを書き換える |
| `have h := ...` | 証明の途中で補助命題を作る |
| `induction n with` | 自然数 `n` の帰納法 |
| `obtain ⟨a, b⟩ := h` | `h` を分解して要素を取り出す |
| `rcases h with ha \| hb` | `h : P ∨ Q` を場合分けする |
| `constructor` | `P ∧ Q` を 2 つのゴールに分割する |