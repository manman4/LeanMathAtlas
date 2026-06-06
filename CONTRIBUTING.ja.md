# LeanMathAtlas への貢献

> **Read in English →** [CONTRIBUTING.md](CONTRIBUTING.md)

## セットアップ

```bash
curl https://elan.lean-lang.org/elan-init.sh | sh
lake update
lake build
```

## モジュールの追加

Lean ファイルは対応する科目ディレクトリに置いてください：

```
LeanMathAtlas/
  Algebra/       — 代数的構造
  Analysis/      — 微積分・極限・積分
  Combinatorics/ — 数え上げ・二項定理
  LinearAlgebra/ — ベクトル・行列
  Logic/         — 命題論理・述語論理
  NumberTheory/  — 素数・合同算術
  Topology/      — 開集合・コンパクト性
```

**規約：**
- カスタム定理名には `my_` プレフィックスをつける（例：`my_gcd_comm`）。
- 証明ファイルに `sorry` を残さない。
- PR 提出前に `lake build` が通ることを確認する。

## プルリクエストの送り方

`main` ブランチに向けて PR を作成し、追加するモジュールの内容とプロジェクトへの適合理由を説明してください。ドキュメントやリリース作業はメンテナーが対応します。
