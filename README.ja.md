# LeanMathAtlas

数学の定理を科目別に整理した Lean 4 証明コレクションです。
証明は Lean コンパイラによって検証され、自動証明スクリプト（`auto_prove.py`）によって
`LeanMathAtlas/ProvedTheorems.lean` に蓄積されていきます。

## 内容

```
LeanMathAtlas/
  Algebra/
    BasicIdentities.lean   # 式の展開・因数分解・二次不等式・因数定理・剰余定理
    Sequences.lean         # 等差・等比数列、和の公式（ガウス・平方和・立方和）
  Analysis/
    Trigonometry.lean      # 三角関数の基本公式・加法定理・2倍角公式
  Combinatorics/
    BinomialTheorem.lean   # 二項係数・パスカルの三角形・二項定理
  NumberTheory/
    NaturalNumbers.lean    # 帰納法・算術の基本法則・偶奇
  Logic/
    Propositional.lean     # 導入・除去規則・ド・モルガン・恒真式
  ProvedTheorems.lean      # 自動生成: auto_prove.py が証明した定理

docs/ja/                   # 各モジュールの日本語解説（Markdown）
tools/
  auto_prove.py            # Lean REPL を使った自動証明スクリプト
  benchmark.py             # 精度ベンチマーク
```

## 環境の準備

| ツール | バージョン |
|--------|-----------|
| Lean 4 | `v4.27.0`（`lean-toolchain` 参照） |
| Mathlib | `v4.27.0` |
| Python | 3.11 以上 |

### Lean / elan のインストール

```bash
curl https://elan.lean-lang.org/elan-init.sh | sh
```

### 依存パッケージの取得

```bash
lake update
```

Mathlib と REPL パッケージをダウンロードします（初回は数分かかります）。

### ビルド

```bash
lake build
```

## [難易度マップ →](ROADMAP.md)

## 学習のしかた

### 1. 証明ファイルを読む

`LeanMathAtlas/` 以下の各ファイルはトピックごとにまとまっています。
VS Code に Lean 4 拡張機能を入れてファイルを開くと、カーソルを当てた項の型が表示されます。
`Exercises.lean` の `sorry` 部分に自分で証明を書いてみましょう。

```bash
code LeanMathAtlas/Algebra/BasicIdentities.lean
```

各定理を日本語で解説したノートは `docs/ja/<科目>/<ファイル名>.md` にあります。

### 2. 自動証明スクリプトを使う

`auto_prove.py` は定理の文を受け取り、Lean REPL 経由でタクティクを試し、
成功した証明を `ProvedTheorems.lean` に保存します。

```bash
# 組み込みテスト（7 定理）を実行
python3 tools/auto_prove.py

# 任意の定理を証明する
python3 tools/auto_prove.py "theorem my_thm (a b : ℝ) : (a - b)^2 ≥ 0"
```

一度証明した定理は `.proof_index.json` にキャッシュされ、次回以降は即座に結果を返します。

### 3. 演習問題を解く

`LeanMathAtlas/Exercises.lean` には `sorry` で穴埋めになった定理があります。
`sorry` を有効なタクティク証明に書き換えてください。

```lean
-- 変更前
theorem ex1 (n : ℕ) : n + 0 = n := by sorry

-- 変更後
theorem ex1 (n : ℕ) : n + 0 = n := by rfl
```

## ライセンス

[MIT License](LICENSE)

> **依存パッケージについて**: このリポジトリは
> [Mathlib](https://github.com/leanprover-community/mathlib4)（Apache 2.0）および
> [Lean REPL](https://github.com/leanprover-community/repl)（Apache 2.0）を使用しています。
> それぞれのパッケージには各ライセンスが適用されます。
