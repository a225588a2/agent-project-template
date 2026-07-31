#!/usr/bin/env python3
"""
New Project Initializer Utility - Dual Versioning Strategy Aware

Copies template files to a target directory, processes conditional markers
to strip the unselected versioning strategy, and initializes a Git repository.
"""
import os
import sys
import re
import json
import shutil
import argparse
import subprocess
from datetime import datetime
from typing import Optional, List

# ---------------------------------------------------------------------------
# Conditional Marker Renderer
# ---------------------------------------------------------------------------

KEEP_PATTERN = re.compile(r'<!--\s*@KEEP:(\w+)\s*-->')
END_PATTERN = re.compile(r'<!--\s*@END:(\w+)\s*-->')


def render_conditional_markers(content: str, selected_strategy: str) -> str:
    """
    Process conditional markers in template content.

    Markers:
      <!-- @KEEP:SEMVER --> ... <!-- @END:SEMVER -->  kept when strategy == 'semver'
      <!-- @KEEP:CALVER --> ... <!-- @END:CALVER -->  kept when strategy == 'calver'
      <!-- @KEEP:TEMPLATE --> ... <!-- @END:TEMPLATE --> always removed in new projects

    Content outside markers is always kept.
    Marker lines themselves are always removed.
    Consecutive blank lines are collapsed to at most one.
    """
    lines = content.splitlines(keepends=True)
    result: List[str] = []
    skip_stack: List[tuple] = []  # (tag_lower, should_skip)

    for line in lines:
        keep_m = KEEP_PATTERN.search(line)
        end_m = END_PATTERN.search(line)

        if keep_m:
            tag = keep_m.group(1).lower()
            should_skip = (tag != selected_strategy.lower())
            skip_stack.append((tag, should_skip))
            continue  # remove the marker line itself
        elif end_m:
            end_tag = end_m.group(1).lower()
            if skip_stack and skip_stack[-1][0] == end_tag:
                skip_stack.pop()
            else:
                raise ValueError(
                    f"Mismatched marker: @END:{end_m.group(1)} "
                    f"without matching @KEEP:{end_m.group(1)}"
                )
            continue  # remove the marker line itself
        elif skip_stack and skip_stack[-1][1]:
            continue  # inside an unselected block — skip
        else:
            result.append(line)

    if skip_stack:
        unclosed = skip_stack[-1][0]
        raise ValueError(f"Unclosed conditional marker: @KEEP:{unclosed.upper()}")

    # Collapse 3+ consecutive newlines into 2 (one blank line)
    return re.sub(r'\n{3,}', '\n\n', ''.join(result))


# ---------------------------------------------------------------------------
# Strategy Resolution
# ---------------------------------------------------------------------------

def resolve_strategy(cli_arg: Optional[str], target_dir: str,
                     non_interactive: bool) -> str:
    """Determine the versioning strategy to use."""
    if cli_arg and cli_arg in ('semver', 'calver'):
        return cli_arg

    if non_interactive:
        dir_name = os.path.basename(os.path.abspath(target_dir)).lower()
        calver_hints = ['note', 'log', 'journal', 'brain',
                        'obsidian', 'wiki', 'diary', 'memo']
        if any(hint in dir_name for hint in calver_hints):
            print("[AUTO-DETECT] Directory name suggests note/journal project -> CalVer")
            return 'calver'
        print("[AUTO-DETECT] Defaulting to SemVer for code/software project")
        return 'semver'

    # TTY interactive menu
    print("\n  Select versioning strategy:")
    print("    [1] SemVer 2.0  (code / software / packages)")
    print("    [2] CalVer      (notes / journals / data)")
    try:
        choice = input("  Enter 1 or 2 (default=1): ").strip()
    except EOFError:
        choice = ''
    return 'calver' if choice == '2' else 'semver'


# ---------------------------------------------------------------------------
# File Operations
# ---------------------------------------------------------------------------

