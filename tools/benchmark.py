#!/usr/bin/env python3
from __future__ import annotations
"""
Coverage benchmark: measure how many theorems auto_prove.py can solve.

Test cases live in tools/bench/*.lean — each file holds one category's
theorem stubs plus its own `open` / `variable` preamble.

Categories:
  logic       — propositional logic (tauto / BFS target)
  algebra     — ring / omega
  induction   — summation formulas (open BigOperators)
  hard        — multi-step have (expected failures)
  competition — competition math (open BigOperators / scoped Nat)
"""
import sys
import csv
import json
import time
import hashlib
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auto_prove import prove_all, cache_key, extract_preamble
from batch_prove import extract_theorems

BENCH_DIR       = Path(__file__).parent / "bench"
LOG_FILE        = Path(__file__).parent / "bench_log.csv"
BENCH_CACHE_FILE = Path(__file__).parent / ".bench_cache.json"
LOG_HEADER = ["date", "label", "suite", "test_hash", "logic", "algebra", "induction", "hard", "competition", "total", "pct", "elapsed_sec"]

# Category definitions: (display_label, csv_key, bench_filename)
CATS_DEF = [
    ("logic       (命題論理)",   "logic",       "logic.lean"),
    ("algebra     (ring/omega)", "algebra",     "algebra.lean"),
    ("induction   (帰納法)",     "induction",   "induction.lean"),
    ("hard        (多ステップ)", "hard",         "hard.lean"),
    ("competition (競技数学)",   "competition", "competition.lean"),
]


def load_categories() -> list[tuple[str, str, list[str], str]]:
    """Load (display, key, theorems, preamble) for each category from bench/*.lean."""
    cats = []
    for display, key, fname in CATS_DEF:
        path = BENCH_DIR / fname
        preamble = extract_preamble(path)
        theorems = extract_theorems(path)
        cats.append((display, key, theorems, preamble))
    return cats


def load_bench_cache() -> dict:
    if BENCH_CACHE_FILE.exists():
        return json.loads(BENCH_CACHE_FILE.read_text(encoding="utf-8"))
    return {}

def save_bench_cache(cache: dict):
    BENCH_CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def compute_test_hash(problems: list[str]) -> str:
    content = "\n".join(sorted(problems))
    return hashlib.sha256(content.encode()).hexdigest()[:8]


def append_log(label: str, suite: str, test_hash: str, scores: dict[str, tuple[int, int]], total_pass: int, total: int, elapsed_sec: float):
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
            "competition":  f"{scores['competition'][0]}/{scores['competition'][1]}",
            "total":        f"{total_pass}/{total}",
            "pct":          f"{total_pass / total * 100:.0f}%",
            "elapsed_sec":  f"{elapsed_sec:.0f}",
        })
    print(f"\n→ 結果を {LOG_FILE.name} に追記しました (suite: {suite!r}, label: {label!r}, test_hash: {test_hash})")


def run_benchmark(save_label: str | None = None, suite: str = "core", clear_cache: bool = False):
    cats = load_categories()
    all_stmts = [s for _, _, stmts, _ in cats for s in stmts]
    test_hash = compute_test_hash(all_stmts)

    bench_cache = {} if clear_cache else load_bench_cache()
    if clear_cache:
        print("  [cache] クリアしました")

    n_cached = sum(1 for s in all_stmts if cache_key(s) in bench_cache)
    n_uncached = len(all_stmts) - n_cached
    print(f"=== ベンチマーク開始: {len(all_stmts)} 件 ({n_cached} キャッシュ済 / {n_uncached} 未計測) ===")
    print(f"    suite: {suite}, test_hash: {test_hash}\n")

    # Prove uncached theorems per category (each with its own preamble)
    solve_times: dict[str, float] = {}
    for _, key, stmts, preamble in cats:
        to_prove = [s for s in stmts if cache_key(s) not in bench_cache]
        if not to_prove:
            continue
        raw = prove_all(to_prove, dry_run=True, preamble=preamble)
        for stmt, proof, goal, t in raw:
            solve_times[stmt] = t
            if proof:
                bench_cache[cache_key(stmt)] = {"proof": proof, "solve_time_sec": t}
    save_bench_cache(bench_cache)

    elapsed_sec = sum(solve_times.values())

    total_pass = total_fail = 0
    scores: dict[str, tuple[int, int]] = {}
    print()
    for display, key, stmts, _ in cats:
        ok = sum(1 for s in stmts if cache_key(s) in bench_cache)
        scores[key] = (ok, len(stmts))
        total_pass += ok
        total_fail += len(stmts) - ok
        print(f"{display}: {ok}/{len(stmts)} ✓")
        for s in stmts:
            cached = cache_key(s) in bench_cache
            name = s.split()[1]
            icon = "✓" if cached else "✗"
            proof_hint = ""
            if cached and key in bench_cache.get(cache_key(s), {}):
                p = bench_cache[cache_key(s)].get("proof", "")
                proof_hint = f" ({p.split(chr(10))[0][:40]})" if p else ""
            cached_mark = " [cached]" if cache_key(s) in bench_cache and s not in solve_times else ""
            print(f"  {icon} {name}{proof_hint}{cached_mark}")
        print()

    total = total_pass + total_fail
    pct = total_pass / total * 100
    print(f"{'='*55}")
    print(f"合計: {total_pass}/{total} ({pct:.0f}%)  [累計証明時間 {elapsed_sec:.0f}s]")

    if save_label is not None:
        append_log(save_label, suite, test_hash, scores, total_pass, total, elapsed_sec)


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
    parser.add_argument("--clear-cache", action="store_true",
                        help=".bench_cache.json を無視して全定理を再実行する")
    args = parser.parse_args()

    if args.suite != "core" and args.save is None:
        parser.error("--suite は --save と一緒に使ってください")

    run_benchmark(save_label=args.save, suite=args.suite, clear_cache=args.clear_cache)
