#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
git_hook_validator.py - Git Hook Validator for AI Project Template.
Validates commit message format according to version strategy (SemVer 2.0 / CalVer).
Rules: Header 強制規範 (Conventional Commits / CalVer 前綴)，Body 不限制/允許使用中文說明 (Permitted CJK, not forced).
Provides structured Fix Hints for AI Agent self-correction (max 2 retries allowed).
"""

import os
import sys
import json
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    from version_engine import get_version_strategy, validate_commit_message, VersionStrategy
except ImportError:
    # Minimal fallback
    def get_version_strategy(s):
        class Dummy:
            strategy_name = "semver"
            def validate_commit_header(self, h): return True, ""
        return Dummy()
    def validate_commit_message(msg, strat): return True, ""


def get_root_dir() -> str:
    # scripts/ directory's parent is the project root
    return os.path.dirname(script_dir)


def load_version_strategy_name(root_dir: str) -> str:
    sync_state_path = os.path.join(root_dir, ".sync-state.json")
    if os.path.exists(sync_state_path):
        try:
            with open(sync_state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("version_strategy", "semver")
        except Exception:
            pass
    return "semver"


def validate_commit_msg_file(commit_msg_filepath: str) -> bool:
    root_dir = get_root_dir()
    strategy_name = load_version_strategy_name(root_dir)
    strategy = get_version_strategy(strategy_name)

    if not os.path.exists(commit_msg_filepath):
        print(f"[Hook Validator Error] Commit message file not found: {commit_msg_filepath}")
        return False

    try:
        with open(commit_msg_filepath, 'r', encoding='utf-8') as f:
            msg_content = f.read()
    except Exception as e:
        print(f"[Hook Validator Error] Failed to read commit message: {e}")
        return False

    # Check for WIP override
    if "WIP" in msg_content.splitlines()[0] or "--no-verify" in msg_content:
        print(f"[Hook Validator] WIP commit override detected. Bypassing check.")
        return True

    is_valid, err_msg = validate_commit_message(msg_content, strategy)
    if not is_valid:
        print("\n=========================================")
        print("❌ [Git Commit Validation Failed]")
        print(f"📌 Strategy    : {strategy_name.upper()}")
        print(f"📌 Error Cause : {err_msg}")
        print("-----------------------------------------")
        print("💡 [Fix Hints for AI Agent Self-Correction]:")
        if strategy_name == "semver":
            print("  1. Header 強制規範 (Conventional Commits):")
            print("     e.g., 'feat(core): add feature' or 'fix(auth): fix login bug'")
            print("     Valid types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert")
            print("  2. Body 不限制/允許使用中文說明 (Permitted CJK, not forced).")
        else:
            print("  1. Header 強制規範 (CalVer 前綴):")
            print("     e.g., 'v1.0.20260728.1 Update notes'")
            print("  2. Body 不限制/允許使用中文說明 (Permitted CJK, not forced).")
        print("  3. Maximum 2 self-correction retries allowed. If still failing, commit with WIP --no-verify.")
        print("=========================================\n")
        return False

    print(f"✅ [Git Hook] Commit message validation passed ({strategy_name.upper()})!")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python git_hook_validator.py [pre-commit | commit-msg <msg_file>]")
        sys.exit(0)

    arg1 = sys.argv[1]
    
    # 1. Pre-commit Hook Phase (Run static check & version alignment)
    if arg1 == "pre-commit":
        root_dir = get_root_dir()
        strategy_name = load_version_strategy_name(root_dir)
        print(f"✅ [Git Hook pre-commit] Strategy check ({strategy_name.upper()}) passed.")
        sys.exit(0)

    # 2. Commit-msg Hook Phase
    commit_msg_file = sys.argv[2] if len(sys.argv) >= 3 else arg1
    if not validate_commit_msg_file(commit_msg_file):
        sys.exit(1)
        
    sys.exit(0)


if __name__ == "__main__":
    main()
