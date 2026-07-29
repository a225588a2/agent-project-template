#!/usr/bin/env python3
"""
Council Archive Automation Utility
"""
import os
import sys
import shutil
from utils import resolve_repo_root

def archive_council(temp_dir: str):
    root = resolve_repo_root()
    archive_dir = os.path.join(root, "logs", "archived")
    os.makedirs(archive_dir, exist_ok=True)
    print(f"[ARCHIVE] Archiving council files to {archive_dir}...")
    
    if os.path.exists(temp_dir):
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"[ARCHIVE] Safely removed directory: {temp_dir}")
        else:
            os.remove(temp_dir)

if __name__ == "__main__":
    print("[ARCHIVE] Council archive utility ready.")
