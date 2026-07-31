#!/usr/bin/env python3
"""
Git Hook Validator Engine - Strategy-Aware
Supports both Conventional Commits (SemVer) and CalVer prefix validation.
"""
import sys
import re
import os
import json
from typing import List, Tuple, Optional

COMMIT_TYPES = ["feat", "fix", "docs", "refactor", "test", "chore",
                "style", "build", "ci", "perf", "revert"]

SEMVER_PATTERN = rf"^({'|'.join(COMMIT_TYPES)})(\([a-zA-Z0-9_\-]+\))?: .+"
CALVER_PATTERN = r"^v\d+\.\d+\.\d{8}\.\d+\s+.+"


def _find_sync_state() -> Optional[str]:
    """Search upward from script directory to find .sync-state.json."""
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        candidate = os.path.join(current, ".sync-state.json")
        if os.path.exists(candidate):
            return candidate
        current = os.path.dirname(current)
    return None


def _read_strategy() -> str:
    """Read version strategy from .sync-state.json."""
    state_file = _find_sync_state()
    if state_file:
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f).get("version_strategy", "semver")
        except (json.JSONDecodeError, IOError):
            pass
    return "semver"


def validate_commit_message(msg: str) -> Tuple[bool, str]:
    """Validate commit message against the active version strategy."""
    lines = msg.strip().splitlines()
    if not lines:
        return False, "Commit message cannot be empty."

    header = lines[0].strip()
    if len(header) > 72:
        return False, f"Commit message header too long ({len(header)} chars). Maximum allowed is 72 chars."

    warning_msg = ""
    if len(header) > 50:
        warning_msg = f"[WARNING] Header length is {len(header)} chars. Recommended limit is 50 chars."

    strategy = _read_strategy()
    if strategy == "calver":
        if not re.match(CALVER_PATTERN, header):
            return False, "Invalid commit format. Expected CalVer: v1.0.YYYYMMDD.Z summary"
    else:
        if not re.match(SEMVER_PATTERN, header):
            types_str = ', '.join(COMMIT_TYPES)
            return False, f"Invalid commit format. Expected: type(scope): summary. Allowed types: {types_str}"

    return True, warning_msg or "Commit message is valid."


if __name__ == "__main__":
    if len(sys.argv) > 1:
        commit_msg_file = sys.argv[1]
        if os.path.exists(commit_msg_file):
            with open(commit_msg_file, "r", encoding="utf-8") as f:
                content = f.read()
            valid, info = validate_commit_message(content)
            if not valid:
                print(f"[ERROR] {info}", file=sys.stderr)
                sys.exit(1)
            elif "[WARNING]" in info:
                print(info, file=sys.stderr)
    print("[SUCCESS] Commit message validation passed.")
    sys.exit(0)
