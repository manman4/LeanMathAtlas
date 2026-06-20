# Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.3.19 | 2026-06-20 | feat(auto_prove): extend Phase 3 `have` search from one-shot helpers to a bounded two-stage search; generate the second `have` from the remaining goal after the first helper, with small width limits to avoid search and memory blow-up; refine Phase 2 BFS to choose a small goal-shape-specific step-tactic set instead of replaying the same broad fixed list on every proof state; make Phase 1.6 `apply?` closers goal-aware by probing the residual subgoal before choosing `simp` / `fun_prop` / `ring` / `linarith`-style finishers; add `tools/check_targets.py` for low-memory dry-run checks of a few `FILE::theorem_name` targets with one REPL reuse per file; add `tools/analyze_failures.py` to summarize local failure logs by reusable goal class instead of theorem-specific cases; add generic `Tendsto` templates that derive a `ContinuousAt` proof with `fun_prop`, replay matching `add` / `mul` / `const_mul` / `comp` hypotheses, and verify search suggestions through goal-aware rewrite hints; add structural `HasDerivAt` templates for broad classes like `x^n + c*x + k`, `x * (x + c)`, and `sin x * cos x`, plus continuity/differentiability templates derived from `HasDerivAt` hypotheses; add REPL startup timeout/phase diagnostics plus `check_targets.py --prepare-timeout` for better low-memory triage when Mathlib import stalls; forcibly tear down stuck REPL processes after startup timeouts so low-memory checks do not hang on `wait()`; prioritize class-specific tactics ahead of generic algebra for `trig` / `limit` goals, add lightweight normalization tactics (`simpa`, `ring_nf`, `field_simp`, `norm_cast`) ahead of broad search, strengthen `have` candidates for `Tendsto`, `HasDerivAt`, `trig`, and `inner_norm` classes, and record normalized goal shapes in failure analysis |
| 0.3.18 | 2026-06-16 | feat(auto_prove): record failed proof attempts to local-only `.auto_prove_failures.jsonl` with goal / timeout / selected-tactic metadata (ignored by git); refine tactic routing by target shape instead of whole context, extend generic real-power inequality handling to `<` / `>`, and stop spraying induction templates onto generic exponent goals |
| 0.3.17 | 2026-06-15 | feat(auto_prove): add lightweight search-time normalisation prefixes (`simp`, `norm_num`, `ring_nf`, `norm_cast`, `push_cast`) around `exact?` / `simp?` / `apply?` exploration; prove: this general normalisation now recovers at least `factor_theorem` and `sum_range_eq` from the unresolved set in dry-run checks |
| 0.3.16 | 2026-06-15 | refactor(auto_prove): split storage / REPL / tactic-selection helpers into `auto_prove_store.py`, `auto_prove_repl.py`, and `auto_prove_tactics.py` while keeping the `auto_prove.py` CLI and the Python API used by `batch_prove.py` / `benchmark.py` stable; docs: update README and AUTO_PROVE guide; smoke: re-check single-theorem `auto_prove` and `batch_prove --dry-run` paths with low-memory sequential runs |
| 0.3.15 | 2026-06-15 | fix(auto_prove): verify `exact?` / `simp?` suggestions through `simpa using` and symmetric variants before giving up; prove: add `arith_diff`, `arith_zero`, `deriv_sq`, `deriv_cube`; fix(proved): restore missing `sin_pi` / `cos_pi` imports in `ProvedTheorems` (26 unresolved → 20) |
| 0.3.14 | 2026-06-10 | perf: reuse one REPL per file in `batch_prove`, add configurable 60s theorem timeout (default for normal `auto_prove` / `batch_prove` runs), skip `ProvedTheorems` build unless `--use-proved`; safety: in `--use-proved` mode, rollback a newly saved theorem if it would break `LeanMathAtlas.ProvedTheorems`; benchmark keeps old no-total-timeout condition; prove: +72 theorems (162/186 total) |
| 0.3.13 | 2026-06-10 | fix(hooks): block --no-verify in Claude Code PreToolUse hook to prevent bypassing personal-info pre-commit guard |
| 0.3.12 | 2026-06-09 | fix(tools): remove AutoProved chain imports (each file now imports only Mathlib, eliminating cascading failures); add use_proved=False flag to prove_all / batch_prove / auto_prove CLI so previously proved theorems are opt-in; fix RuntimeError handling in batch_prove and benchmark; feat(algebra): auto-prove 11 BasicIdentities theorems; chore: untrack .claude/settings.json to prevent personal paths leaking into history |
| 0.3.11 | 2026-06-09 | fix(auto_prove): fail fast when `LeanMathAtlas.ProvedTheorems` build/import fails; refactor(proved): store auto-proved theorems as one-file-per-theorem under `LeanMathAtlas/AutoProved/` and reduce `ProvedTheorems.lean` to an import aggregator to avoid cross-theorem breakage |
| 0.3.10 | 2026-06-09 | fix(auto_prove): stabilize 51/51 benchmark reproducibility by resolving `lake` outside shell PATH, aligning normal-run imports with dry-run `Mathlib`, strengthening chain-rule tactic generation; fix(benchmark): restore Python 3.9 compatibility |
| 0.3.9 | 2026-06-07 | fix(auto_prove): HasDerivAt before trig in select_tactics (fun x => の => が誤マッチするバグ修正); id → id_eq (Lean 4 正しい simp 補題); Phase 3 have-augmented proof search (last resort); bench 51/51 (100%) |
| 0.3.8 | 2026-06-07 | fix(ProvedTheorems): replace 12 incorrect norm_num proofs with correct Mathlib lemmas; docs: document norm_num usage policy in AUTO_PROVE.md |
| 0.3.7 | 2026-06-07 | refactor: remove 7 duplicate entries in ProvedTheorems.lean (210→203); docs: document deduplication issue and policy in AUTO_PROVE.md |
| 0.3.6 | 2026-06-07 | fix(batch_prove): depth-aware := parsing to prevent signature truncation at 𝕜 :=; repair corrupt my_inner_self_nonneg and cauchy_schwarz entries in ProvedTheorems.lean |
| 0.3.5 | 2026-06-07 | feat(auto_prove): add INNER_PRODUCT_TACTICS / COMPLEX_TACTICS / TRIG_DOUBLE_TACTICS; prove de_moivre, normSq_sq, one_add_tan_sq; remove overfitted tactics (TAN_TACTICS, cos_double fallback) |
| 0.3.4 | 2026-06-07 | feat: file-based benchmark (tools/bench/*.lean); prove: remainder_theorem |
| 0.3.3 | 2026-06-07 | prove: 40 theorems (Derivatives/Limits/Integration/Vectors/Combinatorics/Sequences); 34 skipped (auto_prove未対応) |
| 0.3.2 | 2026-06-07 | prove: Algebra/Complex 9/11 (I_sq, norm_mul, conj_*, euler_formula, norm_exp_I_eq_one) |
| 0.3.1 | 2026-06-07 | fix: duplicate theorem guard in append_to_lean_db; whitespace normalization in batch_prove extract_theorems; add batch_prove.py; prove my_exists_le_maximal |
| 0.3.0 | 2026-06-07 | feat: preamble support in auto_prove.py (--file flag extracts open/variable from source); bulk proofs added across Groups, Rings, Topology, Trigonometry, NumberTheory, Combinatorics |
| 0.2.1 | 2026-06-07 | fix: unpack prove_all results as 4-tuple in main(); add mul_sum_diff / cube_sum to ProvedTheorems |
| 0.2.0 | 2026-06-07 | auto_prove: open scoped Nat; !+Nat.Prime 検出で Wilson 解決; 変数名動的抽出で汎用化 — 50/50 (100%) 全問制覇 |
| 0.1.17 | 2026-06-07 | auto_prove: chain_rule_deriv_tactics (明示的引数); FINSET_CARD_TEMPLATES (bijection + rw); open Nat; Wilson 検出 (49/50, 98%, hard 8/8) |
| 0.1.16 | 2026-06-06 | auto_prove: extract_real_vars + nlinarith_pairwise_sq_tactic（対称・Cauchy-Schwarz型不等式を自動解決）; benchmark: 多項式不等式 4問をALGEBRAに追加 (47/50, 94%, test_hash: e456a836) |
| 0.1.15 | 2026-06-06 | auto_prove: 動的 nlinarith witness (AM-GM3); ZMod select; ring_nf DERIV; cast前処理 (43/46, 93%) |
| 0.1.14 | 2026-06-06 | auto_prove: FINTYPE_TEMPLATES (Pigeonhole); Phase 1.5 拡張・堅牢化; Phase 1.6 apply? 追加 (42/46, 91%) |
| 0.1.13 | 2026-06-06 | docs: update AUTO_PROVE / BENCHMARK / PLANNING with current state and next development candidates |
| 0.1.12 | 2026-06-06 | benchmark: per-theorem solve_time cache (.bench_cache.json); BFS timeout 30s→10s; 6min→5.5min |
| 0.1.11 | 2026-06-06 | auto_prove: haveI Fact typeclass preamble; solves Fermat's little theorem (competition 2/5) |
| 0.1.10 | 2026-06-06 | benchmark: add elapsed_sec to log; expand competition to 5 problems (Pigeonhole, Fermat, AM-GM×3) |
| 0.1.9 | 2026-06-06 | benchmark: add competition category (Cauchy-Schwarz, Wilson's theorem), 43 problems total |
| 0.1.8 | 2026-06-06 | benchmark: expand to 41 problems (algebra×12, induction×5) |
| 0.1.7 | 2026-06-06 | Add CLAUDE.md with branching and release instructions for GitHub Flow |
| 0.1.6 | 2026-06-06 | fix: remove duplicate entries in ProvedTheorems.lean caused by pre-dry_run benchmark runs |
| 0.1.5 | 2026-06-06 | benchmark: dry_run mode, hard×8, HasDerivAt templates; auto_prove: fun_prop/norm_cast/import Mathlib |
| 0.1.4 | 2026-06-06 | benchmark.py: bench_log.csv with --save, test_hash, suite column, argparse |
| 0.1.3 | 2026-06-06 | Add CONTRIBUTING.md |
| 0.1.2 | 2026-06-06 | Add PLANNING.md with design decisions and deprioritization notes |
| 0.1.1 | 2026-06-06 | Add English notes (docs/en/) for all 17 modules; add Notes links in ROADMAP.md |
| 0.1.0 | 2026-06-06 | Cleanup: README/ROADMAP updated to reflect all 16 implemented modules |
| 0.0.9 | 2026-06-06 | Integration (interval integrals, FTC parts 1 & 2, concrete examples), all ★★★ Advanced complete |
| 0.0.8 | 2026-06-06 | Ring Theory (CommRing, Ideal, quotient rings, prime/maximal ideal correspondence) |
| 0.0.7 | 2026-06-06 | Group Theory (Group laws, Subgroup, Lagrange's theorem), Topology (open sets, compactness, connectedness) |
| 0.0.6 | 2026-06-06 | Vectors (inner product, norm, Cauchy-Schwarz), ★★☆ Intermediate all complete |
| 0.0.5 | 2026-06-06 | Limits (`ε-δ`, `Filter.Tendsto`), docs/ja for Modular and Limits |
| 0.0.4 | 2026-06-06 | Modular arithmetic (`ZMod`, Fermat's little theorem) |
| 0.0.3 | 2026-06-06 | Move tooling to `tools/` directory |
| 0.0.2 | 2026-06-06 | Add Lean proof files (★☆☆ Beginner all, ★★☆ Intermediate 3/6), auto_prove.py |
| 0.0.1 | 2026-06-06 | Initial setup: README, ROADMAP, .gitignore, Claude security settings |