def _resolve_repo_root() -> str:
    """Locate the template repository root."""
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.sync-state.json')):
            return current
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _copy_with_markers(src_path: str, dst_path: str, strategy: str) -> None:
    """Copy a file, processing conditional markers."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    rendered = render_conditional_markers(content, strategy)
    # Title rewrites: remove "雙軌" references for cleanliness
    rendered = rendered.replace('雙軌版本策略規範 (Dual Versioning Strategy)',
                                '版本策略規範 (Versioning Strategy)')
    rendered = rendered.replace('雙軌版本模式 (Dual Versioning Strategy)',
                                '版本模式')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(rendered)


def _copy_tree(src_dir: str, dst_dir: str,
               exclude: Optional[List[str]] = None) -> None:
    """Recursively copy a directory, skipping exclusions."""
    exclude = exclude or []
    if not os.path.isdir(src_dir):
        return
    for item in os.listdir(src_dir):
        if item in exclude:
            continue
        s = os.path.join(src_dir, item)
        d = os.path.join(dst_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)


def _copy_file(src: str, dst: str) -> None:
    """Copy a single file, creating parent dirs."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


# ---------------------------------------------------------------------------
# Fresh File Generators
# ---------------------------------------------------------------------------

def _generate_sync_state(target: str, name: str, strategy: str) -> None:
    now = datetime.now()
    if strategy == 'calver':
        version = f"v1.0.{now.strftime('%Y%m%d')}.1"
    else:
        version = "v0.1.0"
    state = {
        "version": version,
        "version_strategy": strategy,
        "last_updated": now.isoformat(),
        "last_todo_ref": None,
        "last_commit_summary": f"Initialize project: {name}"
    }
    path = os.path.join(target, '.sync-state.json')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write('\n')


