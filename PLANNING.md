# Planning & Roadmap Notes

This document records design decisions and the reasoning behind things that were considered but not implemented.

---

## Current state (2026-06-06)

- 16 Lean proof files (★☆☆ / ★★☆ / ★★★), bilingual docs (`docs/ja/`, `docs/en/`)
- `tools/auto_prove.py`: automated theorem prover, v0.1.11
- `tools/benchmark.py`: 46-problem benchmark suite, v0.1.12
- Benchmark score: **41/46 (89%)**, competition 2/5
- Unsolved: chain rule, card_filter (hard), Wilson, Pigeonhole, AM-GM 3変数 (competition)

See [CHANGELOG.md](CHANGELOG.md) for full version history and [tools/BENCHMARK.md](tools/BENCHMARK.md) for precision records.

---

## Next development candidates

### auto_prove 精度改善

| ID | 内容 | 難易度 | 期待効果 |
|---|---|---|---|
| A | Wilson の定理（`haveI` 後も `exact?` が失敗する原因を調査。`ZMod.wilsons_lemma` のレンマ名確認） | 中 | competition 3/5 |
| B | Pigeonhole（`apply Fintype.exists_ne_map_eq_of_card_lt` + `simp [Fintype.card_fin]` の BFS 追加） | 中 | competition 3/5 |
| C | chain rule（`convert` + `ring` テンプレートで mul_comm 方向不一致を吸収） | 高 | hard 7/8 |
| D | LLM ベース証明探索（Claude API をゴール → タクティク推論に使用） | 高 | 全カテゴリ改善 |

### ベンチマーク・可視化

| ID | 内容 |
|---|---|
| E | GitHub Actions で PR 時に自動ベンチマーク実行（`bench_log.csv` に自動追記） |
| F | bench_log.csv をグラフ化（HTML レポート or GitHub Pages） |

### Lean ライブラリとしての充実

| ID | 内容 |
|---|---|
| G | 数学モジュール追加（例: 組み合わせ論の拡張、確率論の基礎） |
| H | 証明済み定理に解説コメント追加（教育用途） |

### インフラ・高速化

| ID | 内容 | 備考 |
|---|---|---|
| I | 並列 REPL（threading で 2 インスタンム化） | 理論値 150s（現在 360s）、メモリ ~4GB×2 必要 |
| J | TheoremForces / LeanCopilot との連携調査 | LLM + Lean REPL の外部エコシステム |

---

---

## Considered and deprioritized

### GitHub Actions CI

**Status:** Not implemented.

**What it would do:** Run `lake build` automatically on every push and pull request, and surface a "build passing" badge.

**Why it was deprioritized:**
- Currently a solo project — every push is already verified locally with `lake build` before it goes out.
- CI adds the most value when multiple contributors are pushing independently, or when dependency updates (e.g. a Mathlib version bump) could silently break things without anyone noticing.
- Technically feasible in ~5–10 min per run using `lake exe cache get` to pull pre-built Mathlib binaries from Lean's CDN, so compilation cost is not a blocker.

**Reconsider when:** The project has external contributors, or automated Mathlib version bumps are set up.

