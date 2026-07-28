#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_project.py - Progress, DoD & Version Sync Automation for AI Project Template.
Integrates version_engine.py for Dual Versioning (SemVer 2.0 / CalVer),
Strict Parsing, Cold/Hot Memory sync, and Type A Markdown Static Quality Checks.
"""

import os
import sys
import re
import json
import argparse
import traceback
from datetime import datetime

# Add scripts dir to sys.path to import version_engine
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    from version_engine import get_version_strategy, VersionStrategy
except ImportError:
    # Minimal fallback definition if version_engine is missing
    class MinimalStrategy:
        strategy_name = "semver"
        def bump_version(self, v, b="patch"): return "v1.0.1"
        def validate_version(self, v): return True
        def format_commit_header(self, v, s, t="feat"): return f"feat: {s}"
    def get_version_strategy(s): return MinimalStrategy()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Project Progress & Version Synchronization Tool (sync_project.py)"
    )
    parser.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        default="patch",
        help="Version bump increment type for SemVer (default: patch)"
    )
    parser.add_argument(
        "--summary",
        default="",
        help="Optional commit summary text"
    )
    parser.add_argument(
        "--skip-static-check",
        action="store_true",
        help="Skip Type A Markdown static quality checks (not recommended)"
    )
    return parser.parse_args()


def load_version_strategy(root_dir: str) -> Tuple[VersionStrategy, str]:
    """Load version strategy from .sync-state.json or project-meta.json."""
    sync_state_path = os.path.join(root_dir, ".sync-state.json")
    strategy_name = "semver"
    current_version = "v1.0.0"

    if os.path.exists(sync_state_path):
        try:
            with open(sync_state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                strategy_name = data.get("version_strategy", "semver")
                current_version = data.get("version", "v1.0.0")
        except Exception:
            pass
    else:
        meta_path = os.path.join(root_dir, "project-meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    strategy_name = data.get("version_strategy", "semver")
            except Exception:
                pass

    return get_version_strategy(strategy_name), current_version


def run_type_a_static_checks(root_dir: str):
    """
    Type A DoD: Markdown Static Quality Checks.
    Validates file:/// links, filename case conventions, and embedded JSON syntax.
    """
    print("\n--- Running Type A Markdown Static Quality Checks ---")
    errors = []
    
    # 1. Filename Case Convention Check
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore .git, .obsidian, .venv, etc.
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        rel_dir = os.path.relpath(dirpath, root_dir)
        
        for f in filenames:
            if f.startswith("."):
                continue
            
            rel_path = os.path.join(rel_dir, f) if rel_dir != "." else f
            
            # Rule: Core plan files must be UPPER-CASE
            if rel_dir == "plan" and f.endswith(".md"):
                base = f[:-3]
                if base not in ["AGENT", "TARGET", "PROCESS", "MEMORY", "GIT-GUIDE", "FEEDBACK"]:
                    if not base.isupper() and "-" in base:
                        errors.append(f"[Filename Error] File in plan/ '{f}' should be UPPER-CASE (e.g. AGENT.md)")
            
            # Rule: Skills markdown files should be SKILL.md, README.md, or use kebab-case
            if rel_dir.startswith("skills") and f.endswith(".md"):
                if f not in ["SKILL.md", "README.md"]:
                    base = f[:-3]
                    if base != base.lower() or "_" in base:
                        errors.append(f"[Filename Error] Skill file '{rel_path}' should be SKILL.md, README.md, or use kebab-case.")

            # Rule: Python files should use snake_case
            if f.endswith(".py") and "-" in f:
                errors.append(f"[Filename Error] Python script '{f}' contains hyphen '-'. Use snake_case with '_' to prevent import errors.")

    # 2. Markdown file:/// Link & Obsidian Wiki Link [[FileName]] Verification
    file_link_pattern = re.compile(r"\[([^\]]+)\]\((file:///[^\)]+)\)")
    wiki_link_pattern = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]")
    
    # Pre-build set of all markdown filenames for quick wiki-link matching
    all_md_files = set()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".md"):
                all_md_files.add(fn)
                all_md_files.add(fn[:-3]) # Also store base name without .md
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if f.endswith(".md"):
                full_path = os.path.join(dirpath, f)
                try:
                    with open(full_path, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                        
                    # Check file:/// links for existence and enforce no internal file:/// rule
                    for match in file_link_pattern.finditer(content):
                        link_text, raw_url = match.groups()
                        clean_path = raw_url.replace("file:///", "").split("#")[0]
                        if len(clean_path) > 1 and clean_path[1] == ":":
                            local_abs_path = os.path.normpath(clean_path)
                        else:
                            local_abs_path = os.path.normpath("/" + clean_path)
                            
                        # Check existence
                        if not os.path.exists(local_abs_path):
                            errors.append(f"[Link Rot Error] Broken file:/// link in '{f}': {raw_url} (File not found)")
                        else:
                            # Rule: Project-internal links MUST NOT use file:///. Must use [[WikiLink]] instead.
                            try:
                                common_p = os.path.commonpath([os.path.abspath(root_dir), os.path.abspath(local_abs_path)])
                                if common_p == os.path.abspath(root_dir):
                                    # Link points inside the project directory!
                                    rel_target = os.path.relpath(local_abs_path, root_dir)
                                    target_base = os.path.basename(local_abs_path)
                                    if target_base.endswith(".md"):
                                        target_base = target_base[:-3]
                                    errors.append(
                                        f"[Forbidden Link Error] In '{f}': Avoid using 'file:///' for project-internal links! "
                                        f"Use Obsidian Wiki Link [[{target_base}]] instead of '{raw_url}'."
                                    )
                            except ValueError:
                                # Different drive letter, external link is permitted as last resort
                                pass
                            
                    # Check Obsidian Wiki Links [[TargetFile]]
                    ignored_wiki_placeholders = {"FileName", "Note Title", "wikilinks", "MISSION.md", "TargetFile", "Obsidian Wiki Link"}
                    
                    clean_content_for_links = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
                    clean_content_for_links = re.sub(r"`[^`]+`", "", clean_content_for_links)
                    
                    for match in wiki_link_pattern.finditer(clean_content_for_links):
                        raw_target = match.group(1).strip()
                        if not raw_target or raw_target in ignored_wiki_placeholders:
                            continue
                        
                        # 1. Check if raw_target is a direct relative path (file or directory) in root_dir
                        clean_rel_target = raw_target.rstrip("/")
                        abs_target = os.path.normpath(os.path.join(root_dir, clean_rel_target))
                        abs_target_md = abs_target if abs_target.endswith(".md") else abs_target + ".md"
                        
                        if os.path.exists(abs_target) or os.path.exists(abs_target_md):
                            continue
                            
                        # 2. Check if base name matches any existing markdown file
                        target_base = os.path.basename(clean_rel_target)
                        if target_base.endswith(".md"):
                            target_base = target_base[:-3]
                            
                        if target_base in all_md_files or (target_base + ".md") in all_md_files:
                            continue
                            
                        errors.append(f"[Wiki Link Error] Broken Obsidian Wiki Link in '{f}': [[{raw_target}]] (Target file or directory not found)")
                            
                    # Check embedded ```json code blocks
                    json_blocks = re.findall(r"```json\s*\n(.*?)\n```", content, re.DOTALL)
                    for idx, j_str in enumerate(json_blocks):
                        try:
                            json.loads(j_str)
                        except json.JSONDecodeError as je:
                            errors.append(f"[Embedded Syntax Error] Invalid JSON block #{idx+1} in '{f}': {je}")

                except Exception as ex:
                    errors.append(f"[Read Error] Failed to inspect '{f}': {ex}")

    if errors:
        print(f"❌ Type A Static Check Failed with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        print("\n[Strict Parsing] Please fix the static quality issues before synchronizing.")
        sys.exit(1)
        
    print("✅ Type A Markdown Static Quality Checks Passed cleanly!")


def sync_project_status(bump_type: str = "patch", summary_arg: str = "", skip_static: bool = False):
    root_dir = os.path.dirname(script_dir)
    
    # 1. Run Type A static quality checks
    if not skip_static:
        run_type_a_static_checks(root_dir)
        
    strategy, current_version = load_version_strategy(root_dir)
    print(f"\n--- Project Sync Strategy: {strategy.strategy_name.upper()} (Current: {current_version}) ---")

    # 2. Parse cold-history.log for latest commit and todo_ref
    cold_log_path = os.path.join(root_dir, "plan", "cold-history.log")
    if not os.path.exists(cold_log_path):
        print(f"[Error] Log file not found: {cold_log_path}")
        sys.exit(1)

    try:
        with open(cold_log_path, 'r', encoding='utf-8') as f:
            log_content = f.read().strip()
    except Exception as e:
        print(f"[Error] Failed to read plan/cold-history.log: {e}")
        sys.exit(1)

    if not log_content:
        print("[Warning] plan/cold-history.log is empty.")
        log_entries = []
    else:
        # Split log entries by date brackets or header entries
        log_entries = [e.strip() for e in re.split(r'\n(?=\[\d{4}/\d{2}/\d{2})', log_content) if e.strip()]

    latest_entry = log_entries[-1] if log_entries else ""
    
    # Extract todo_ref and commit summary
    todo_ref_match = re.search(r"-\s*todo_ref:\s*(.+)", latest_entry)
    todo_ref = todo_ref_match.group(1).strip() if todo_ref_match else None
    if todo_ref == "null":
        todo_ref = None

    commit_summary_match = re.search(r"-\s*commit:\s*(.+)", latest_entry)
    log_commit_summary = commit_summary_match.group(1).strip() if commit_summary_match else summary_arg

    # 3. Bump Version
    new_version = strategy.bump_version(current_version, bump_type)
    print(f"[Version Bump] {current_version} -> {new_version} ({strategy.strategy_name})")

    # 4. Update plan/PROCESS.md ToDo if todo_ref is present
    process_md_path = os.path.join(root_dir, "plan", "PROCESS.md")
    if os.path.exists(process_md_path):
        try:
            with open(process_md_path, 'r', encoding='utf-8') as f:
                proc_content = f.read()

            # Update current status version line
            proc_content = re.sub(
                r"(-\s*\*\*目前版本\*\*：\s*)(v[^\s\n]+)",
                f"\\g<1>{new_version}",
                proc_content
            )

            # Check off ToDo item if matched
            if todo_ref:
                # Replace - [ ] [todo_ref] with - [x] [todo_ref]
                escaped_ref = re.escape(todo_ref)
                pattern = re.compile(rf"(-\s*\[\s*\]\s*(`?\[?{escaped_ref}\]?`?))")
                if pattern.search(proc_content):
                    proc_content = pattern.sub(f"- [x] \\2", proc_content)
                    print(f"[PROCESS.md] Checked off ToDo: '{todo_ref}' -> [x]")
                else:
                    print(f"[Info] ToDo ref '{todo_ref}' not found in unchecked state in PROCESS.md.")

            with open(process_md_path, 'w', encoding='utf-8') as f:
                f.write(proc_content)
            print(f"[Info] Updated {process_md_path}")
        except Exception as e:
            print(f"[Warning] Failed to update PROCESS.md: {e}")

    # 5. Update plan/MEMORY.md Hot Memory Summary
    memory_md_path = os.path.join(root_dir, "plan", "MEMORY.md")
    if os.path.exists(memory_md_path):
        try:
            with open(memory_md_path, 'r', encoding='utf-8') as f:
                mem_content = f.read()

            # Append new change index entry right under Recent Change Indexes section
            new_index_entry = f"\n### {new_version} {log_commit_summary}\n- **變更項目**：\n  * {log_commit_summary} (todo_ref: {todo_ref or 'null'})\n"
            
            section_header = "## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)"
            if section_header in mem_content:
                parts = mem_content.split(section_header, 1)
                mem_content = parts[0] + section_header + "\n" + new_index_entry + parts[1]
                with open(memory_md_path, 'w', encoding='utf-8') as f:
                    f.write(mem_content)
                print(f"[MEMORY.md] Updated Hot Memory index for {new_version}")
        except Exception as e:
            print(f"[Warning] Failed to update MEMORY.md: {e}")

    # 6. Update .sync-state.json
    sync_state_path = os.path.join(root_dir, ".sync-state.json")
    sync_state = {
        "version": new_version,
        "version_strategy": strategy.strategy_name,
        "last_updated": datetime.now().isoformat(),
        "last_todo_ref": todo_ref,
        "last_commit_summary": log_commit_summary
    }
    with open(sync_state_path, 'w', encoding='utf-8') as f:
        json.dump(sync_state, f, indent=2, ensure_ascii=False)
    print(f"[State] Updated .sync-state.json to version {new_version}")

    # 7. Print recommended git commit command
    commit_header = strategy.format_commit_header(new_version, log_commit_summary or "update project status")
    print("\n=========================================")
    print("✨ Sync Completed Successfully!")
    print(f"📌 Next Git Commit Header Recommendation:")
    print(f"   git commit -m \"{commit_header}\"")
    print("=========================================\n")


def main():
    args = parse_args()
    try:
        sync_project_status(bump_type=args.bump, summary_arg=args.summary, skip_static=args.skip_static_check)
    except Exception as e:
        print(f"\n❌ [Sync Error] Synchronization failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
