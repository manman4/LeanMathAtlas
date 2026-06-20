#!/usr/bin/env python3
"""
Lean 4 automated theorem prover.
- Accumulates proofs in ProvedTheorems.lean (correctness guaranteed by the Lean compiler)
- .proof_index.json for fast lookup (hash → theorem name)
- Interactive REPL: breaks immediately on the first successful tactic
- Rule-based tactic filtering: narrows candidates from the goal string
- Iterative proof search: BFS over tactic sequences via REPL tactic mode (time-limited)
"""

from __future__ import annotations
from pathlib import Path
import sys
import time

from auto_prove_repl import ReplSession, has_error, prepare_proof_env
from auto_prove_failure_log import log_failure
from auto_prove_store import (
    AUTO_PROVED_DIR,
    cache_key,
    ensured_proof_entry,
    extract_preamble,
    lean_name_from,
    load_index,
    persist_proof,
    save_index,
)
from auto_prove_tactics import (
    DEFAULT_THEOREM_TIMEOUT,
    HAVE_STAGE1_LIMIT,
    SEARCH_TACTICS,
    STEP_TIME_LIMIT,
    probe_apply_subgoal,
    extract_try_this,
    fact_preamble,
    limited_have_candidates,
    prove_iterative,
    prove_with_have,
    prove_with_two_haves,
    normalize_goal_shape,
    search_normalization_prefixes,
    verify_search_suggestion,
    select_tactics,
    single_line_closers,
    to_example,
    verify_tactic_variants,
)

# ────────────────────────────────────────────────
# Automated proving
# ────────────────────────────────────────────────

