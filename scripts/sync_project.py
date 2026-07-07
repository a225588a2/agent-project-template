#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import json
import subprocess
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(
        description="AI Project Status Sync Tool (sync_project.py)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="Workspace directory (default: current directory)"
    )
    parser.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        help="Increment version type (default: daily progress patch calculation)"
    )
    parser.add_argument(
        "-l", "--log",
        default="logs/cold-history.log",
        help="Path to cold history log file relative to workspace"
    )
    parser.add_argument(
        "-p", "--process",
        default="plan/PROCESS.md",
        help="Path to PROCESS.md file relative to workspace"
    )
    parser.add_argument(
        "-m", "--memory",
        default="plan/MEMORY.md",
        help="Path to MEMORY.md file relative to workspace"
    )
    parser.add_argument(
        "-s", "--state",
        default=".sync-state.json",
        help="Path to state JSON file relative to workspace"
    )
    return parser.parse_args()

def clean_text(text):
    """Normalize text for matching (strip, lowercase, alphanumeric only)."""
    return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '', text).lower()

def parse_last_log_entry(log_path):
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Log file not found: {log_path}")
        
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    header_indices = []
    # Header pattern: [YYYY/MM/DD vX.Y.YYYYMMDD.Z] English Summary
    header_pattern = re.compile(r'^\[\d{4}/\d{2}/\d{2}\s+v\d+\.\d+\.\d{8}\.\d+\].*$')
    
    # Check for silent typos/malformed headers in cold-history.log
    last_bracket_line = None
    for line in reversed(lines):
        if line.startswith("["):
            last_bracket_line = line.strip()
            break
            
    if last_bracket_line and not header_pattern.match(last_bracket_line):
        raise ValueError(
            f"Latest log entry header in logs/cold-history.log is malformed.\n"
            f"Expected: [YYYY/MM/DD vX.Y.YYYYMMDD.Z] English Summary\n"
            f"Got:      '{last_bracket_line}'"
        )
    
    for idx, line in enumerate(lines):
        if header_pattern.match(line.strip()):
            header_indices.append(idx)
            
    if not header_indices:
        raise ValueError("No valid log entries starting with [YYYY/MM/DD vX.Y.YYYYMMDD.Z] found in cold history log.")
        
    last_header_idx = header_indices[-1]
    entry_lines = lines[last_header_idx:]
    
    # Parse title line
    title_line = entry_lines[0].strip()
    title_match = re.match(r'^\[(\d{4}/\d{2}/\d{2})\s+v((\d+)\.(\d+)\.(\d{8})\.(\d+))\]\s+(.+)$', title_line)
    if not title_match:
        raise ValueError(
            f"Latest log entry header format invalid.\n"
            f"Expected: [YYYY/MM/DD vX.Y.YYYYMMDD.Z] Summary\n"
            f"Got:      '{title_line}'"
        )
        
    log_date, log_version, log_major, log_minor, log_version_date, log_version_index, log_title = title_match.groups()
    
    todo_ref = None
    commit_msg = None
    summary_bullets = []
    in_summary = False
    
    for line in entry_lines[1:]:
        stripped = line.strip()
        if not stripped:
            continue
            
        # Stop if we hit another header (safety check)
        if header_pattern.match(stripped):
            break
            
        if stripped.startswith("- todo_ref:"):
            todo_ref = stripped.split("- todo_ref:")[1].strip()
            in_summary = False
        elif stripped.startswith("- commit:"):
            commit_msg = stripped.split("- commit:")[1].strip()
            in_summary = False
        elif stripped.startswith("- summary:"):
            in_summary = True
        elif in_summary:
            if line.startswith(" ") or line.startswith("\t"):
                summary_bullets.append(stripped)
            else:
                in_summary = False
                
    if todo_ref is None:
        raise ValueError("Log entry missing '- todo_ref:' field.")
    if commit_msg is None:
        raise ValueError("Log entry missing '- commit:' field.")
    if not summary_bullets:
        raise ValueError("Log entry summary cannot be empty and must contain indented bullet points.")
        
    return {
        "date": log_date,
        "version": log_version,
        "major": int(log_major),
        "minor": int(log_minor),
        "version_date": log_version_date,
        "version_index": int(log_version_index),
        "title": log_title,
        "todo_ref": todo_ref,
        "commit": commit_msg,
        "summary": summary_bullets
    }

