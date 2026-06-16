from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from auto_prove_store import WORKDIR

FAILURE_LOG_FILE = WORKDIR / ".auto_prove_failures.jsonl"


def failure_log_enabled() -> bool:
    return os.environ.get("AUTO_PROVE_LOG_FAILURES", "1") != "0"


def log_failure(entry: dict):
    """Append a lightweight theorem-failure record for later analysis."""
    if not failure_log_enabled():
        return
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **entry,
    }
    with FAILURE_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
