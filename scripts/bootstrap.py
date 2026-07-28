#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap.py - AI Project Template Initializer
Supports Smart Auto-Detection & Dual Versioning Strategy (SemVer 2.0 vs CalVer),
Mandatory Author Signature check, and clean one-time static template rendering.
"""

import os
import sys
import shutil
import argparse
import json
import subprocess
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(
        description="AI Project Template Initializer (bootstrap.py)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-d", "--target-dir",
        default=".",
        help="Target directory to initialize the project (default: current directory)"
    )
    parser.add_argument(
        "-n", "--name",
        help="Project name"
    )
    parser.add_argument(
        "-a", "--agent",
        help="Primary AI Agent name (e.g. Claude, Cursor, Antigravity)"
    )
    parser.add_argument(
        "-v", "--version-strategy",
        choices=["semver", "calver"],
        help="Version strategy: 'semver' (SemVer 2.0 for code/software) or 'calver' (Date-based for notes/logs)"
    )
    parser.add_argument(
        "-m", "--modules",
        default="",
        help="Comma-separated list of optional folders to create (default: none)"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode. Skips TTY check and uses smart auto-detection/default values."
    )
    parser.add_argument(
        "-c", "--config",
        default="project-meta.json",
        help="Path to project metadata JSON config file (default: project-meta.json)"
    )
    return parser.parse_args()

def load_config(config_path):
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Failed to parse config file {config_path}: {e}")
    return {}

def write_config(config_path, data):
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[Info] Saved metadata config to {config_path}")
    except Exception as e:
        print(f"[Warning] Failed to save config file: {e}")

def check_git_author_signature(target_dir):
    """Check and guide user for Mandatory Author Signature (user.name & user.email)."""
    print("\n--- Checking Git Author Signature ---")
    try:
        name_res = subprocess.run(["git", "config", "user.name"], cwd=target_dir, capture_output=True, text=True)
        email_res = subprocess.run(["git", "config", "user.email"], cwd=target_dir, capture_output=True, text=True)
        
        user_name = name_res.stdout.strip()
        user_email = email_res.stdout.strip()
        
        if user_name and user_email:
            print(f"[Git Author] Verified: {user_name} <{user_email}>")
        else:
            print("[Warning] Git Author Signature (user.name / user.email) is missing in Git config.")
            print("[Info] Setting local placeholder Author Signature for initial commits...")
            subprocess.run(["git", "config", "user.name", "AI Developer"], cwd=target_dir, check=False)
            subprocess.run(["git", "config", "user.email", "developer@ai-project.template"], cwd=target_dir, check=False)
            print("[Info] Local Author Signature set: AI Developer <developer@ai-project.template>")
            print("[Tip] You can update it anytime using: git config user.name 'Your Name' && git config user.email 'your@email.com'")
    except Exception as e:
        print(f"[Warning] Failed to check Git config: {e}")

def detect_smart_version_strategy(target_dir):
    """Heuristic auto-detection for version strategy in non-interactive mode."""
    # Check for code project indicators -> semver
    code_indicators = ["package.json", "pyproject.toml", "Cargo.toml", "go.mod", "setup.py", "pom.xml"]
    for ind in code_indicators:
        if os.path.exists(os.path.join(target_dir, ind)):
            print(f"[Smart Detection] Found '{ind}' -> Auto-selecting 'semver' strategy.")
            return "semver"
            
    # Check for document/note indicators -> calver
    doc_indicators = ["obsidian.json", ".obsidian", "notes", "daily_logs"]
    for ind in doc_indicators:
        if os.path.exists(os.path.join(target_dir, ind)):
            print(f"[Smart Detection] Found '{ind}' -> Auto-selecting 'calver' strategy.")
            return "calver"
            
    # Default to semver
    print("[Smart Detection] No specific project indicators found. Defaulting to 'semver' strategy.")
    return "semver"

def main():
    args = parse_args()
    target_dir = os.path.abspath(args.target_dir)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_root = os.path.dirname(script_dir)
    
    # 1. Determine if interactive mode is allowed
    is_interactive = not args.non_interactive and sys.stdin.isatty()
    
    # 2. Try loading config file
    config_file_path = os.path.join(target_dir, args.config) if args.target_dir != "." else os.path.abspath(args.config)
    config_data = load_config(config_file_path)
    
    # Resolve project name
    proj_name = args.name or config_data.get("name")
    if not proj_name:
        if is_interactive:
            proj_name = input("Enter project name: ").strip()
        if not proj_name:
            proj_name = "NewAIProject"
            print(f"[Info] Defaulting project name to: {proj_name}")

    # Resolve AI Agent name
    agent_name = args.agent or config_data.get("agent")
    if not agent_name:
        if is_interactive:
            agent_name = input("Enter primary AI Agent name (default: Antigravity): ").strip()
        if not agent_name:
            agent_name = "Antigravity"

    # Resolve Version Strategy (Dual Versioning Strategy)
    version_strategy = args.version_strategy or config_data.get("version_strategy")
    if not version_strategy:
        if is_interactive:
            print("\nSelect Versioning Strategy for this Project:")
            print("  1) [SemVer 2.0]  Recommended for software code, libraries, research frameworks (vMAJOR.MINOR.PATCH, Conventional Commits, Gitflow)")
            print("  2) [CalVer]      Recommended for personal notes, daily logs, data collection (vYYYY.MM.DD / v1.0.YYYYMMDD.Z, Date-prefix)")
            choice = input("Enter choice (1 or 2, default: 1): ").strip()
            version_strategy = "calver" if choice == "2" else "semver"
        else:
            version_strategy = detect_smart_version_strategy(target_dir)

    # Resolve modules list
    modules_str = args.modules
    if not modules_str and "modules" in config_data:
        modules_str = ",".join(config_data.get("modules", []))
    modules_list = [m.strip() for m in modules_str.split(",") if m.strip()]
    
    print(f"\n=========================================")
    print(f"--- Initializing Project Configuration ---")
    print(f"Target Directory : {target_dir}")
    print(f"Project Name     : {proj_name}")
    print(f"Primary Agent    : {agent_name}")
    print(f"Version Strategy : {version_strategy.upper()}")
    print(f"Optional Modules : {modules_list if modules_list else 'None'}")
    print(f"=========================================\n")

    # 3. Create directories
    os.makedirs(target_dir, exist_ok=True)
    core_dirs = ["plan", "doc", "structure", "scripts", "skills"]
    for d in core_dirs:
        os.makedirs(os.path.join(target_dir, d), exist_ok=True)
        
    for m in modules_list:
        m_path = os.path.join(target_dir, m)
        os.makedirs(m_path, exist_ok=True)
        with open(os.path.join(m_path, ".gitkeep"), 'w', encoding='utf-8') as f:
            pass

    # Determine initial version string based on strategy
    today_str = datetime.now().strftime("%Y%m%d")
    if version_strategy == "semver":
        initial_version = "v1.0.0"
    else:
        initial_version = f"v1.0.{today_str}.1"

    # Define files to copy/render
    files_to_copy = [
        ("plan/TARGET.md", "plan/TARGET.md"),
        ("plan/AGENT.md", "plan/AGENT.md"),
        ("plan/PROCESS.md", "plan/PROCESS.md"),
        ("plan/MEMORY.md", "plan/MEMORY.md"),
        ("plan/GIT-GUIDE.md", "plan/GIT-GUIDE.md"),
        ("plan/cold-history.log", "plan/cold-history.log"),
        (".gitignore", ".gitignore"),
        ("README.md", "README.md"),
        ("scripts/version_engine.py", "scripts/version_engine.py"),
        ("scripts/sync_project.py", "scripts/sync_project.py"),
        ("scripts/git_hook_validator.py", "scripts/git_hook_validator.py"),
        ("scripts/install_hooks.py", "scripts/install_hooks.py")
    ]
    
    # Automatically add all skill files to copy list
    skills_dir_abs = os.path.join(template_root, "skills")
    if os.path.exists(skills_dir_abs):
        for r, _, fs in os.walk(skills_dir_abs):
            for file in fs:
                abs_f = os.path.join(r, file)
                rel_f = os.path.relpath(abs_f, template_root).replace("\\", "/")
                files_to_copy.append((rel_f, rel_f))

    is_in_place = (os.path.abspath(target_dir) == os.path.abspath(template_root))
    if not is_in_place:
        for src_rel, dst_rel in files_to_copy:
            src_abs = os.path.join(template_root, src_rel)
            dst_abs = os.path.join(target_dir, dst_rel)
            if os.path.exists(src_abs):
                os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
                shutil.copy2(src_abs, dst_abs)
                print(f"[Copy] {src_rel} -> {dst_rel}")

    # 4. Save metadata and sync state JSONs
    meta_data = {
        "name": proj_name,
        "agent": agent_name,
        "version_strategy": version_strategy,
        "created_at": datetime.now().isoformat(),
        "modules": modules_list
    }
    write_config(os.path.join(target_dir, "project-meta.json"), meta_data)
    
    sync_state = {
        "version": initial_version,
        "version_strategy": version_strategy,
        "last_updated": datetime.now().isoformat(),
        "project_name": proj_name
    }
    with open(os.path.join(target_dir, ".sync-state.json"), 'w', encoding='utf-8') as f:
        json.dump(sync_state, f, indent=2, ensure_ascii=False)
    print(f"[Info] Saved .sync-state.json (Initial Version: {initial_version})")

    # 5. Initialize Git repository if needed
    git_dir = os.path.join(target_dir, ".git")
    if not os.path.exists(git_dir):
        print("\n--- Initializing Git Repository ---")
        try:
            subprocess.run(["git", "init"], cwd=target_dir, check=True)
            print("[Git] Initialized empty Git repository.")
        except Exception as e:
            print(f"[Warning] Failed to run 'git init': {e}")
            
    # Check and set Git Author Signature
    check_git_author_signature(target_dir)

    # 6. Install Git Hooks
    print("\n--- Installing Git Hook Validation ---")
    try:
        install_script = os.path.join(target_dir, "scripts", "install_hooks.py")
        if os.path.exists(install_script):
            subprocess.run([sys.executable, install_script], cwd=target_dir, check=False)
    except Exception as e:
        print(f"[Warning] Failed to install git hooks: {e}")

    print(f"\n✨ Project '{proj_name}' initialized successfully!")
    print(f"📌 Version Strategy: {version_strategy.upper()} ({initial_version})")
    print("🚀 You are all set. Have fun building!\n")

if __name__ == "__main__":
    main()
