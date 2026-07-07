# Council Decision: Git Hook Mechanism for AI Agent Commit Validation

**Status**: Consensus Approved (Review Passed)  
**Date**: 2026-07-07  
**Participants**:
- Consensus Coordinator (Lead Agent)
- Proposal Executor (`council_executor`)
- Proposal Critic (`council_critic`)

---

## 1. Context and Objective
AI agents working on this project template are required to maintain strict versioning alignment across multiple files (`plan/PROCESS.md`, `logs/cold-history.log`, and `.sync-state.json`) and write clean, English-only commit messages prefixed with the version number. Doing these checks manually is error-prone. 

This decision defines the implementation of a localized Git Hook system (`pre-commit` and `commit-msg`) designed specifically for Windows environments to automate validation before commits are accepted.

---

## 2. Technical Architecture & Design Consensus

To ensure portability on Windows, where Git hooks are run within Git Bash's shell (`/bin/sh` or `bash`) and path configurations can be fragile across GUI clients, the council agreed on a hybrid model:
1. **Lightweight Shell Wrappers**: Placed in `.git/hooks/` to resolve local PATH issues, check if python is runnable, locate the repository root dynamically via `git rev-parse --show-toplevel`, and execute the python validator script.
2. **Python Validator (`scripts/git_hook_validator.py`)**: Cross-platform python script implementing the detailed formatting, language character encoding, and file synchronization checks.

```
[git commit]
    │
    ├──► 1. pre-commit (shell wrapper)
    │         └──► python scripts/git_hook_validator.py pre-commit
    │                   └──► Verify plan/PROCESS.md, logs/cold-history.log, and .sync-state.json versions match.
    │
    └──► 2. commit-msg (shell wrapper)
              └──► python scripts/git_hook_validator.py commit-msg "$1"
                        ├──► Block CJK characters/punctuation (English only).
                        ├──► Check title pattern: vX.Y.YYYYMMDD.Z Summary.
                        └──► Check if commit version matches project file versions.
```

---

## 3. Implemented Components

The following files have been successfully added/updated in the workspace:
1. **[NEW] [git_hook_validator.py](file:///c:/PersonalWS/AgentSandBox/AiProjectTemplate/scripts/git_hook_validator.py)**: The central validation engine.
2. **[NEW] [install_hooks.py](file:///c:/PersonalWS/AgentSandBox/AiProjectTemplate/scripts/install_hooks.py)**: Installer script that writes CWD-independent and alias-safe wrappers into `.git/hooks/`.
3. **[MODIFY] [bootstrap.py](file:///c:/PersonalWS/AgentSandBox/AiProjectTemplate/scripts/bootstrap.py)**: Integrated automatic hook installation during project initialization and zero-commit creation.
4. **[MODIFY] [sync_project.py](file:///c:/PersonalWS/AgentSandBox/AiProjectTemplate/scripts/sync_project.py)**: Removed redundant commit warnings and integrated early syntax checks for malformed headers in `cold-history.log`.

---

## 4. Key Critic Audits Resolved

- **Git Executable Bypass (High)**: If `git` is missing from the environment PATH (such as in some GUI clients), the validator prints a warning but enforces the local file checks instead of bypassing validation.
- **Microsoft Store Alias Trap (Medium)**: Added `is_runnable` logic in the shell wrappers to check if `python3` or `python` is fully functional (prevents blocking or triggering Microsoft Store popups).
- **CWD Independence (Medium)**: Resolves the repository path using `git rev-parse --show-toplevel` so hooks execute correctly regardless of where the commit command is run.
- **Expanded CJK Filter (Medium)**: Enhanced message filtering to block Japanese (Hiragana/Katakana) and Korean (Hangul) along with Chinese. Smart quotes and emojis are still allowed.
- **Syntax Error Protection (Medium)**: Both the validator and the sync script throw clean errors if there are syntax errors/typos in the header format of `logs/cold-history.log`.
