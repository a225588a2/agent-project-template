#!/usr/bin/env python3
"""
New Project Initializer Utility
"""
import os
import sys
import argparse
import shutil
from typing import Optional, List
from utils import resolve_repo_root

def bootstrap(output_dir: str, install_hooks: bool = False):
    repo_root = resolve_repo_root()
    target_dir = os.path.abspath(output_dir)
    print(f"[BOOTSTRAP] Initializing new project template from {repo_root} -> {target_dir}")
    
    if os.path.exists(target_dir) and os.listdir(target_dir):
        print(f"[WARNING] Target directory {target_dir} is not empty.")
    
    os.makedirs(target_dir, exist_ok=True)
    print(f"[BOOTSTRAP] Created target directory: {target_dir}")
    
    if install_hooks:
        hooks_installer = os.path.join(repo_root, "scripts", "install_hooks.py")
        if os.path.exists(hooks_installer):
            print(f"[BOOTSTRAP] Executing git hooks installer...")
            os.system(f"{sys.executable} "{hooks_installer}"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap a new AI project template.")
    parser.add_argument("--output", "-o", "--target-dir", dest="output", required=True, help="Target output directory")
    parser.add_argument("--install-hooks", action="store_true", help="Automatically install Git hooks")
    args = parser.parse_args()
    bootstrap(args.output, args.install_hooks)
