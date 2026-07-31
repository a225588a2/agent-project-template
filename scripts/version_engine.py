#!/usr/bin/env python3
"""
Core Dual Versioning Strategy Engine (SemVer & CalVer)
"""
import os
import sys
import re
import json
from datetime import datetime
from typing import Tuple, List, Dict, Optional

class CalVerStrategy:
    @staticmethod
    def bump(current_version: str, bump_type: str = "patch") -> str:
        # Expected format: YYYY.MM.PATCH or YYYY.MM.PATCH-suffix
        now = datetime.now()
        year_month = f"{now.year}.{now.month:02d}"
        
        match = re.match(r"^(\d{4}\.\d{2})\.(\d+)(?:-(.+))?$", current_version)
        if match:
            old_ym, patch_str, suffix = match.groups()
            patch = int(patch_str)
            if old_ym == year_month:
                new_patch = patch + 1
            else:
                new_patch = 0
            res = f"{year_month}.{new_patch}"
            if suffix:
                res += f"-{suffix}"
            return res
        return f"{year_month}.0-dev"

class SemVerStrategy:
    @staticmethod
    def bump(current_version: str, bump_type: str = "patch") -> str:
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$", current_version)
        if match:
            major, minor, patch, suffix = match.groups()
            ma, mi, pa = int(major), int(minor), int(patch)
            if bump_type == "major":
                ma += 1
                mi, pa = 0, 0
            elif bump_type == "minor":
                mi += 1
                pa = 0
            else:
                pa += 1
            res = f"{ma}.{mi}.{pa}"
            if suffix:
                res += f"-{suffix}"
            return res
        return "1.0.0-dev"

def update_repo_versions(repo_path: str, new_version: str):
    """
    Perform a single os.walk pass to update version strings across sync files.
    """
    target_files = {".sync-state.json", "package.json", "plugin.json"}
    for root, dirs, files in os.walk(repo_path):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            if f in target_files:
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, "r", encoding="utf-8") as file:
                        c = file.read()
                    c_updated = re.sub(r'"version"\s*:\s*"[^"]+"', f'"version": "{new_version}"', c)
                    with open(fpath, "w", encoding="utf-8", newline="\n") as file:
                        file.write(c_updated)
                    print(f"[VERSION Engine] Updated {fpath} -> {new_version}")
                except Exception as e:
                    print(f"[ERROR] Updating {fpath}: {e}")

def get_strategy(repo_root: str):
    """Read .sync-state.json and return the appropriate version strategy."""
    import json
    state_file = os.path.join(repo_root, ".sync-state.json")
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
        if state.get("version_strategy") == "calver":
            return CalVerStrategy()
    return SemVerStrategy()

if __name__ == "__main__":
    print("[VERSION Engine] Engine initialized.")
