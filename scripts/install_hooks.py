#!/usr/bin/env python3
"""
Git Hook Installation Script
"""
import os
import sys
from utils import resolve_repo_root

HOOK_SCRIPT = """#!/bin/sh
python scripts/git_hook_validator.py "$1"
"""

def install_hooks():
    root = resolve_repo_root()
    hooks_dir = os.path.join(root, ".git", "hooks")
    if not os.path.exists(hooks_dir):
        print(f"[ERROR] .git/hooks directory not found at {hooks_dir}")
        return
    
    commit_msg_hook = os.path.join(hooks_dir, "commit-msg")
    with open(commit_msg_hook, "w", encoding="utf-8", newline="\n") as f:
        f.write(HOOK_SCRIPT)
    
    if hasattr(os, "chmod"):
        os.chmod(commit_msg_hook, 0o755)
    print(f"[HOOKS] Successfully installed commit-msg hook at {commit_msg_hook}")

if __name__ == "__main__":
    install_hooks()
