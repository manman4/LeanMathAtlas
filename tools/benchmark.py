#!/usr/bin/env python3
"""
Coverage benchmark: measure how many theorems auto_prove.py can solve.

Categories:
  A) Logic (Propositional-style) — main target for iterative BFS
  B) Algebra (ring / omega)      — phase-1 should close most
  C) Induction (Sequences)       — template matching
  D) Hard (multi-step have)      — expected failures

Usage:
  python3 benchmark.py                        # run only, no log
  python3 benchmark.py --save "tauto追加"     # run and append result to bench_log.csv
"""
import sys
import csv
from datetime import date
from pathlib import Path
from auto_prove import prove_all, cache_key, load_index

LOG_FILE = Path(__file__).parent / "bench_log.csv"
LOG_HEADER = ["date", "label", "A", "B", "C", "D", "total", "pct"]

LOGIC = [
    # 含意
    "theorem bench_imp_id (P : Prop) : P → P",
    "theorem bench_imp_weak (P Q : Prop) : P → Q → P",
    "theorem bench_imp_trans (P Q R : Prop) : (P → Q) → (Q → R) → (P → R)",
    # 論理積
    "theorem bench_and_intro (P Q : Prop) (hp : P) (hq : Q) : P ∧ Q",
    "theorem bench_and_left (P Q : Prop) (h : P ∧ Q) : P",
    "theorem bench_and_right (P Q : Prop) (h : P ∧ Q) : Q",
    "theorem bench_and_comm (P Q : Prop) : P ∧ Q → Q ∧ P",
    # 論理和
    "theorem bench_or_inl (P Q : Prop) (hp : P) : P ∨ Q",
    "theorem bench_or_inr (P Q : Prop) (hq : Q) : P ∨ Q",
    "theorem bench_or_comm (P Q : Prop) : P ∨ Q → Q ∨ P",
    # 否定
    "theorem bench_not_false : ¬False",
    "theorem bench_contrapos (P Q : Prop) : (P → Q) → (¬Q → ¬P)",
    "theorem bench_absurd_ex (P Q : Prop) : P → ¬P → Q",
    # 同値
    "theorem bench_iff_refl (P : Prop) : P ↔ P",
    "theorem bench_iff_mp (P Q : Prop) (h : P ↔ Q) (hp : P) : Q",
    # ド・モルガン
    "theorem bench_demorgan (P Q : Prop) : ¬(P ∨ Q) → ¬P ∧ ¬Q",
]

ALGEBRA = [
    "theorem bench_sq_sum (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2",
    "theorem bench_sq_diff (a b : ℝ) : (a - b)^2 = a^2 - 2*a*b + b^2",
    "theorem bench_diff_sq (a b : ℝ) : (a + b) * (a - b) = a^2 - b^2",
    "theorem bench_cube_sum (a b : ℝ) : (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3",
    "theorem bench_nat_comm (a b : ℕ) : a + b = b + a",
    "theorem bench_nat_assoc (a b c : ℕ) : (a + b) + c = a + (b + c)",
    "theorem bench_nat_le (n : ℕ) : n ≤ n + 1",
    "theorem bench_int_linarith (a b : ℤ) (h1 : a ≤ b) (h2 : b ≤ a) : a = b",
]

INDUCTION = [
    "theorem bench_sum_gauss (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)",
    "theorem bench_sum_sq (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1)",
]

HARD = [
    # These require multi-step `have` with specific Mathlib lemmas — expected ✗
    "theorem bench_hard_deriv (f : ℝ → ℝ) (a : ℝ) : HasDerivAt (fun x => 2 * Real.sin x) (2 * Real.cos a) a",
    "theorem bench_hard_prime_inf : ∀ n : ℕ, ∃ p, n ≤ p ∧ Nat.Prime p",
]

ALL = LOGIC + ALGEBRA + INDUCTION + HARD

CATS = [
    ("A) 論理 (BFS 主ターゲット)", "A", LOGIC),
    ("B) 代数 (ring/omega)",       "B", ALGEBRA),
    ("C) 帰納法 (テンプレート)",    "C", INDUCTION),
    ("D) 難問 (多ステップ have)",   "D", HARD),
]


def append_log(label: str, scores: dict[str, tuple[int, int]], total_pass: int, total: int):
    exists = LOG_FILE.exists()
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_HEADER)
        if not exists:
            writer.writeheader()
        writer.writerow({
            "date":  date.today().isoformat(),
            "label": label,
            "A":     f"{scores['A'][0]}/{scores['A'][1]}",
            "B":     f"{scores['B'][0]}/{scores['B'][1]}",
            "C":     f"{scores['C'][0]}/{scores['C'][1]}",
            "D":     f"{scores['D'][0]}/{scores['D'][1]}",
            "total": f"{total_pass}/{total}",
            "pct":   f"{total_pass / total * 100:.0f}%",
        })
    print(f"\n→ 結果を {LOG_FILE.name} に追記しました (label: {label!r})")


def run_benchmark(save_label: str | None = None):
    index = load_index()
    cached = sum(1 for s in ALL if cache_key(s) in index)
    print(f"=== ベンチマーク開始: {len(ALL)} 件 ({cached} キャッシュ済 / {len(ALL)-cached} 未計測) ===\n")

    results = prove_all(ALL)

    total_pass = total_fail = 0
    scores: dict[str, tuple[int, int]] = {}
    print()
    for label, key, stmts in CATS:
        r = {s: p for s, p, _ in results if s in stmts}
        ok = sum(1 for s in stmts if r.get(s))
        scores[key] = (ok, len(stmts))
        total_pass += ok
        total_fail += len(stmts) - ok
        print(f"{label}: {ok}/{len(stmts)} ✓")
        for s in stmts:
            p = r.get(s)
            name = s.split()[1]
            icon = "✓" if p else "✗"
            proof_hint = f" ({p.split(chr(10))[0][:40]})" if p else ""
            print(f"  {icon} {name}{proof_hint}")
        print()

    total = total_pass + total_fail
    pct = total_pass / total * 100
    print(f"{'='*55}")
    print(f"合計: {total_pass}/{total} ({pct:.0f}%)")

    if save_label is not None:
        append_log(save_label, scores, total_pass, total)


if __name__ == "__main__":
    label = None
    args = sys.argv[1:]
    if "--save" in args:
        idx = args.index("--save")
        if idx + 1 < len(args):
            label = args[idx + 1]
        else:
            print("使い方: python3 benchmark.py --save <ラベル>")
            sys.exit(1)
    run_benchmark(save_label=label)
