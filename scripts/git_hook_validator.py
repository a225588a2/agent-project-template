#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_path(rel_path):
    return os.path.join(ROOT_DIR, rel_path)

def has_no_commits():
    try:
        # If git rev-parse HEAD fails, it means we have no commits yet.
        res = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ROOT_DIR)
        return res.returncode != 0
    except FileNotFoundError:
        print("[Git Hook Warning] Git executable not found in PATH. Enforcing local validation checks...", file=sys.stderr)
        return False
    except Exception:
        return False

def get_process_version():
    path = get_path("plan/PROCESS.md")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Match the version line in PROCESS.md (supporting both full-width and half-width colons)
        match = re.search(r'^\-\s*\*\*目前版本\*\*\s*[:：]\s*v?(\d+\.\d+\.\d{8}\.\d+)', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"[Git Hook Error] Failed to read version from plan/PROCESS.md: {e}", file=sys.stderr)
    return None

def get_cold_history_version():
    path = get_path("logs/cold-history.log")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[Git Hook Error] Failed to read logs/cold-history.log: {e}", file=sys.stderr)
        return None
    
    # Header pattern: [YYYY/MM/DD vX.Y.YYYYMMDD.Z] English Summary
    header_pattern = re.compile(r'^\[\d{4}/\d{2}/\d{2}\s+v\d+\.\d+\.\d{8}\.\d+\].*$')
    
    # Check for malformed logs/cold-history.log headers berjalan backwards
    last_bracket_line = None
    for line in reversed(lines):
        if line.startswith("["):
            last_bracket_line = line.strip()
            break
            
    if last_bracket_line and not header_pattern.match(last_bracket_line):
        print("[Git Hook Error] Malformed log entry header detected in logs/cold-history.log!", file=sys.stderr)
        print(f"  Got: '{last_bracket_line}'", file=sys.stderr)
        print("  Expected format: [YYYY/MM/DD vX.Y.YYYYMMDD.Z] English Summary", file=sys.stderr)
        return None

    header_indices = [idx for idx, line in enumerate(lines) if header_pattern.match(line.strip())]
    if not header_indices:
        return None
        
    last_header = lines[header_indices[-1]].strip()
    title_match = re.match(r'^\[\d{4}/\d{2}/\d{2}\s+v(\d+\.\d+\.\d{8}\.\d+)\]\s+(.+)$', last_header)
    if title_match:
        return title_match.group(1).strip()
    return None

