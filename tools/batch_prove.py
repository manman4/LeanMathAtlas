#!/usr/bin/env python3
"""Batch prove all unproven theorems in a .lean file using auto_prove."""
from __future__ import annotations
import sys, re, subprocess, json
from pathlib import Path

# Add tools dir to path
sys.path.insert(0, str(Path(__file__).parent))
from auto_prove import prove_all, extract_preamble, cache_key, load_index, ensured_proof_entry

WORKDIR = Path(__file__).parent.parent

def _assign_pos_depth0(text: str) -> int:
    """Return index of first ':=' at parenthesis depth 0, or -1."""
    depth = 0
    i = 0
    while i < len(text):
        c = text[i]
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif text[i:i+2] == ':=' and depth == 0:
            return i
        i += 1
    return -1


def extract_theorems(lean_file: Path) -> list[str]:
    """Extract theorem signatures (without body) from a .lean file."""
    text = lean_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    theorems = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if re.match(r'^theorem\s+', stripped):
            sig_lines = [stripped]
            j = i + 1
            while j < len(lines):
                next_stripped = lines[j].strip()
                full_so_far = ' '.join(sig_lines)
                # Stop when := appears at parenthesis depth 0
                if _assign_pos_depth0(full_so_far) != -1:
                    break
                if lines[j].startswith('    ') and not re.match(r'^theorem|^def|^lemma', next_stripped):
                    sig_lines.append(next_stripped)
                    j += 1
                else:
                    break
            full = ' '.join(sig_lines)
            # Strip proof body: remove from the first := at depth 0
            pos = _assign_pos_depth0(full)
            sig = full[:pos].rstrip() if pos != -1 else full
            sig = re.sub(r'\s+', ' ', sig)
            theorems.append(sig)
            i = j
        else:
            i += 1
    return theorems


def run_file(lean_file: Path, batch_size: int = 10, dry_run: bool = False, use_proved: bool = False) -> dict:
    """Prove all unproven theorems in a .lean file. Returns {'passed': n, 'failed': n}."""
    preamble = extract_preamble(lean_file)
    print(f"\n{'='*60}")
    try:
        display = lean_file.resolve().relative_to(WORKDIR)
    except ValueError:
        display = lean_file
    print(f"File: {display}")
    if preamble:
        print(f"Preamble: {preamble!r}")

    theorems = extract_theorems(lean_file)
    index = load_index()
    unproven = [t for t in theorems if ensured_proof_entry(index.get(cache_key(t))) is None]
    print(f"Theorems: {len(theorems)} total, {len(unproven)} unproven")

    if not unproven:
        print("  All already proven!")
        return {'passed': 0, 'failed': 0}

    total_passed = total_failed = 0
    for batch_start in range(0, len(unproven), batch_size):
        batch = unproven[batch_start:batch_start + batch_size]
        print(f"\n  Batch {batch_start//batch_size + 1}: proving {len(batch)} theorems...")
        try:
            results = prove_all(batch, dry_run=dry_run, preamble=preamble, use_proved=use_proved)
        except RuntimeError as err:
            print(f"  [error] {err}")
            total_failed += len(batch)
            continue
        passed = sum(1 for _, proof, _, _ in results if proof)
        failed = len(batch) - passed
        total_passed += passed
        total_failed += failed
        for stmt, proof, goal, t in results:
            name = stmt.split()[1] if len(stmt.split()) > 1 else stmt[:40]
            if proof:
                print(f"    ✓ {name}")
            else:
                print(f"    ✗ {name}")

    print(f"\n  Result: {total_passed}/{total_passed+total_failed} proved")
    return {'passed': total_passed, 'failed': total_failed}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path, help=".lean files to process")
    parser.add_argument("--batch", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--use-proved", action="store_true",
                        help="import previously proved theorems into the REPL during proof search")
    args = parser.parse_args()

    if not args.files:
        # Default: all .lean files in LeanMathAtlas/
        exclude = {"ProvedTheorems.lean", "Basic.lean", "Exercises.lean", "Tactics.lean"}
        args.files = sorted((WORKDIR / "LeanMathAtlas").rglob("*.lean"))
        args.files = [f for f in args.files if f.name not in exclude]

    grand_passed = grand_failed = 0
    for f in args.files:
        result = run_file(f, batch_size=args.batch, dry_run=args.dry_run, use_proved=args.use_proved)
        grand_passed += result['passed']
        grand_failed += result['failed']

    print(f"\n{'='*60}")
    print(f"Grand total: {grand_passed}/{grand_passed+grand_failed} proved")
