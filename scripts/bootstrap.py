#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        "-m", "--modules",
        default="",
        help="Comma-separated list of optional folders to create (default: none)"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode. Skips TTY check and uses default values/json if arguments are missing."
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

def main():
    args = parse_args()
    target_dir = os.path.abspath(args.target_dir)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_root = os.path.dirname(script_dir)
    
    # 1. Determine if interactive mode is allowed
    is_interactive = not args.non_interactive and sys.stdin.isatty()
    
    # 2. Try loading config file from either command line or target dir
    config_file_path = os.path.join(target_dir, args.config) if args.target_dir != "." else os.path.abspath(args.config)
    config_data = load_config(config_file_path)
    
    # Resolve project name
    proj_name = args.name or config_data.get("name")
    if not proj_name:
        if is_interactive:
            proj_name = input("Enter project name: ").strip()
        if not proj_name:
            proj_name = "NewAIProject"
            print(f"[Info] No project name provided. Defaulting to: {proj_name}")

    # Resolve AI Agent name
    agent_name = args.agent or config_data.get("agent")
    if not agent_name:
        if is_interactive:
            agent_name = input("Enter primary AI Agent name (default: Claude): ").strip()
        if not agent_name:
            agent_name = "Claude"
            print(f"[Info] No Agent name provided. Defaulting to: {agent_name}")

    # Resolve modules list
    modules_str = args.modules
    if not modules_str and "modules" in config_data:
        modules_str = ",".join(config_data.get("modules", []))
    
    modules_list = [m.strip() for m in modules_str.split(",") if m.strip()]
    
    print(f"\n--- Initializing Project Configuration ---")
    print(f"Target Directory : {target_dir}")
    print(f"Project Name     : {proj_name}")
    print(f"Primary Agent    : {agent_name}")
    print(f"Optional Modules : {modules_list if modules_list else 'None'}")
    print(f"-----------------------------------------\n")

    # 3. Create directories and copy template files
    os.makedirs(target_dir, exist_ok=True)
    
    core_dirs = ["plan", "doc", "structure", "logs"]
    for d in core_dirs:
        os.makedirs(os.path.join(target_dir, d), exist_ok=True)
        
    for m in modules_list:
        m_path = os.path.join(target_dir, m)
        os.makedirs(m_path, exist_ok=True)
        # Touch a .gitkeep to keep directory in Git
        with open(os.path.join(m_path, ".gitkeep"), 'w', encoding='utf-8') as f:
            pass

    # Ensure logs/.gitkeep exists
    with open(os.path.join(target_dir, "logs", ".gitkeep"), 'w', encoding='utf-8') as f:
        pass

    # Define files to copy/render
    files_to_copy = [
        ("plan/TARGET.md", "plan/TARGET.md"),
        ("plan/AGENT.md", "plan/AGENT.md"),
        ("plan/PROCESS.md", "plan/PROCESS.md"),
        ("plan/MEMORY.md", "plan/MEMORY.md"),
        ("plan/COUNCIL.md", "plan/COUNCIL.md"),
        ("logs/cold-history.log", "logs/cold-history.log"),
        (".gitignore", ".gitignore"),
        ("README.md", "README.md")
    ]
    
    today_str = datetime.now().strftime("%Y%m%d")
    initial_version = f"v1.0.{today_str}.1"

    # Copy files if target dir is different from template root
    is_in_place = (os.path.abspath(target_dir) == os.path.abspath(template_root))
    if not is_in_place:
        for src_rel, dst_rel in files_to_copy:
            src_abs = os.path.join(template_root, src_rel)
            dst_abs = os.path.join(target_dir, dst_rel)
            if os.path.exists(src_abs):
                # Only copy if destination doesn't exist
                if not os.path.exists(dst_abs):
                    shutil.copy2(src_abs, dst_abs)
                    print(f"[Info] Copied template file: {dst_rel}")
            else:
                # If file doesn't exist (e.g. cold-history.log is being created fresh)
                if not os.path.exists(dst_abs):
                    with open(dst_abs, 'w', encoding='utf-8') as f:
                        if dst_rel == "logs/cold-history.log":
                            f.write("=== COLD HISTORY LOG ===\n")
                    print(f"[Info] Created file: {dst_rel}")
    else:
        print("[Info] Initializing in-place within the template repository. Skipping file copy.")

    # 4. Replace placeholders in target files
    # Define placeholder replacements
    replacements = {
        "[請在此填入專案名稱]": proj_name,
        "[請在此填入主要 Agent 名稱]": agent_name,
        "v20260628.2": initial_version,
        "v20260628.1": initial_version
    }
    
    for _, dst_rel in files_to_copy:
        dst_abs = os.path.join(target_dir, dst_rel)
        if os.path.exists(dst_abs):
            try:
                with open(dst_abs, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                replaced = False
                for placeholder, value in replacements.items():
                    if placeholder in content:
                        content = content.replace(placeholder, value)
                        replaced = True
                
                if replaced:
                    with open(dst_abs, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"[Info] Rendered placeholders in: {dst_rel}")
            except Exception as e:
                print(f"[Warning] Failed to render placeholders in {dst_rel}: {e}")

    # 5. Local Git initialization check (Strictly localized)
    git_dir = os.path.join(target_dir, ".git")
    if not os.path.exists(git_dir):
        print("[Info] No Git repository detected in target directory. Initializing Git...")
        try:
            # Run git init
            subprocess.run(["git", "init"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
            # Run git add
            subprocess.run(["git", "add", "."], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
            # Run git commit
            subprocess.run(
                ["git", "commit", "-m", f"{initial_version} Initialize project template"],
                cwd=target_dir,
                check=True,
                stdout=subprocess.DEVNULL
            )
            print(f"[Success] Initialized Git repository and created zero-commit: {initial_version}")
        except Exception as e:
            print(f"[Warning] Git initialization failed: {e}. Please run git commands manually.")
    else:
        print("[Info] Existing Git repository detected in target directory. Skipping Git initialization.")

    # 6. Save JSON config file
    config_data["name"] = proj_name
    config_data["agent"] = agent_name
    config_data["modules"] = modules_list
    write_config(config_file_path, config_data)
    
    print("\n[Success] Project bootstrapping completed successfully!")
    print(f"Initial Version  : {initial_version}")
    print("You can now start editing files in the plan/ directory.")

if __name__ == "__main__":
    main()