def prove_all(theorems: list, dry_run: bool = False, preamble: str = "",
              skip_phase17: bool = False, use_proved: bool = False,
              theorem_timeout: int | None = DEFAULT_THEOREM_TIMEOUT,
              session: ReplSession | None = None, base_env: int | None = None) -> list:
    """Attempt to prove each theorem.

    dry_run=True: skip ProvedTheorems.lean writes and cache updates (used by benchmark.py
    so that one run cannot contaminate the next).
    skip_phase17=True: bypass Phase 1.7 (used by A/B coverage tests).
    use_proved=True: import LeanMathAtlas.ProvedTheorems into the REPL so previously
    proved theorems are available as lemmas during proof search.
    theorem_timeout: total per-theorem time budget in seconds across all phases.
    session/base_env: optional preloaded proof environment to reuse across calls.
    """
    index = load_index()
    uncached = theorems if dry_run else [
        s for s in theorems
        if ensured_proof_entry(index.get(cache_key(s))) is None
    ]

    new_results: dict[str, tuple] = {}

    if uncached:
        owns_session = session is None or base_env is None
        if owns_session:
            session, base_env = prepare_proof_env(dry_run=dry_run, preamble=preamble, use_proved=use_proved)
        try:
            for stmt in uncached:
                example = to_example(stmt)
                t_stmt = time.monotonic()
                theorem_deadline = None if theorem_timeout is None else t_stmt + theorem_timeout

                def timed_out() -> bool:
                    return theorem_deadline is not None and time.monotonic() >= theorem_deadline

                # Fetch the goal
                goal = ""
                resp = session.send({"cmd": f"{example} := by sorry", "env": base_env})
                sorries = resp.get("sorries", [])
                if sorries:
                    goal = sorries[0].get("goal", "")

                # Phase 1: try each filtered tactic in one shot
                proof = None
                search_prefixes = search_normalization_prefixes(goal)
                for t in select_tactics(goal):
                    if timed_out():
                        break
                    if t in SEARCH_TACTICS:
                        search_attempts = search_prefixes
                    else:
                        search_attempts = [""]
                    for norm_prefix in search_attempts:
                        if timed_out():
                            break
                        resp = session.send({"cmd": f"{example} := by\n  {norm_prefix}{t}", "env": base_env})
                        if not has_error(resp):
                            if t in SEARCH_TACTICS:
                                extracted = extract_try_this(resp)
                                if extracted is None:
                                    continue
                                proof = f"{norm_prefix}{extracted}" if norm_prefix else extracted
                            else:
                                proof = f"{norm_prefix}{t}" if norm_prefix else t
                            if not dry_run:
                                lean_name = lean_name_from(stmt)
                                persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                            break
                        if t not in SEARCH_TACTICS:
                            continue
                        extracted = extract_try_this(resp)
                        if extracted is None:
                            continue
                        verified = verify_search_suggestion(
                            session, example, base_env,
                            extracted, goal,
                            normalization_prefixes=search_prefixes,
                        )
                        if verified is None:
                            continue
                        proof = verified
                        if not dry_run:
                            lean_name = lean_name_from(stmt)
                            persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                        break
                    if not has_error(resp):
                        break

                # Phase 1.5: Fact typeclass preamble + tactics
                # Handles lemmas that require [Fact (Nat.Prime p)] typeclass.
                # Tries SIMPLE_TACTICS first (simp/norm_num may find the goal if the target
                # lemma is @[simp]), then SEARCH_TACTICS as fallback.
                # For search tactics (exact?/simp?), we extract the "Try this:" suggestion even
                # if the response has errors (exact? may report an error while still suggesting
                # the right lemma), then verify the suggestion in a separate REPL call.
                if proof is None:
                    fact_block = fact_preamble(stmt)
                    if fact_block:
                        # Preprocessing variants: try cast normalisation before search tactics.
                        # norm_cast / push_cast can reveal ZMod.wilsons_lemma and similar
                        # lemmas that exact? misses when the goal has coercion noise.
                        _cast_prefixes = ["", "norm_cast\n  ", "push_cast\n  "]
                        _phase15_tactics = SIMPLE_TACTICS + SEARCH_TACTICS
                        for _cast in _cast_prefixes:
                            if proof is not None:
                                break
                            for t in _phase15_tactics:
                                if timed_out():
                                    break
                                resp = session.send({
                                    "cmd": f"{example} := by\n  {fact_block}\n  {_cast}{t}",
                                    "env": base_env
                                })
                                if t in SEARCH_TACTICS:
                                    # Extract suggestion regardless of errors, then verify separately
                                    extracted = extract_try_this(resp)
                                    if extracted:
                                        if timed_out():
                                            break
                                        verified = verify_search_suggestion(
                                            session, example, base_env,
                                            extracted, goal,
                                            prefix=f"{fact_block}\n  {_cast}",
                                        )
                                        if verified is not None:
                                            proof = verified
                                            if not dry_run:
                                                lean_name = lean_name_from(stmt)
                                                persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                                            break
                                elif not has_error(resp):
                                    proof = f"{fact_block}\n  {_cast}{t}"
                                    if not dry_run:
                                        lean_name = lean_name_from(stmt)
                                        persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                                    break

                # Phase 1.6: apply? + all_goals closer
                # apply? finds any Mathlib lemma that partially matches the goal,
                # then closes remaining subgoals with standard tactics.
                # More powerful than exact? for goals that need a lemma application
                # followed by a simple finishing step (e.g. Pigeonhole + card simp).
                if proof is None:
                    # Try plain apply? first, then with Fact preamble if present
                    _preamble = fact_preamble(stmt)
                    _prefixes = [""]
                    if _preamble:
                        _prefixes.append(_preamble)
                    for _pre in _prefixes:
                        if proof is not None:
                            break
                        if timed_out():
                            break
                        for _norm in search_prefixes:
                            if timed_out():
                                break
                            _pre_block = f"  {_pre}\n  {_norm}" if _pre else f"  {_norm}"
                            _resp = session.send({
                                "cmd": f"{example} := by\n{_pre_block}apply?",
                                "env": base_env
                            })
                            _sug = extract_try_this(_resp)
                            if not _sug or not (_sug.startswith("apply ") or _sug.startswith("refine ")):
                                continue
                            _prefix_lines = [_pre, f"{_norm}{_sug}"] if _pre else [f"{_norm}{_sug}"]
                            _remaining_goal = probe_apply_subgoal(
                                session, example, base_env, _prefix_lines[:-1], _prefix_lines[-1]
                            )
                            if _remaining_goal == "":
                                proof = f"{_pre}\n  {_norm}{_sug}" if _pre else f"{_norm}{_sug}"
                                if not dry_run:
                                    lean_name = lean_name_from(stmt)
                                    persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                                break
                            _closers = single_line_closers(_remaining_goal or goal)
                            for _closer in _closers:
                                if timed_out():
                                    break
                                _cmd = (
                                    f"{example} := by\n  {_pre}\n  {_norm}{_sug}\n  all_goals {_closer}"
                                    if _pre else
                                    f"{example} := by\n  {_norm}{_sug}\n  all_goals {_closer}"
                                )
                                _resp2 = session.send({"cmd": _cmd, "env": base_env})
                                if not has_error(_resp2):
                                    proof = (
                                        f"{_pre}\n  {_norm}{_sug}\n  all_goals {_closer}"
                                        if _pre else
                                        f"{_norm}{_sug}\n  all_goals {_closer}"
                                    )
                                    if not dry_run:
                                        lean_name = lean_name_from(stmt)
                                        persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                                    break

                # Phase 2: if one-shot failed, try iterative BFS (time-limited)
                if proof is None and not timed_out():
                    remaining = None if theorem_deadline is None else max(0.0, theorem_deadline - time.monotonic())
                    phase_limit = STEP_TIME_LIMIT if remaining is None else min(STEP_TIME_LIMIT, remaining)
                    print(f"  [step] iterative search (up to {phase_limit:.0f}s)...")
                    step_proof = prove_iterative(session, example, base_env, time_limit=max(1, int(phase_limit)),
                                                 deadline=theorem_deadline)
                    if step_proof:
                        proof = step_proof
                        if not dry_run:
                            lean_name = lean_name_from(stmt)
                            persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)

                # Phase 3 (last resort): have-augmented proofs
                # Tried after BFS because it costs extra REPL calls.
                # First try one intermediate fact, then a tightly bounded two-stage
                # have search where the second candidate is generated from the
                # remaining goal after the first have.
                if proof is None and not skip_phase17 and not timed_out():
                    for have_line in limited_have_candidates(goal, HAVE_STAGE1_LIMIT):
                        if timed_out():
                            break
                        p = prove_with_have(session, example, base_env, have_line, theorem_deadline)
                        if p:
                            proof = p
                            if not dry_run:
                                lean_name = lean_name_from(stmt)
                                persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                            break
                        p = prove_with_two_haves(session, example, base_env, have_line, theorem_deadline)
                        if p:
                            proof = p
                            if not dry_run:
                                lean_name = lean_name_from(stmt)
                                persist_proof(stmt, proof, goal, lean_name, preamble, index, use_proved)
                            break

                if proof is None and timed_out():
                    print(f"  [timeout] theorem budget exceeded ({theorem_timeout}s)")
                if proof is None:
                    log_failure({
                        "stmt": stmt,
                        "goal": goal,
                        "normalized_goal_shape": normalize_goal_shape(goal),
                        "timed_out": timed_out(),
                        "theorem_timeout_sec": theorem_timeout,
                        "search_prefixes": search_prefixes,
                        "selected_tactics": select_tactics(goal),
                        "solve_time_sec": time.monotonic() - t_stmt,
                    })

                new_results[stmt] = (proof, goal, time.monotonic() - t_stmt)

        finally:
            if owns_session:
                session.close()
            if not dry_run:
                save_index(index)

    # Collect results in the original order
    results = []
    for stmt in theorems:
        if stmt in new_results:
            proof, goal, solve_time = new_results[stmt]
        else:
            lean_name = ensured_proof_entry(index.get(cache_key(stmt))) or ""
            proof = lean_name  # already proved — return the Lean name
            goal = ""
            solve_time = 0.0
        results.append((stmt, proof, goal, solve_time))
    return results

