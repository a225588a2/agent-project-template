#!/usr/bin/env python3
"""
Git Hook Validator Engine
"""
import sys
import re
import os
from typing import List, Tuple, Optional

COMMIT_TYPES = ["feat", "fix", "docs", "refactor", "test", "chore", "style", "build", "ci"]

def validate_commit_message(msg: str) -> Tuple[bool, str]:
    lines = msg.strip().splitlines()
    if not lines:
        return False, "Commit message cannot be empty."
    
    header = lines[0].strip()
    # Check length
    if len(header) > 72:
        return False, f"Commit message header too long ({len(header)} chars). Maximum allowed is 72 chars."
    
    warning_msg = ""
    if len(header) > 50:
        warning_msg = f"[WARNING] Header length is {len(header)} chars. Recommended limit is 50 chars."
    
    pattern = rf"^({'|'.join(COMMIT_TYPES)})(\([a-zA-Z0-9_\-]+\))?: .+"
    if not re.match(pattern, header):
        return False, f"Invalid commit format. Header must match pattern: type(scope): summary. Allowed types: {', '.join(COMMIT_TYPES)}"
    
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
