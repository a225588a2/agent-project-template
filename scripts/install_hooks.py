#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def install_hooks(target_dir=None):
    if not target_dir:
        target_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    git_dir = os.path.join(target_dir, ".git")
    hooks_dir = os.path.join(git_dir, "hooks")
    
    if not os.path.exists(git_dir):
        print(f"[Warning] No .git directory found at {target_dir}. Skipping hook installation.", file=sys.stderr)
        return False
        
    os.makedirs(hooks_dir, exist_ok=True)
    
    pre_commit_wrapper = """#!/bin/sh

is_runnable() {
  if command -v "$1" >/dev/null 2>&1; then
    "$1" -c "import sys" >/dev/null 2>&1
    return $?
  fi
  return 1
}

# Find python executable
if is_runnable "python3"; then
  PYTHON_EXE="python3"
elif is_runnable "python"; then
  PYTHON_EXE="python"
elif is_runnable "py"; then
  PYTHON_EXE="py"
else
  echo "[Git Hook Error] Python is not installed, not in PATH, or not runnable." >&2
  exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
"$PYTHON_EXE" "$REPO_ROOT/scripts/git_hook_validator.py" pre-commit
exit $?
"""

    commit_msg_wrapper = """#!/bin/sh

is_runnable() {
  if command -v "$1" >/dev/null 2>&1; then
    "$1" -c "import sys" >/dev/null 2>&1
    return $?
  fi
  return 1
}

# Find python executable
if is_runnable "python3"; then
  PYTHON_EXE="python3"
elif is_runnable "python"; then
  PYTHON_EXE="python"
elif is_runnable "py"; then
  PYTHON_EXE="py"
else
  echo "[Git Hook Error] Python is not installed, not in PATH, or not runnable." >&2
  exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
"$PYTHON_EXE" "$REPO_ROOT/scripts/git_hook_validator.py" commit-msg "$1"
exit $?
"""

    # Write pre-commit hook
    pre_commit_path = os.path.join(hooks_dir, "pre-commit")
    with open(pre_commit_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(pre_commit_wrapper)
    
    # Write commit-msg hook
    commit_msg_path = os.path.join(hooks_dir, "commit-msg")
    with open(commit_msg_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(commit_msg_wrapper)

    try:
        os.chmod(pre_commit_path, 0o755)
        os.chmod(commit_msg_path, 0o755)
    except Exception:
        pass
        
    print("[Success] Git hooks (pre-commit, commit-msg) installed successfully.")
    return True

if __name__ == "__main__":
    install_hooks()