# ────────────────────────────────────────────────
# Test theorems
# ────────────────────────────────────────────────

TESTS = [
    "theorem t1 : (1:ℕ) + 1 = 2",
    "theorem t2 (n : ℕ) : n + 0 = n",
    "theorem t3 (a b : ℤ) : a + b = b + a",
    "theorem t4 (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2",
    "theorem t5 (a b c : ℕ) : (a + b) + c = a + (b + c)",
    "theorem t6 (n : ℕ) : 2 * ∑ k ∈ Finset.range (n + 1), k = n * (n + 1)",
    "theorem t7 (n : ℕ) : 6 * ∑ k ∈ Finset.range (n + 1), k ^ 2 = n * (n + 1) * (2 * n + 1)",
]

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, help="source .lean file to extract preamble from")
    parser.add_argument("--use-proved", action="store_true",
                        help="import previously proved theorems into the REPL during proof search")
    parser.add_argument("--theorem-timeout", type=int, default=DEFAULT_THEOREM_TIMEOUT,
                        help="total per-theorem timeout in seconds across all proof phases")
    parser.add_argument("theorems", nargs="*")
    args = parser.parse_args()

    targets = args.theorems if args.theorems else TESTS
    preamble = extract_preamble(args.file) if args.file else ""
    if preamble:
        print(f"[preamble] {preamble!r}")

    index = load_index()
    cached_count = sum(1 for s in targets if ensured_proof_entry(index.get(cache_key(s))) is not None)
    print(f"[run] {len(targets)} theorems ({cached_count} cached / {len(targets) - cached_count} uncached)")

    t0 = time.time()
    try:
        results = prove_all(
            targets,
            preamble=preamble,
            use_proved=args.use_proved,
            theorem_timeout=args.theorem_timeout,
        )
    except RuntimeError as err:
        print(f"[error] {err}")
        sys.exit(1)
    elapsed = time.time() - t0

    passed = failed = 0
    for stmt, proof, goal, solve_time in results:
        print(f"\n{'─'*60}")
        print(f"target: {stmt}")
        if goal:
            print(f"  goal: {goal}")
        if proof:
            proof_display = "\n    ".join(proof.split("\n"))
            print(f"  ✓ by\n    {proof_display}")
            passed += 1
        else:
            print(f"  ✗ proof not found")
            failed += 1

    print(f"\n{'─'*60}")
    print(f"total: {passed} passed / {failed} failed / {elapsed:.1f}s")
    if passed > 0:
        print(f"  → saved to {AUTO_PROVED_DIR.relative_to(WORKDIR)}/ + {LEAN_DB_FILE.relative_to(WORKDIR)}")

if __name__ == "__main__":
    main()
