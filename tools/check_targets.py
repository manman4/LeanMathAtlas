#!/usr/bin/env python3
"""Dry-run selected theorems while reusing one REPL per file."""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

# Add tools dir to path
sys.path.insert(0, str(Path(__file__).parent))

from auto_prove import prove_all, extract_preamble, prepare_proof_env
from batch_prove import extract_theorems

WORKDIR = Path(__file__).parent.parent


def parse_target(spec: str) -> tuple[Path, str]:
    if "::" not in spec:
        raise ValueError(f"Target must be FILE::theorem_name, got: {spec}")
    file_part, theorem_name = spec.split("::", 1)
    lean_file = Path(file_part)
    if not lean_file.is_absolute():
        lean_file = WORKDIR / lean_file
    return lean_file, theorem_name.strip()


def theorem_map(lean_file: Path) -> dict[str, str]:
    result = {}
    for stmt in extract_theorems(lean_file):
        parts = stmt.split()
        if len(parts) >= 2:
            result[parts[1]] = stmt
    return result


def run_targets(target_specs: list[str], theorem_timeout: int = 20,
                prepare_timeout: float | None = None) -> int:
    grouped: dict[Path, list[str]] = defaultdict(list)
    for spec in target_specs:
        lean_file, theorem_name = parse_target(spec)
        grouped[lean_file].append(theorem_name)

    total_failed = 0
    for lean_file, theorem_names in grouped.items():
        preamble = extract_preamble(lean_file)
        stmt_by_name = theorem_map(lean_file)
        selected = []
        missing = []
        for theorem_name in theorem_names:
            stmt = stmt_by_name.get(theorem_name)
            if stmt is None:
                missing.append(theorem_name)
            else:
                selected.append(stmt)

        try:
            display = lean_file.resolve().relative_to(WORKDIR)
        except ValueError:
            display = lean_file
        print(f"\n{'='*60}", flush=True)
        print(f"File: {display}", flush=True)

        for theorem_name in missing:
            total_failed += 1
            print(f"  ! theorem not found: {theorem_name}", flush=True)
        if not selected:
            continue

        session = base_env = None
        try:
            print("  [check] preparing REPL...", flush=True)
            session, base_env = prepare_proof_env(
                dry_run=True, preamble=preamble, use_proved=False,
                startup_timeout=prepare_timeout,
            )
            print(f"  [check] REPL ready; running {len(selected)} theorem(s)...", flush=True)
            results = []
            for index, stmt in enumerate(selected, start=1):
                theorem_name = stmt.split()[1] if len(stmt.split()) >= 2 else stmt
                print(f"  [check] ({index}/{len(selected)}) {theorem_name}", flush=True)
                result = prove_all(
                    [stmt],
                    dry_run=True,
                    preamble=preamble,
                    theorem_timeout=theorem_timeout,
                    session=session,
                    base_env=base_env,
                )
                results.extend(result)
        finally:
            if session is not None:
                session.close()

        for stmt, proof, goal, solve_time in results:
            theorem_name = stmt.split()[1] if len(stmt.split()) >= 2 else stmt
            if proof:
                print(f"  ✓ {theorem_name} ({solve_time:.1f}s)", flush=True)
                proof_display = "\n    ".join(proof.splitlines())
                print(f"    by {proof_display}", flush=True)
            else:
                total_failed += 1
                print(f"  ✗ {theorem_name} ({solve_time:.1f}s)", flush=True)
                if goal:
                    print(f"    goal: {goal_target_line(goal)}", flush=True)

    return total_failed


def goal_target_line(goal: str) -> str:
    for line in reversed(goal.splitlines()):
        if "⊢" in line:
            return line.strip()
    return goal.strip()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Target in FILE::theorem_name form. Repeatable.",
    )
    parser.add_argument(
        "--theorem-timeout",
        type=int,
        default=20,
        help="Total per-theorem timeout in seconds across all proof phases.",
    )
    parser.add_argument(
        "--prepare-timeout",
        type=float,
        default=None,
        help="Optional REPL startup timeout in seconds.",
    )
    args = parser.parse_args()

    if not args.target:
        parser.error("At least one --target FILE::theorem_name is required")

    sys.exit(1 if run_targets(
        args.target,
        theorem_timeout=args.theorem_timeout,
        prepare_timeout=args.prepare_timeout,
    ) else 0)
