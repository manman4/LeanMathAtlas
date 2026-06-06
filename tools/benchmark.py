#!/usr/bin/env python3
"""
Coverage benchmark: measure how many theorems auto_prove.py can solve.

Categories:
  logic     — propositional logic (tauto / BFS target)
  algebra   — ring / omega
  induction — summation formulas
  hard      — multi-step have (expected failures)
"""
import sys
import csv
import hashlib
from datetime import date
from pathlib import Path
from auto_prove import prove_all, cache_key, load_index

LOG_FILE = Path(__file__).parent / "bench_log.csv"
LOG_HEADER = ["date", "label", "suite", "test_hash", "logic", "algebra", "induction", "hard", "competition", "total", "pct"]


def compute_test_hash(problems: list[str]) -> str:
    """Compute a short hash of the problem set to detect accidental changes."""
    content = "\n".join(sorted(problems))
    return hashlib.sha256(content.encode()).hexdigest()[:8]

# Problem sets are defined inline here rather than in a separate file.
# Rationale: at ~40 problems the overhead of a separate module outweighs the benefit.
# If the total grows past ~100 problems or multiple suites need to be managed
# independently, consider splitting into bench_problems.py or a JSON file.

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
    # additional algebra
    "theorem bench_cube_diff (a b : ℝ) : (a - b)^3 = a^3 - 3*a^2*b + 3*a*b^2 - b^3",
    "theorem bench_am_gm (a b : ℝ) : 2 * a * b ≤ a^2 + b^2",
    "theorem bench_sq_nonneg (a : ℝ) : 0 ≤ a^2",
    "theorem bench_mul_comm_real (a b : ℝ) : a * b = b * a",
]

INDUCTION = [
    "theorem bench_sum_gauss (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)",
    "theorem bench_sum_sq (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1)",
    # additional induction
    "theorem bench_sum_cube (n : ℕ) : 4 * ∑ k ∈ Finset.range (n + 1), k ^ 3 = (n * (n + 1)) ^ 2",
    "theorem bench_geom_sum (n : ℕ) : ∑ k ∈ Finset.range (n + 1), 2 ^ k + 1 = 2 ^ (n + 1)",
    "theorem bench_sum_odd (n : ℕ) : ∑ k ∈ Finset.range n, (2 * k + 1) = n ^ 2",
]

HARD = [
    # Multi-step `have` with specific Mathlib lemmas
    "theorem bench_hard_deriv (a : ℝ) : HasDerivAt (fun x => 2 * Real.sin x) (2 * Real.cos a) a",
    "theorem bench_hard_prime_inf : ∀ n : ℕ, ∃ p, n ≤ p ∧ Nat.Prime p",
    # sqrt: needs Real.sqrt_sq
    "theorem bench_hard_sqrt (a : ℝ) (ha : 0 ≤ a) : Real.sqrt (a ^ 2) = a",
    # continuous composition: needs Continuous.comp or fun_prop
    "theorem bench_hard_cont_comp (f g : ℝ → ℝ) (hf : Continuous f) (hg : Continuous g) : Continuous (f ∘ g)",
    # chain rule sin(2x): needs HasDerivAt.comp
    "theorem bench_hard_chain (a : ℝ) : HasDerivAt (fun x => Real.sin (2 * x)) (2 * Real.cos (2 * a)) a",
    # irrational sqrt 2: direct Mathlib lemma
    "theorem bench_hard_irrational_sqrt2 : Irrational (Real.sqrt 2)",
    # integer mod mod: needs Int.emod_emod_of_dvd
    "theorem bench_hard_emod (a b c : ℤ) (h : c ∣ b) : a % b % c = a % c",
    # finset card of even numbers: needs Finset manipulation
    "theorem bench_hard_card_filter (n : ℕ) : ((Finset.range (2 * n)).filter (fun k => k % 2 = 0)).card = n",
]

COMPETITION = [
    # Cauchy-Schwarz inequality: (∑ fᵢgᵢ)² ≤ (∑ fᵢ²)(∑ gᵢ²)
    "theorem bench_comp_cauchy_schwarz (n : ℕ) (f g : Fin n → ℝ) : (∑ i, f i * g i) ^ 2 ≤ (∑ i, f i ^ 2) * (∑ i, g i ^ 2)",
    # Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p
    "theorem bench_comp_wilson (p : ℕ) (hp : Nat.Prime p) : ((p - 1)! : ZMod p) = -1",
]

ALL = LOGIC + ALGEBRA + INDUCTION + HARD + COMPETITION

CATS = [
    ("logic       (命題論理)",     "logic",       LOGIC),
    ("algebra     (ring/omega)",   "algebra",     ALGEBRA),
    ("induction   (帰納法)",       "induction",   INDUCTION),
    ("hard        (多ステップ)",   "hard",        HARD),
    ("competition (競技数学)",     "competition", COMPETITION),
]


def append_log(label: str, suite: str, test_hash: str, scores: dict[str, tuple[int, int]], total_pass: int, total: int):
    exists = LOG_FILE.exists()
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_HEADER)
        if not exists:
            writer.writeheader()
        writer.writerow({
            "date":        date.today().isoformat(),
            "label":       label,
            "suite":       suite,
            "test_hash":   test_hash,
            "logic":       f"{scores['logic'][0]}/{scores['logic'][1]}",
            "algebra":     f"{scores['algebra'][0]}/{scores['algebra'][1]}",
            "induction":   f"{scores['induction'][0]}/{scores['induction'][1]}",
            "hard":        f"{scores['hard'][0]}/{scores['hard'][1]}",
            "competition": f"{scores['competition'][0]}/{scores['competition'][1]}",
            "total":       f"{total_pass}/{total}",
            "pct":         f"{total_pass / total * 100:.0f}%",
        })
    print(f"\n→ 結果を {LOG_FILE.name} に追記しました (suite: {suite!r}, label: {label!r}, test_hash: {test_hash})")


def run_benchmark(save_label: str | None = None, suite: str = "core"):
    test_hash = compute_test_hash(ALL)
    index = load_index()
    cached = sum(1 for s in ALL if cache_key(s) in index)
    print(f"=== ベンチマーク開始: {len(ALL)} 件 ({cached} キャッシュ済 / {len(ALL)-cached} 未計測) ===")
    print(f"    suite: {suite}, test_hash: {test_hash}\n")

    results = prove_all(ALL, dry_run=True)

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
        append_log(save_label, suite, test_hash, scores, total_pass, total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="auto_prove.py の証明カバレッジを計測する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python3 benchmark.py\n"
            "  python3 benchmark.py --save 'tauto追加'\n"
            "  python3 benchmark.py --save 'label' --suite hard_v2"
        ),
    )
    parser.add_argument("--save", metavar="LABEL", help="結果を bench_log.csv に追記する")
    parser.add_argument("--suite", metavar="NAME", default="core",
                        help="スイート名（デフォルト: core）。--save なしでは無視される")
    args = parser.parse_args()

    if args.suite != "core" and args.save is None:
        parser.error("--suite は --save と一緒に使ってください")

    run_benchmark(save_label=args.save, suite=args.suite)