def get_sync_state_version():
    path = get_path(".sync-state.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("version", "").strip().lstrip("vV")
    except Exception as e:
        print(f"[Git Hook Error] Failed to read .sync-state.json: {e}", file=sys.stderr)
        return None

def normalize_version(ver):
    if not ver:
        return ""
    return ver.strip().lower().lstrip("v")

def check_sync():
    if has_no_commits():
        print("[Git Hook Check] Initial commit detected. Bypassing project status sync check.")
        return True

    process_ver = normalize_version(get_process_version())
    cold_history_ver = normalize_version(get_cold_history_version())
    state_ver = normalize_version(get_sync_state_version())
    
    if not process_ver:
        print("[Git Hook Error] Could not read version from plan/PROCESS.md", file=sys.stderr)
        return False
    if not cold_history_ver:
        print("[Git Hook Error] Could not read version from logs/cold-history.log", file=sys.stderr)
        return False
    if not state_ver:
        print("[Git Hook Error] Could not read version from .sync-state.json. Please run 'python scripts/sync_project.py' first.", file=sys.stderr)
        return False
        
    if process_ver != cold_history_ver or process_ver != state_ver:
        print("[Git Hook Error] Project status files are out of sync!", file=sys.stderr)
        print(f"  plan/PROCESS.md version:       v{process_ver}", file=sys.stderr)
        print(f"  logs/cold-history.log version: v{cold_history_ver}", file=sys.stderr)
        print(f"  .sync-state.json version:      v{state_ver}", file=sys.stderr)
        print("Please run 'python scripts/sync_project.py' to synchronize your project state before committing.", file=sys.stderr)
        return False
        
    return True

def check_commit_msg(msg_file):
    if not os.path.exists(msg_file):
        print(f"[Git Hook Error] Commit message file not found: {msg_file}", file=sys.stderr)
        return False
        
    try:
        with open(msg_file, "r", encoding="utf-8") as f:
            msg_content = f.read()
    except Exception as e:
        print(f"[Git Hook Error] Failed to read commit message file: {e}", file=sys.stderr)
        return False
        
    if not msg_content.strip():
        print("[Git Hook Error] Commit message cannot be empty.", file=sys.stderr)
        return False
        
    # Reject Chinese, Japanese, Korean, CJK Symbols, and Fullwidth forms:
    # \u4e00-\u9fff (CJK Unified Ideographs)
    # \u3040-\u309f (Japanese Hiragana)
    # \u30a0-\u30ff (Japanese Katakana)
    # \uac00-\ud7af (Korean Hangul Syllables)
    # \u3000-\u303f (CJK Symbols and Punctuation)
    # \uff00-\uffef (Halfwidth and Fullwidth Forms)
    cjk_pattern = re.compile(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af\u3000-\u303f\uff00-\uffef]')
    if cjk_pattern.search(msg_content):
        print("[Git Hook Error] CJK (Chinese, Japanese, Korean) characters/punctuation are not allowed in the commit message.", file=sys.stderr)
        print("Please write commit messages strictly in English.", file=sys.stderr)
        return False
        
    lines = msg_content.splitlines()
    if not lines:
        print("[Git Hook Error] Commit message contains no lines.", file=sys.stderr)
        return False
        
    title = lines[0].strip()
    
    # Check title format: must be vX.Y.YYYYMMDD.Z English Summary
    title_match = re.match(r'^v(\d+\.\d+\.\d{8}\.\d+)\s+(.+)$', title)
    if not title_match:
        print("[Git Hook Error] Commit title format is invalid.", file=sys.stderr)
        print("Expected format: vX.Y.YYYYMMDD.Z English Summary", file=sys.stderr)
        print("Example: v1.0.20260701.7 Update directory definitions", file=sys.stderr)
        print(f"Got: '{title}'", file=sys.stderr)
        return False
        
    commit_ver = normalize_version(title_match.group(1))
    
    if has_no_commits():
        print("[Git Hook Check] Initial commit detected. Bypassing version alignment check.")
        return True
        
    # Check if the commit message version matches the project's synced version
    process_ver = normalize_version(get_process_version())
    cold_history_ver = normalize_version(get_cold_history_version())
    state_ver = normalize_version(get_sync_state_version())
    
    # Verify alignment of version strings
    if commit_ver != process_ver or commit_ver != cold_history_ver or commit_ver != state_ver:
        print("[Git Hook Error] Commit version does not align with synchronized project files!", file=sys.stderr)
        print(f"  Commit Title version:          v{commit_ver}", file=sys.stderr)
        print(f"  plan/PROCESS.md version:       v{process_ver}", file=sys.stderr)
        print(f"  logs/cold-history.log version: v{cold_history_ver}", file=sys.stderr)
        print(f"  .sync-state.json version:      v{state_ver}", file=sys.stderr)
        print("Please verify you have run 'python scripts/sync_project.py' and your commit title matches the synced version.", file=sys.stderr)
        return False
        
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python git_hook_validator.py [pre-commit|commit-msg] [args...]", file=sys.stderr)
        sys.exit(1)
        
    mode = sys.argv[1]
    if mode == "pre-commit":
        success = check_sync()
    elif mode == "commit-msg":
        if len(sys.argv) < 3:
            print("Usage: python git_hook_validator.py commit-msg <commit_msg_file>", file=sys.stderr)
            sys.exit(1)
        msg_file = sys.argv[2]
        if not check_sync():
            success = False
        else:
            success = check_commit_msg(msg_file)
    else:
        print(f"Unknown validation mode: {mode}", file=sys.stderr)
        sys.exit(1)
        
    if not success:
        sys.exit(1)
        
    print(f"[Git Hook Check] {mode} validation passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