def get_open_todos(process_path):
    todos = []
    if os.path.exists(process_path):
        todo_pattern = re.compile(r'^\s*[\-\*\+]\s+`?\[([\s\/])\]`?\s*(.*)$')
        with open(process_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = todo_pattern.match(line)
                if match:
                    todos.append(match.group(2).strip())
    return todos

def sync_todos(process_path, todo_ref_val):
    if not os.path.exists(process_path):
        raise FileNotFoundError(f"PROCESS.md not found: {process_path}")
        
    with open(process_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    clean_ref = clean_text(todo_ref_val)
    matched_count = 0
    new_lines = []
    
    # Matches markdown list checkboxes with optional backticks and indentations
    todo_pattern = re.compile(r'^(\s*[\-\*\+]\s+`?)\[([\s\/])\](`?\s*)(.*)$')
    
    for line in lines:
        match = todo_pattern.match(line)
        if match:
            prefix, marker_content, suffix, todo_text = match.groups()
            clean_todo = clean_text(todo_text)
            
            # Double-sided substring matching
            if clean_ref in clean_todo or clean_todo in clean_ref:
                line = f"{prefix}[x]{suffix}{todo_text}\n"
                matched_count += 1
        new_lines.append(line)
        
    if matched_count == 0:
        open_todos = get_open_todos(process_path)
        todos_list_str = "\n".join([f"  * {t}" for t in open_todos])
        raise ValueError(
            f"No matching ToDo task found in PROCESS.md for reference: '{todo_ref_val}'\n"
            f"Currently open ToDo tasks in PROCESS.md:\n{todos_list_str if open_todos else '  (None)'}"
        )
        
    with open(process_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"[Info] Checked off '{todo_ref_val}' in PROCESS.md.")

def bump_version(process_path, bump_type):
    if not os.path.exists(process_path):
        raise FileNotFoundError(f"PROCESS.md not found: {process_path}")
        
    with open(process_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find current version line: - **目前版本**：vX.Y.YYYYMMDD.Z
    version_pattern = re.compile(
        r'^(\-\s*\*\*目前版本\*\*\s*：\s*)v?(\d+)\.(\d+)\.(\d{8})\.(\d+)(.*?)$',
        re.MULTILINE
    )
    
    match = version_pattern.search(content)
    if not match:
        raise ValueError("Could not find a valid version line in format '- **目前版本**：vX.Y.YYYYMMDD.Z' in PROCESS.md.")
        
    prefix, major_str, minor_str, date_str, index_str, suffix = match.groups()
    
    major = int(major_str)
    minor = int(minor_str)
    date_part = date_str
    index = int(index_str)
    
    today_str = datetime.now().strftime("%Y%m%d")
    
    # Calculate new version
    if bump_type == "major":
        new_major = major + 1
        new_minor = 0
        new_date = today_str
        new_index = 1
    elif bump_type == "minor":
        new_major = major
        new_minor = minor + 1
        new_date = today_str
        new_index = 1
    else: # patch / default daily index calculation
        new_major = major
        new_minor = minor
        if date_part == today_str:
            new_date = today_str
            new_index = index + 1
        else:
            new_date = today_str
            new_index = 1
            
    old_version = f"v{major}.{minor}.{date_part}.{index}"
    new_version = f"v{new_major}.{new_minor}.{new_date}.{new_index}"
    
    new_line = f"{prefix}{new_version}{suffix}"
    content = version_pattern.sub(new_line, content)
    
    return old_version, new_version, content

def update_memory_md(memory_path, new_version, log_entry):
    if not os.path.exists(memory_path):
        return
        
    with open(memory_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    section_header = "## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)"
    if section_header not in content:
        print("[Warning] Could not find 'Recent Change Indexes' section in MEMORY.md. Skipping MEMORY.md index update.")
        return
        
    parts = content.split(section_header)
    intro_part = parts[0] + section_header + "\n\n"
    entries_part = parts[1].strip()
    
    # Split existing entries by ###
    existing_entries = []
    if entries_part:
        # Split but keep the delimiter ###
        splits = re.split(r'^(###\s+.*)$', entries_part, flags=re.MULTILINE)
        current_header = None
        current_body = []
        
        for part in splits:
            part_strip = part.strip()
            if not part_strip:
                continue
            if part.startswith("###"):
                if current_header:
                    existing_entries.append((current_header, "\n".join(current_body)))
                current_header = part_strip
                current_body = []
            else:
                current_body.append(part)
        if current_header:
            existing_entries.append((current_header, "\n".join(current_body)))

    # Format new entry
    formatted_summary = "\n".join([f"  {b}" for b in log_entry["summary"]])
    new_entry_header = f"### {new_version} {log_entry['title']} ({new_version})"
    new_entry_body = f"- **變更項目**：\n{formatted_summary}"
    
    # Prepend new entry
    all_entries = [(new_entry_header, new_entry_body)] + existing_entries
    # Keep last 5 entries
    all_entries = all_entries[:5]
    
    # Reassemble entries
    formatted_entries = ""
    for header, body in all_entries:
        formatted_entries += f"{header}\n{body.strip()}\n\n"
        
    new_content = intro_part + formatted_entries.strip() + "\n"
    
    with open(memory_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("[Info] Updated MEMORY.md change indexes.")



def save_state(state_path, new_version, last_task, open_todos):
    state_data = {
        "version": new_version,
        "last_sync": datetime.now().isoformat(),
        "last_task": last_task,
        "open_todos": open_todos
    }
    try:
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        print(f"[Info] Exported state to {state_path}")
    except Exception as e:
        print(f"[Warning] Failed to save state file: {e}")

def main():
    args = parse_args()
    os.chdir(args.dir)
    
    log_path = args.log
    process_path = args.process
    memory_path = args.memory
    state_path = args.state
    
    print("--- Executing AI Project Sync Tool ---")
    
    # 1. Parse cold-history log
    try:
        log_entry = parse_last_log_entry(log_path)
        print(f"[Info] Parsed last log entry successfully.")
        print(f"  Log Version: {log_entry['version']}")
        print(f"  Log Title  : {log_entry['title']}")
        print(f"  ToDo Ref   : {log_entry['todo_ref']}")
    except Exception as e:
        print(f"\n[Strict Parsing Error] {e}")
        print("Please fix the last entry in logs/cold-history.log and run again.\n")
        sys.exit(1)
        
    # 2. Sync ToDo
    todo_ref_val = log_entry["todo_ref"]
    is_task_free = todo_ref_val.lower() in ["null", "none", "", "empty"]
    
    if is_task_free:
        print("[Info] Task-free change detected (todo_ref is null/none). Skipping ToDo checkbox update.")
    else:
        try:
            sync_todos(process_path, todo_ref_val)
        except Exception as e:
            print(f"\n[Strict Parsing Error] {e}")
            print("Please correct the todo_ref in logs/cold-history.log to match an open ToDo and try again.\n")
            sys.exit(1)
            
    # 3. Bump version
    try:
        old_version, new_version, new_process_content = bump_version(process_path, args.bump)
    except Exception as e:
        print(f"\n[Error] Failed to calculate version bump: {e}")
        sys.exit(1)
        
    # Validate version consistency between log header and calculated version
    log_version_normalized = log_entry["version"].lstrip('v')
    new_version_normalized = new_version.lstrip('v')
    if log_version_normalized != new_version_normalized:
        print(f"\n[Strict Parsing Error] Version mismatch detected!")
        print(f"  Version in logs/cold-history.log: v{log_version_normalized}")
        print(f"  Calculated version in PROCESS.md: v{new_version_normalized}")
        print("Please align the version in logs/cold-history.log to match the calculated progression and try again.\n")
        sys.exit(1)
        
    # Commit version bump to PROCESS.md
    try:
        with open(process_path, 'w', encoding='utf-8') as f:
            f.write(new_process_content)
        print(f"[Info] Bumped version: {old_version} -> {new_version} in PROCESS.md.")
    except Exception as e:
        print(f"\n[Error] Failed to write version to PROCESS.md: {e}")
        sys.exit(1)
        
    # 4. Update MEMORY.md hot memory
    try:
        update_memory_md(memory_path, new_version, log_entry)
    except Exception as e:
        print(f"[Warning] Failed to update MEMORY.md: {e}")
        

    
    # 6. Save State JSON
    open_todos = get_open_todos(process_path)
    last_task_desc = "Task-free change" if is_task_free else todo_ref_val
    save_state(state_path, new_version, last_task_desc, open_todos)
    
    print(f"\n[Success] Project status synced successfully to version: {new_version}")
    print(f"[Git Command Tip] git commit -m \"{new_version} {log_entry['title']}\"\n")

if __name__ == "__main__":
    main()