def _generate_target_md(target: str, name: str) -> None:
    content = f"""# 專案核心目標書 (Target)

本文件定義本專案的最終目標、核心應用情境、功能範圍與品質標準。

---

## 1. 專案核心目標 (Project Goal)

> 我們的目標是：`{name}`

---

## 2. 核心使用情境 (Core Scenarios)

> 1. **`[情境一]`** - `[待填入]`
> 2. **`[情境二]`** - `[待填入]`

---

## 3. 初步功能與執行範圍 (Scope of Work)

> ### 納入範圍 (In Scope)
> - `[待填入]`
>
> ### 排除範圍 (Out of Scope)
> - `[待填入]`
"""
    path = os.path.join(target, 'plan', 'TARGET.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def _generate_process_md(target: str) -> None:
    content = """# 專案進度與開發計畫 (Process)

---

## 目前狀態 (Current Status)

- **當前進度**：[專案初始化完成]
- **目前版本**：見 `.sync-state.json`

---

## 已完成的里程碑 (Completed Milestones)

- [x] 專案初始化完成 (Project Initialized)。

---

## 分階段開發計畫與待辦項目 (Development Plan & ToDo List)

### 階段 1：核心功能實作 🚀 進行中
- [ ] `[待填入]`
"""
    path = os.path.join(target, 'plan', 'PROCESS.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def _generate_memory_md(target: str, name: str, strategy: str) -> None:
    strategy_label = 'SemVer 2.0' if strategy == 'semver' else 'CalVer'
    content = f"""# 專案執行紀錄與決策歷史 (Hot Memory)

本文件僅記錄專案的「熱記憶 (Hot Memory)」。
詳細歷史變更日誌已物理分離至 [[plan/cold-history.log]]。

---

## 📌 專案滾動式摘要 (Rolling Summary)

- **當前核心目標**：{name}
- **版本策略**：{strategy_label}

---

## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)

（初始化完成，尚無變更記錄）
"""
    path = os.path.join(target, 'plan', 'MEMORY.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def _generate_cold_history(target: str, name: str) -> None:
    path = os.path.join(target, 'plan', 'cold-history.log')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f"# Cold History Log - {name}\n\n")
        f.write(f"## [{now}] Project Initialized\n")
        f.write(f"- Bootstrapped from AiProjectTemplate.\n")


# ---------------------------------------------------------------------------
# Git Operations
# ---------------------------------------------------------------------------

def _run_git(cmd: str, cwd: str) -> bool:
    """Run a git command, return True on success."""
    try:
        subprocess.run(
            cmd, shell=True, cwd=cwd, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[GIT ERROR] {cmd}: {e.stderr.decode(errors='replace').strip()}")
        return False


def _check_git_author(cwd: str) -> None:
    """Check and warn if git user.name or user.email is not configured."""
    try:
        name = subprocess.run(
            'git config user.name', shell=True, cwd=cwd,
            capture_output=True, text=True
        ).stdout.strip()
        email = subprocess.run(
            'git config user.email', shell=True, cwd=cwd,
            capture_output=True, text=True
        ).stdout.strip()
        if not name or not email:
            print("[WARNING] Git author not configured. Please set:")
            print(f'  git config user.name "Your Name"')
            print(f'  git config user.email "your.email@example.com"')
        else:
            print(f"[GIT AUTHOR] {name} <{email}>")
    except Exception:
        print("[WARNING] Could not check git author configuration.")


# ---------------------------------------------------------------------------
# Main Bootstrap
# ---------------------------------------------------------------------------

def bootstrap(target_dir: str, name: str, strategy: str,
              modules: Optional[List[str]] = None,
              non_interactive: bool = False,
              force: bool = False) -> None:
    """Bootstrap a new project from the AiProjectTemplate."""
    repo_root = _resolve_repo_root()
    target = os.path.abspath(target_dir)

    # Safety guard: prevent self-destruction
    if os.path.normcase(os.path.abspath(target)) == os.path.normcase(os.path.abspath(repo_root)):
        print("[FATAL] Cannot bootstrap into the template directory itself!")
        sys.exit(1)

    # Non-empty target guard
    if os.path.exists(target) and os.listdir(target):
        if not force:
            print(f"[ERROR] Target directory is not empty: {target}")
            print("  Use --force to overwrite.")
            sys.exit(1)
        print(f"[WARNING] Target directory is not empty, proceeding with --force.")

    print(f"\n{'='*60}")
    print(f"  AiProjectTemplate Bootstrap")
    print(f"  Template : {repo_root}")
    print(f"  Target   : {target}")
    print(f"  Name     : {name}")
    print(f"  Strategy : {strategy.upper()}")
    print(f"{'='*60}\n")

    os.makedirs(target, exist_ok=True)

    # --- 1. Files with conditional marker processing ---
    marker_files = [
        ('plan/AGENT.md', 'plan/AGENT.md'),
        ('plan/GIT-GUIDE.md', 'plan/GIT-GUIDE.md'),
        ('README.md', 'README.md'),
    ]
    for src_rel, dst_rel in marker_files:
        src = os.path.join(repo_root, src_rel)
        dst = os.path.join(target, dst_rel)
        if os.path.exists(src):
            _copy_with_markers(src, dst, strategy)
            print(f"  [RENDER] {dst_rel}")

    # --- 2. Copy as-is directories ---
    copy_dirs = ['doc', 'structure', 'skills', 'scripts']
    for d in copy_dirs:
        src = os.path.join(repo_root, d)
        dst = os.path.join(target, d)
        if os.path.isdir(src):
            _copy_tree(src, dst)
            print(f"  [COPY]   {d}/")

    # Copy optional files
    for f_name in ['.gitignore']:
        src = os.path.join(repo_root, f_name)
        if os.path.exists(src):
            _copy_file(src, os.path.join(target, f_name))
            print(f"  [COPY]   {f_name}")

    # Copy optional plan files
    for f_name in ['plan/FEEDBACK.md']:
        src = os.path.join(repo_root, f_name)
        if os.path.exists(src):
            _copy_file(src, os.path.join(target, f_name))
            print(f"  [COPY]   {f_name}")

    # --- 3. Create optional module directories ---
    modules = modules or []
    for mod in modules:
        mod_path = os.path.join(target, mod.strip())
        os.makedirs(mod_path, exist_ok=True)
        # Add .gitkeep so git tracks empty dirs
        gitkeep = os.path.join(mod_path, '.gitkeep')
        if not os.path.exists(gitkeep):
            with open(gitkeep, 'w') as f:
                pass
        print(f"  [MODULE] {mod.strip()}/")

    # --- 4. Generate fresh files ---
    _generate_sync_state(target, name, strategy)
    print(f"  [GEN]    .sync-state.json")
    _generate_target_md(target, name)
    print(f"  [GEN]    plan/TARGET.md")
    _generate_process_md(target)
    print(f"  [GEN]    plan/PROCESS.md")
    _generate_memory_md(target, name, strategy)
    print(f"  [GEN]    plan/MEMORY.md")
    _generate_cold_history(target, name)
    print(f"  [GEN]    plan/cold-history.log")

    # --- 5. Git initialization ---
    print(f"\n  --- Git Initialization ---")
    _run_git('git init', target)
    _check_git_author(target)
    _run_git('git add .', target)

    if strategy == 'semver':
        commit_msg = 'feat(init): initialize project structure'
        _run_git(f'git commit -m "{commit_msg}" --no-verify', target)
        _run_git('git branch develop', target)
        print(f"  [GIT]    Created branch: develop")
    else:
        now = datetime.now()
        version = f"v1.0.{now.strftime('%Y%m%d')}.1"
        commit_msg = f'{version} Initialize project structure'
        _run_git(f'git commit -m "{commit_msg}" --no-verify', target)

    # --- 6. Install hooks ---
    try:
        hooks_installer = os.path.join(target, 'scripts', 'install_hooks.py')
        if os.path.exists(hooks_installer):
            # Import and call directly instead of subprocess to avoid path issues
            sys.path.insert(0, os.path.join(target, 'scripts'))
            from install_hooks import install_hooks as _install
            _install(target)
            sys.path.pop(0)
    except Exception as e:
        print(f"[WARNING] Could not install hooks: {e}")

    # --- Summary ---
    strategy_label = 'SemVer 2.0' if strategy == 'semver' else 'CalVer'
    print(f"\n{'='*60}")
    print(f"  ✅ Project '{name}' initialized successfully!")
    print(f"  Strategy: {strategy_label}")
    if strategy == 'semver':
        print(f"  Branches: main, develop")
        print(f"  Commit format: type(scope): summary")
    else:
        print(f"  Branch: main")
        print(f"  Commit format: v1.0.YYYYMMDD.Z summary")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bootstrap a new AI project from AiProjectTemplate."
    )
    parser.add_argument(
        '--target-dir', '-o', '--output', dest='target_dir',
        required=True, help='Target output directory for the new project'
    )
    parser.add_argument(
        '--name', '-n', dest='name',
        default=None, help='Project name (defaults to target directory name)'
    )
    parser.add_argument(
        '--version-strategy', '-v', dest='strategy',
        choices=['semver', 'calver'], default=None,
        help='Version strategy: semver or calver'
    )
    parser.add_argument(
        '--modules', '-m', dest='modules',
        default=None,
        help='Comma-separated list of optional modules to create (e.g. "source,test")'
    )
    parser.add_argument(
        '--non-interactive', dest='non_interactive',
        action='store_true', default=False,
        help='Run without interactive prompts (auto-detect strategy)'
    )
    parser.add_argument(
        '--force', dest='force',
        action='store_true', default=False,
        help='Force initialization even if target directory is not empty'
    )

    args = parser.parse_args()

    project_name = args.name or os.path.basename(os.path.abspath(args.target_dir))
    strategy = resolve_strategy(args.strategy, args.target_dir, args.non_interactive)
    mod_list = [m.strip() for m in args.modules.split(',')] if args.modules else []

    bootstrap(
        target_dir=args.target_dir,
        name=project_name,
        strategy=strategy,
        modules=mod_list,
        non_interactive=args.non_interactive,
        force=args.force,
    )
