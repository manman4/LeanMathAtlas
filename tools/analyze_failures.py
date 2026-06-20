#!/usr/bin/env python3
"""Summarize local auto_prove failure logs by reusable goal classes."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from auto_prove_failure_log import FAILURE_LOG_FILE
from auto_prove_tactics import goal_target, normalize_goal_shape


def load_failures(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def dedupe_failures(rows: list[dict]) -> list[dict]:
    latest: dict[tuple[str, str], dict] = {}
    for row in rows:
        key = (row.get("stmt", ""), row.get("goal", ""))
        latest[key] = row
    return list(latest.values())


def classify_goal(goal: str) -> str:
    target = goal_target(goal)
    if "HasDerivAt" in target or "HasFDerivAt" in target:
        return "derivative"
    if "Tendsto" in target:
        return "limit"
    if "Continuous" in target or "Differentiable" in target:
        return "continuity"
    if "inner" in target or "⟪" in target or "‖" in target:
        return "inner_norm"
    if "normSq" in target or ("ℂ" in goal and "exp" in target):
        return "complex"
    if "∑" in target or "Finset" in target:
        return "finset_sum"
    if "ZMod" in goal or "ZMod" in target:
        return "zmod_cast"
    if "sin" in target or "cos" in target or "tan" in target:
        return "trig"
    if any(token in target for token in [" ≤ ", " ≥ ", " < ", " > "]):
        if "^" in target:
            return "power_inequality"
        return "inequality"
    if "^" in target:
        return "power_algebra"
    if " = " in target or "↔" in target:
        return "equality"
    return "other"


def tactic_family(tactic: str) -> str:
    if tactic in {"exact?", "simp?"}:
        return "search"
    if tactic.startswith("apply ") or tactic.startswith("refine "):
        return "apply_refine"
    if tactic.startswith("induction "):
        return "induction"
    if "fun_prop" in tactic:
        return "fun_prop"
    if "nlinarith" in tactic:
        return "nlinarith"
    if "linarith" in tactic:
        return "linarith"
    if "ring" in tactic:
        return "ring"
    if "omega" in tactic:
        return "omega"
    if "norm_num" in tactic:
        return "norm_num"
    if "norm_cast" in tactic or "push_cast" in tactic:
        return "cast"
    if "simp" in tactic:
        return "simp"
    if "aesop" in tactic or "tauto" in tactic:
        return "logic"
    if "HasDerivAt" in tactic or "hasDerivAt" in tactic:
        return "deriv_template"
    if "inner" in tactic or "norm_smul" in tactic:
        return "inner_norm"
    if "Fintype" in tactic:
        return "fintype"
    return "other"


def summarize(rows: list[dict]) -> list[str]:
    by_class: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_class[classify_goal(row.get("goal", ""))].append(row)

    lines = [
        f"log file: {FAILURE_LOG_FILE}",
        f"entries: {len(rows)} unique failures",
    ]
    for goal_class, group in sorted(by_class.items(), key=lambda item: (-len(item[1]), item[0])):
        timeouts = sum(1 for row in group if row.get("timed_out"))
        family_counts = Counter()
        shape_counts = Counter()
        prefix_counts = Counter()
        for row in group:
            shape = row.get("normalized_goal_shape") or normalize_goal_shape(row.get("goal", ""))
            if shape:
                shape_counts[shape] += 1
            for prefix in row.get("search_prefixes", []):
                label = (prefix or "<none>").replace("\n", "\\n").strip() or "<none>"
                prefix_counts[label] += 1
            for tactic in row.get("selected_tactics", []):
                family_counts[tactic_family(tactic)] += 1
        example = group[0].get("stmt", "")
        lines.append("")
        lines.append(
            f"[{goal_class}] count={len(group)} timed_out={timeouts}/{len(group)} "
            f"top_families={', '.join(f'{name}:{count}' for name, count in family_counts.most_common(5)) or 'none'}"
        )
        if shape_counts:
            lines.append(
                "top_shapes: "
                + ", ".join(f"{shape}:{count}" for shape, count in shape_counts.most_common(3))
            )
        if prefix_counts:
            lines.append(
                "search_prefixes: "
                + ", ".join(f"{name}:{count}" for name, count in prefix_counts.most_common(5))
            )
        if example:
            lines.append(f"example: {example}")
    return lines


if __name__ == "__main__":
    rows = dedupe_failures(load_failures(FAILURE_LOG_FILE))
    for line in summarize(rows):
        print(line)
