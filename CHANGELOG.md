# Changelog

| Version | Date | Changes |
|---------|------|---------|
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
