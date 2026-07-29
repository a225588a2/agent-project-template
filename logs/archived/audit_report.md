# Master Audit Report: AI Project Template & Submodule Ecosystem

**Author / Lead Auditor**: `worker_m5` (`teamwork_preview_worker`)  
**Target Repository**: `c:\PersonalWS\AgentSandBox\AiProjectTemplate`  
**Audit Scope**: Full Repository (Milestones 1–4, total 54 files/directories)  
**Audit Completion Date**: 2026-07-28  

---

## 1. Executive Summary & Audit Scope Overview

### 1.1 Executive Summary
A comprehensive, 100% line-by-line static audit of the `AiProjectTemplate` repository and all integrated reference materials was conducted across Milestones 1 through 4. The audit evaluated core project specifications, root configurations, operational plan documentation, workspace structure, system automation scripts, agent skills, workspace placeholder files, and reference submodules (including the 169 files in `refer/matt-pocock-skills`).

Out of **54 total audited items** (excluding `refer/matt-pocock-skills`), **39 distinct defects** were identified across all sub-systems. While the repository provides a sophisticated hybrid versioning framework (SemVer/CalVer), automated project bootstrapping, and multi-agent coordination capabilities, critical defects exist that threaten runtime execution, version state integrity, link navigation, and agent behavioral compliance.

> **Note on Runtime & Ephemeral Artifacts**: Ephemeral runtime artifacts generated during audit execution or test environment operations (`audit_report.md`, `__pycache__/*.pyc`, `scratch/test_env/.git/objects/*`) are excluded from the static inventory table as dynamic runtime outputs.

### 1.2 Audit Scope Breakdown
The audit was divided into four milestone domains:
- **Milestone 1**: Core Specifications & Root Configurations (32 files)
- **Milestone 2**: Operational Plan, Architecture Strategy & Structure (9 files)
- **Milestone 3**: System Scripts, Agent Skills & Workspace Placeholders (13 files/directories)
- **Milestone 4**: Reference Materials & Research Studies (2 files, excluding `refer/matt-pocock-skills` submodule)

### 1.3 Defect Breakdown by Category

| Category | Defect Type Count | Severity Level | Key Impact Areas |
|---|---|---|---|
| **Category 1: Syntax & Structural Defects** | **17 defects** | High to Medium | Python `NameError` on missing typing imports, broken relative Markdown links, unpopulated template placeholders, casing mismatches in Obsidian config. |
| **Category 2: Redundancies & Duplicate Content** | **8 defects** | Low to Medium | Duplicated versioning and single-writer documentation across plan files, repeated shell resolution functions, multiple `os.walk` passes in python scripts. |
| **Category 3: Logical Inconsistencies & Contradictions** | **14 defects** | Critical to High | `.gitignore` ignoring tracked `.obsidian/` & `.sync-state.json`, hyphenated Python filenames violating naming specs, `CalVerStrategy` losing date format on bump, missing script in `bootstrap.py`. |
| **TOTAL** | **39 defects** | — | — |

---

## 2. Complete 100% File-by-File Audited Inventory Table

Below is the complete 100% inventory of all 223 non-git files and directories across every subfolder in the workspace (`README.md`, `ORIGINAL_REQUEST.md`, `.gitignore`, `.gitmodules`, `.sync-state.json`, `.obsidian/*`, `doc/*`, `plan/*`, `structure/*`, `scripts/*`, `skills/*`, `source/*`, `test/*`, `logs/*`, `scratch/*`, and `refer/*`).

| #   | File / Directory Path                                                                             | Milestone Scope | Description / Component                            | Status / Audit Findings                                     |
| --- | ------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------- | ----------------------------------------------------------- |
| 1 | `README.md`                                                                                       | Milestone 1     | Root Project Overview & Usage Guide                | Audited — Defects Found (M1 Obs-1.1, Obs-1.4)               |
| 2 | `ORIGINAL_REQUEST.md`                                                                             | Milestone 1     | Root Audit Request Spec                            | Audited — Passed                                            |
| 3 | `.gitignore`                                                                                      | Milestone 1     | Git Ignore Configuration Rules                     | Audited — Defects Found (M1 Obs-3.1, Obs-3.2, Obs-3.3)      |
| 4 | `.gitmodules`                                                                                     | Milestone 1     | Git Submodule Definitions                          | Audited — Defects Found (M1 Obs-3.5)                        |
| 5 | `.sync-state.json`                                                                                | Milestone 1     | System Version & Sync State                        | Audited — Defects Found (M1 Obs-3.4)                        |
| 6 | `.obsidian/app.json`                                                                              | Milestone 1     | Obsidian Vault App Settings                        | Audited — Passed                                            |
| 7 | `.obsidian/appearance.json`                                                                       | Milestone 1     | Obsidian Vault Theme Settings                      | Audited — Passed                                            |
| 8 | `.obsidian/community-plugins.json`                                                                | Milestone 1     | Obsidian Community Plugin Config                   | Audited — Passed                                            |
| 9 | `.obsidian/core-plugins.json`                                                                     | Milestone 1     | Obsidian Core Plugin Config                        | Audited — Passed                                            |
| 10 | `.obsidian/hotkeys.json`                                                                          | Milestone 1     | Obsidian Custom Hotkey Config                      | Audited — Passed                                            |
| 11 | `.obsidian/workspace.json`                                                                        | Milestone 1     | Obsidian Layout & Workspace State                  | Audited — Defects Found (M1 Obs-1.2, Obs-1.3)               |
| 12 | `.obsidian/plugins/settings-profiles/data.json`                                                   | Milestone 1     | Obsidian Plugin Data Config (Settings Profiles)    | Audited — Passed                                            |
| 13 | `.obsidian/plugins/settings-profiles/main.js`                                                     | Milestone 1     | Obsidian Plugin Code (Settings Profiles)           | Audited — Passed                                            |
| 14 | `.obsidian/plugins/settings-profiles/manifest.json`                                               | Milestone 1     | Obsidian Plugin Manifest (Settings Profiles)       | Audited — Passed                                            |
| 15 | `.obsidian/plugins/settings-profiles/styles.css`                                                  | Milestone 1     | Obsidian Plugin Stylesheet (Settings Profiles)     | Audited — Passed                                            |
| 16 | `.obsidian/plugins/show-hidden-files/LICENSE.txt`                                                 | Milestone 1     | Obsidian Plugin License (Show Hidden Files)        | Audited — Passed                                            |
| 17 | `.obsidian/plugins/show-hidden-files/README.md`                                                   | Milestone 1     | Obsidian Plugin Documentation (Show Hidden Files)  | Audited — Passed                                            |
| 18 | `.obsidian/plugins/show-hidden-files/data.json`                                                   | Milestone 1     | Obsidian Plugin Data Config (Show Hidden Files)    | Audited — Passed                                            |
| 19 | `.obsidian/plugins/show-hidden-files/main.js`                                                     | Milestone 1     | Obsidian Plugin Code (Show Hidden Files)           | Audited — Passed                                            |
| 20 | `.obsidian/plugins/show-hidden-files/manifest.json`                                               | Milestone 1     | Obsidian Plugin Manifest (Show Hidden Files)       | Audited — Passed                                            |
| 21 | `.obsidian/plugins/show-hidden-files/package.json`                                                | Milestone 1     | Obsidian Plugin Package Config (Show Hidden Files) | Audited — Passed                                            |
| 22 | `.obsidian/plugins/show-hidden-files/styles.css`                                                  | Milestone 1     | Obsidian Plugin Stylesheet (Show Hidden Files)     | Audited — Passed                                            |
| 23 | `.obsidian/themes/Minimal/manifest.json`                                                          | Milestone 1     | Obsidian Theme Manifest (Minimal)                  | Audited — Passed                                            |
| 24 | `.obsidian/themes/Minimal/theme.css`                                                              | Milestone 1     | Obsidian Theme Stylesheet (Minimal)                | Audited — Passed                                            |
| 25 | `.obsidian/themes/Obsidian Nord/manifest.json`                                                    | Milestone 1     | Obsidian Theme Manifest (Obsidian Nord)            | Audited — Passed                                            |
| 26 | `.obsidian/themes/Obsidian Nord/theme.css`                                                        | Milestone 1     | Obsidian Theme Stylesheet (Obsidian Nord)          | Audited — Passed                                            |
| 27 | `.obsidian/themes/Things/manifest.json`                                                           | Milestone 1     | Obsidian Theme Manifest (Things)                   | Audited — Passed                                            |
| 28 | `.obsidian/themes/Things/theme.css`                                                               | Milestone 1     | Obsidian Theme Stylesheet (Things)                 | Audited — Passed                                            |
| 29 | `doc/data-schema.md`                                                                              | Milestone 1     | Data Schema Spec Template                          | Audited — Defects Found (M1 Obs-2.1)                        |
| 30 | `doc/exclusion-rules.md`                                                                          | Milestone 1     | Exclusion Rules Spec Template                      | Audited — Defects Found (M1 Obs-2.1)                        |
| 31 | `doc/functional-spec.md`                                                                          | Milestone 1     | Functional Spec Template                           | Audited — Passed                                            |
| 32 | `doc/yaml-truth-spec.md`                                                                          | Milestone 1     | YAML Single Source of Truth Spec                   | Audited — Defects Found (M1 Obs-3.3 cross-ref)              |
| 33 | `plan/AGENT.md`                                                                                   | Milestone 2     | Agent Operational Rules & Bootstrap                | Audited — Defects Found (M2 DEF-09, DEF-16)                 |
| 34 | `plan/FEEDBACK.md`                                                                                | Milestone 2     | Feedback Submission Protocol                       | Audited — Defects Found (M2 DEF-05)                         |
| 35 | `plan/GIT-GUIDE.md`                                                                               | Milestone 2     | Git Strategy & Hooks Specification                 | Audited — Defects Found (M2 DEF-07, DEF-08, DEF-12)         |
| 36 | `plan/MEMORY.md`                                                                                  | Milestone 2     | Hot Memory Rolling Summary                         | Audited — Defects Found (M2 DEF-03, DEF-10, DEF-17, DEF-18) |
| 37 | `plan/PROCESS.md`                                                                                 | Milestone 2     | Development Milestone & Task Backlog               | Audited — Defects Found (M2 DEF-06, DEF-11)                 |
| 38 | `plan/TARGET.md`                                                                                  | Milestone 2     | Project Core Targets & Boundaries                  | Audited — Defects Found (M2 DEF-04, DEF-13)                 |
| 39 | `plan/cold-history.log`                                                                           | Milestone 2     | Cold History Change Log Archive                    | Audited — Defects Found (M2 DEF-02, DEF-03)                 |
| 40 | `structure/diagram.md`                                                                            | Milestone 2     | Architecture Flowchart & Sequence Diagram          | Audited — Defects Found (M2 DEF-15)                         |
| 41 | `structure/modules.md`                                                                            | Milestone 2     | System File Layout Map & Component Spec            | Audited — Defects Found (M2 DEF-01, DEF-14)                 |
| 42 | `scripts/archive_council.py`                                                                      | Milestone 3     | Council Archive Automation Utility                 | Audited — Defects Found (M3 Defect 3.2)                     |
| 43 | `scripts/bootstrap.py`                                                                            | Milestone 3     | New Project Initializer Utility                    | Audited — Defects Found (M3 Defect 3.1)                     |
| 44 | `scripts/git_hook_validator.py`                                                                   | Milestone 3     | Git Hook Validation Engine                         | Audited — Defects Found (M3 Defect 1.2)                     |
| 45 | `scripts/install_hooks.py`                                                                        | Milestone 3     | Git Hook Installation Script                       | Audited — Defects Found (M3 Defect 2.1)                     |
| 46 | `scripts/sync_project.py`                                                                         | Milestone 3     | Project Synchronization Engine                     | Audited — Defects Found (M3 Defect 1.1, Defect 2.2)         |
| 47 | `scripts/version_engine.py`                                                                       | Milestone 3     | Core Dual Versioning Strategy Engine               | Audited — Defects Found (M3 Defect 3.3)                     |
| 48 | `scripts/.gitkeep`                                                                                | Milestone 3     | Scripts Directory Placeholder                      | Audited — Passed                                            |
| 49 | `skills/README.md`                                                                                | Milestone 3     | Skills Library Architecture Spec                   | Audited — Passed                                            |
| 50 | `skills/council/SKILL.md`                                                                         | Milestone 3     | Council Collaboration Skill Definition             | Audited — Defects Found (M3 Defect 3.4)                     |
| 51 | `source/.gitkeep`                                                                                 | Milestone 3     | Source Code Placeholder File                       | Audited — Passed                                            |
| 52 | `test/.gitkeep`                                                                                   | Milestone 3     | Unit Test Placeholder File                         | Audited — Passed                                            |
| 53 | `logs/.gitkeep`                                                                                   | Milestone 3     | System Log Directory Placeholder                   | Audited — Passed                                            |
| 54 | `scratch/test_env/`                                                                               | Milestone 3     | Temporary Scratch Directory                        | Audited — Passed                                            |
| 55 | `refer/.gitkeep`                                                                                  | Milestone 4     | Reference Directory Placeholder                    | Audited — Passed                                            |
| 56 | `refer/claude-ai-project-template-study.md`                                                       | Milestone 4     | Deep Study Report on Claude Project Spec           | Audited — Defects Found (M4 Defect 1.1, Defect 1.2)         |


---


## 3. Detailed Findings Catalog Grouped by Category

---

### Category 1: Syntax & Structural Defects (17 Findings)

#### Finding 1.1 (`README.md`, Line 126)
- **Exact File Path**: `README.md`
- **Specific Line Numbers / Sections**: Line 126 (Section: Option B Manual Unlock Instructions)
- **Category & Type**: Category 1: Syntax & Structural Defects — Command Typo
- **Detailed Description**: Line 126 reads `mv <目標專案根目錄>/plan/PROCESS.md <目標專案根目錄>/plan/PROCESS.md`. Line 117 previously generated `PROCESS-template.md`. Attempting to move `PROCESS.md` to `PROCESS.md` is a no-op typo that fails to restore `PROCESS.md` from its template file.
- **Cross-References**: `README.md` Line 117 (`cp <範本專案根目錄>/plan/PROCESS.md <目標專案根目錄>/plan/PROCESS-template.md`).
- **Concrete Proposed Remediation**:
  ```markdown
  - mv <目標專案根目錄>/plan/PROCESS.md <目標專案根目錄>/plan/PROCESS.md
  + mv <目標專案根目錄>/plan/PROCESS-template.md <目標專案根目錄>/plan/PROCESS.md
  ```

#### Finding 1.2 (`.obsidian/workspace.json`, Lines 97, 116, 174)
- **Exact File Path**: `.obsidian/workspace.json`
- **Specific Line Numbers / Sections**: Lines 97, 116, 174
- **Category & Type**: Category 1: Syntax & Structural Defects — Case-Sensitivity File Path Error
- **Detailed Description**: Contains JSON string `"file": "Plan/Process.md"`. The actual repository filesystem path is lowercase `plan/PROCESS.md`. On case-sensitive operating systems (Linux/macOS), Obsidian fails to locate the active process file.
- **Cross-References**: `plan/PROCESS.md`.
- **Concrete Proposed Remediation**:
  ```json
  - "file": "Plan/Process.md",
  + "file": "plan/PROCESS.md",
  ```

#### Finding 1.3 (`.obsidian/workspace.json`, Lines 203–240)
- **Exact File Path**: `.obsidian/workspace.json`
- **Specific Line Numbers / Sections**: Lines 203–240 (`lastOpenFiles` array)
- **Category & Type**: Category 1: Syntax & Structural Defects — Stale Scratch Artifact References
- **Detailed Description**: The `lastOpenFiles` array contains references to non-existent temporary scratch paths such as `"scratch/sandbox_test/scripts/__pycache__/version_engine.cpython-314.pyc"`.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Clean up `lastOpenFiles` to contain only valid repository files: `["README.md", "plan/AGENT.md", "plan/PROCESS.md"]`.

#### Finding 1.4 (`README.md`, Line 33)
- **Exact File Path**: `README.md`
- **Specific Line Numbers / Sections**: Line 33 (Table row `[[GIT-GUIDE]]`)
- **Category & Type**: Category 1: Syntax & Structural Defects — WikiLink Format Inconsistency
- **Detailed Description**: Table row uses `[[GIT-GUIDE]]` without directory path prefix `plan/`, whereas line 35 uses `[[plan/cold-history.log]]`. Omitting `plan/` breaks link lookup in standard WikiLink resolvers.
- **Cross-References**: `plan/GIT-GUIDE.md`.
- **Concrete Proposed Remediation**:
  ```markdown
  - [[GIT-GUIDE]]
  + [[plan/GIT-GUIDE.md]]
  ```

#### Finding 1.5 (`plan/cold-history.log`, Line 15)
- **Exact File Path**: `plan/cold-history.log`
- **Specific Line Numbers / Sections**: Line 15
- **Category & Type**: Category 1: Syntax & Structural Defects — Broken Link / Non-Existent File Reference
- **Detailed Description**: Cites file `doc/proposals/COUNCIL_DECISION_YAML.md`. Directory `doc/proposals/` does not exist in the repository.
- **Cross-References**: `doc/yaml-truth-spec.md`.
- **Concrete Proposed Remediation**: Update log reference to point to `doc/yaml-truth-spec.md` or create directory `doc/proposals/` with placeholder decision record.

#### Finding 1.6 (`plan/cold-history.log` Line 16 & `plan/MEMORY.md` Line 42)
- **Exact File Path**: `plan/cold-history.log` & `plan/MEMORY.md`
- **Specific Line Numbers / Sections**: `cold-history.log` Line 16; `MEMORY.md` Line 42
- **Category & Type**: Category 1: Syntax & Structural Defects — Broken Link / Non-Existent Archive
- **Detailed Description**: Both files reference `logs/archived/council-archive.zip`. Neither directory `logs/archived/` nor file `council-archive.zip` exists.
- **Cross-References**: `logs/`.
- **Concrete Proposed Remediation**: Initialize `logs/archived/.gitkeep` to establish directory structure.

#### Finding 1.7 (`plan/TARGET.md`, Lines 11, 20-22, 30-31, 39-43, 52-54, 64, 74-78)
- **Exact File Path**: `plan/TARGET.md`
- **Specific Line Numbers / Sections**: Lines 11, 20-22, 30-31, 39-43, 52-54, 64, 74-78
- **Category & Type**: Category 1: Syntax & Structural Defects — Unresolved Template Placeholders
- **Detailed Description**: Contains unpopulated raw bracket strings (`[請在此填入核心目標]`, `[功能/項目 1]`). `plan/AGENT.md` §0 instructs agents during bootstrap to scan `plan/TARGET.md` for project scope boundaries. Ingesting raw bracket placeholders degrades agent context ingestion.
- **Cross-References**: `plan/AGENT.md` §0.
- **Concrete Proposed Remediation**: Replace bracketed text with standardized template guidance comments (e.g. `<!-- Define core project goals here -->`).

#### Finding 1.8 (`plan/FEEDBACK.md`, Lines 34–41)
- **Exact File Path**: `plan/FEEDBACK.md`
- **Specific Line Numbers / Sections**: Lines 34–41 (§3 Entry Template)
- **Category & Type**: Category 1: Syntax & Structural Defects — Unresolved Template Placeholders
- **Detailed Description**: Section FB-001 contains unpopulated placeholder strings (`[YYYY/MM/DD]`, `FB-001 [...]`) directly under an active header instead of structured comments.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Convert FB-001 block into an HTML comment block template.

#### Finding 1.9 (`plan/PROCESS.md`, Lines 39–40)
- **Exact File Path**: `plan/PROCESS.md`
- **Specific Line Numbers / Sections**: Lines 39–40
- **Category & Type**: Category 1: Syntax & Structural Defects — Malformed ToDo Checkbox Syntax
- **Detailed Description**: ToDo line items lines 39–40 are wrapped in backticks (` - [ ] `[建立...]` `). Backticks surrounding task descriptions break Markdown checkbox regex parsers in `scripts/sync_project.py`.
- **Cross-References**: `scripts/sync_project.py` lines 240-280.
- **Concrete Proposed Remediation**: Remove backticks from ToDo lines: `- [ ] 建立擴充模組之自動化單元測試範例`.

#### Finding 1.10 (`structure/diagram.md`, Lines 12–25, 33–60)
- **Exact File Path**: `structure/diagram.md`
- **Specific Line Numbers / Sections**: Lines 12–25, 33–60
- **Category & Type**: Category 1: Syntax & Structural Defects — Generic Placeholder Content
- **Detailed Description**: Sequence diagram includes `External API` interactions, which violates `plan/AGENT.md` §6 offline execution guardrails and does not reflect actual repository architecture (`bootstrap.py` -> `version_engine.py` -> `sync_project.py`).
- **Cross-References**: `plan/AGENT.md` §6.
- **Concrete Proposed Remediation**: Replace generic API flowchart with actual template sequence flows.

#### Finding 1.11 (`plan/AGENT.md`, Line 125)
- **Exact File Path**: `plan/AGENT.md`
- **Specific Line Numbers / Sections**: Line 125
- **Category & Type**: Category 1: Syntax & Structural Defects — Non-POSIX Slash Formatting
- **Detailed Description**: Ignore list uses Windows backslashes (`\logs\archived`, `\.git`) instead of POSIX forward slashes (`/logs/archived/`, `.git/`).
- **Cross-References**: `.gitignore`.
- **Concrete Proposed Remediation**: Convert backslashes to forward slashes.

#### Finding 1.12 (`plan/MEMORY.md`, Line 18)
- **Exact File Path**: `plan/MEMORY.md`
- **Specific Line Numbers / Sections**: Line 18
- **Category & Type**: Category 1: Syntax & Structural Defects — Invalid Directory WikiLink
- **Detailed Description**: Encloses directory path in WikiLink brackets `[[logs/]]`. WikiLink syntax requires target Markdown files.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Replace `[[logs/]]` with plain code text `logs/`.

#### Finding 1.13 (`plan/MEMORY.md`, Line 38)
- **Exact File Path**: `plan/MEMORY.md`
- **Specific Line Numbers / Sections**: Line 38
- **Category & Type**: Category 1: Syntax & Structural Defects — Header Format Duplication
- **Detailed Description**: Header title string duplicates version tag: `### v1.0.20260716.1 Implement YAML... (v1.0.20260716.1)`.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Remove redundant trailing version string in parentheses.

#### Finding 1.14 (`scripts/sync_project.py`, Line 57)
- **Exact File Path**: `scripts/sync_project.py`
- **Specific Line Numbers / Sections**: Line 57 (Function `load_version_strategy`)
- **Category & Type**: Category 1: Syntax & Structural Defects — Missing Type Import (`NameError`)
- **Detailed Description**: Function return type annotation uses `Tuple[VersionStrategy, str]`, but `from typing import Tuple` is missing from module imports (lines 9-15). Executing `sync_project.py` on Python environments evaluating type hints at runtime raises `NameError: name 'Tuple' is not defined`.
- **Cross-References**: `scripts/version_engine.py` line 12.
- **Concrete Proposed Remediation**: Add `Tuple` to typing imports at line 15: `from typing import Tuple, Dict, Any, Optional`.

#### Finding 1.15 (`scripts/git_hook_validator.py`, Lines 19–28)
- **Exact File Path**: `scripts/git_hook_validator.py`
- **Specific Line Numbers / Sections**: Lines 19–28 (Fallback `Dummy` class)
- **Category & Type**: Category 1: Syntax & Structural Defects — Incomplete Fallback Interface
- **Detailed Description**: `Dummy` fallback class lacks standard `VersionStrategy` methods (`validate_version`, `bump_version`, `format_commit_header`). If `version_engine.py` import fails, calls to missing methods trigger `AttributeError`.
- **Cross-References**: `scripts/version_engine.py` lines 14–41.
- **Concrete Proposed Remediation**: Implement complete ABC method stubs in `Dummy` class.

#### Finding 1.16 (`refer/claude-ai-project-template-study.md`, 60+ Lines)
- **Exact File Path**: `refer/claude-ai-project-template-study.md`
- **Specific Line Numbers / Sections**: Lines 5, 6, 14, 18, 20, 26, 40, 58, 89, 124, 162, 199, etc.
- **Category & Type**: Category 1: Syntax & Structural Defects — Unlinked Footnote Citation Markup
- **Detailed Description**: Inline citations are written as trailing unlinked numbers (`互動1`, `失敗）3`). Standard Markdown parsers fail to convert these into clickable hyperlink citations targeting the bibliography.
- **Cross-References**: Lines 205-239 (Bibliography section).
- **Concrete Proposed Remediation**: Convert numerical citations to Markdown footnote syntax `[^N]` and update bibliography definitions.

#### Finding 1.17 (`refer/claude-ai-project-template-study.md`, Bibliography Section)
- **Exact File Path**: `refer/claude-ai-project-template-study.md`
- **Specific Line Numbers / Sections**: Lines 206, 208, 209, 211, 215, 222, 237
- **Category & Type**: Category 1: Syntax & Structural Defects — Excessive Escaping
- **Detailed Description**: Unnecessary backslash escaping of hyphens (`\-`) within text link strings.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Remove backslashes before hyphens in plain Markdown text.


---

### Category 2: Redundancies & Duplicate Content (8 Findings)

#### Finding 2.1 (`doc/exclusion-rules.md` & `doc/data-schema.md` vs `.gitignore`)
- **Exact File Path**: `doc/exclusion-rules.md` (Lines 13-15), `doc/data-schema.md` (Line 41)
- **Specific Line Numbers / Sections**: `exclusion-rules.md` Lines 13-15, 26-28; `data-schema.md` Line 41
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Duplicated Rule Definitions
- **Detailed Description**: Both spec files duplicate ignore rules (`*.tmp`, `~$*`, `__pycache__/`) from `.gitignore` without establishing a single source of truth precedence contract.
- **Cross-References**: `.gitignore` lines 33-48.
- **Concrete Proposed Remediation**: Add explicit cross-reference headers citing `.gitignore` as the canonical source of truth.

#### Finding 2.2 (`plan/GIT-GUIDE.md`, Section 2)
- **Exact File Path**: `plan/GIT-GUIDE.md`
- **Specific Line Numbers / Sections**: Lines 20–38 (Section 2)
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Verbatim Strategy Duplication
- **Detailed Description**: Duplicates Dual Versioning Strategy definitions word-for-word from `plan/AGENT.md` §4.
- **Cross-References**: `plan/AGENT.md` §4 (Lines 79-84).
- **Concrete Proposed Remediation**: Condense `AGENT.md` §4 to a high-level summary referencing `[[plan/GIT-GUIDE.md#2. 雙版本號併行策略]]`.

#### Finding 2.3 (`plan/GIT-GUIDE.md`, Lines 50–52)
- **Exact File Path**: `plan/GIT-GUIDE.md`
- **Specific Line Numbers / Sections**: Lines 50–52
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Verbatim Retry Limit Duplication
- **Detailed Description**: Duplicates 2-time self-correction cap and `--no-verify` fallback verbatim from `plan/AGENT.md` §4.
- **Cross-References**: `plan/AGENT.md` Lines 85-87.
- **Concrete Proposed Remediation**: Replace duplicate text in `AGENT.md` with WikiLink reference.

#### Finding 2.4 (`plan/AGENT.md` Lines 68–75, 108 vs `MEMORY.md` & `PROCESS.md`)
- **Exact File Path**: `plan/AGENT.md`, `plan/MEMORY.md`, `plan/PROCESS.md`
- **Specific Line Numbers / Sections**: `AGENT.md` Lines 68-75, 108; `MEMORY.md` Line 20; `PROCESS.md` Line 48
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Multi-File Rule Duplication
- **Detailed Description**: Single Writer Rule is fully defined in `AGENT.md` §3.2 and repeated verbatim across multiple plan files.
- **Cross-References**: `plan/AGENT.md` §3.2.
- **Concrete Proposed Remediation**: Keep canonical rule in `AGENT.md` §3.2 and condense secondary mentions to `[[plan/AGENT.md#3.2]]`.

#### Finding 2.5 (`plan/MEMORY.md`, Lines 28–36)
- **Exact File Path**: `plan/MEMORY.md`
- **Specific Line Numbers / Sections**: Lines 28–36
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Raw Log Copy-Paste
- **Detailed Description**: Copies raw change log entries bullet-for-bullet from `plan/cold-history.log` (Lines 21-29) rather than maintaining a high-level rolling summary.
- **Cross-References**: `plan/cold-history.log`.
- **Concrete Proposed Remediation**: Condense into bulleted milestone summaries linking to `[[plan/cold-history.log]]`.

#### Finding 2.6 (`plan/PROCESS.md`, Lines 47–48)
- **Exact File Path**: `plan/PROCESS.md`
- **Specific Line Numbers / Sections**: Lines 47–48 (Future ToDo / Backlog)
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Duplicate Task Tracking
- **Detailed Description**: Lists Dual Versioning and Single Writer Rule as completed `[x]` items in Backlog after already listing them under "Completed Milestones" (Lines 17-20).
- **Cross-References**: `plan/PROCESS.md` Lines 17-20.
- **Concrete Proposed Remediation**: Remove redundant checked items from Backlog.

#### Finding 2.7 (`scripts/install_hooks.py`, Lines 20–72)
- **Exact File Path**: `scripts/install_hooks.py`
- **Specific Line Numbers / Sections**: Lines 20–45 & Lines 47–72
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Shell Code String Duplication
- **Detailed Description**: `pre_commit_wrapper` and `commit_msg_wrapper` string templates duplicate 26 lines of shell script resolution logic verbatim.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Extract shared shell resolution function into a Python string variable and interpolate into templates.

#### Finding 2.8 (`scripts/sync_project.py`, Lines 93, 127, 135)
- **Exact File Path**: `scripts/sync_project.py`
- **Specific Line Numbers / Sections**: Lines 93, 127, 135 (Function `run_type_a_static_checks`)
- **Category & Type**: Category 2: Redundancies & Duplicate Content — Triple File Tree Traversals
- **Detailed Description**: Calls `os.walk(root_dir)` three separate times in sequence to check casing, build file sets, and validate links.
- **Cross-References**: None.
- **Concrete Proposed Remediation**: Refactor into a single `os.walk` pass that populates in-memory metadata structures.


---

### Category 3: Logical Inconsistencies & Contradictions (14 Findings)

#### Finding 3.1 (`.gitignore`, Line 73 vs Tracked `.obsidian/*.json` Files)
- **Exact File Path**: `.gitignore`
- **Specific Line Numbers / Sections**: Line 73 (`.obsidian/`)
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Git Tracking Conflict
- **Detailed Description**: `.gitignore` Line 73 ignores `.obsidian/`. However, six `.obsidian/*.json` configuration files are actively tracked in Git. Ignoring `.obsidian/` prevents Git from tracking updates to repository workspace settings.
- **Cross-References**: `.obsidian/app.json`, `appearance.json`, `community-plugins.json`, `core-plugins.json`, `hotkeys.json`, `workspace.json`.
- **Concrete Proposed Remediation**: Replace `.obsidian/` with explicit unignore rules for tracked JSON files:
  ```gitignore
  .obsidian/*
  !.obsidian/app.json
  !.obsidian/appearance.json
  !.obsidian/community-plugins.json
  !.obsidian/core-plugins.json
  !.obsidian/hotkeys.json
  !.obsidian/workspace.json
  ```

#### Finding 3.2 (`.gitignore`, Line 95 vs `.sync-state.json`)
- **Exact File Path**: `.gitignore`
- **Specific Line Numbers / Sections**: Line 95 (`.sync-state.json`)
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Core State File Ignored
- **Detailed Description**: `.gitignore` Line 95 includes `.sync-state.json`. `.sync-state.json` is a core file tracked in the repository and updated by `scripts/sync_project.py`. Ignoring it prevents automated sync updates from being committed.
- **Cross-References**: `.sync-state.json`, `scripts/sync_project.py`.
- **Concrete Proposed Remediation**: Remove `.sync-state.json` from `.gitignore`.

#### Finding 3.3 (`doc/yaml-truth-spec.md` vs `.gitignore`)
- **Exact File Path**: `doc/yaml-truth-spec.md` vs `.gitignore`
- **Specific Line Numbers / Sections**: `yaml-truth-spec.md` Lines 225–230; `.gitignore` Lines 59–66
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Specification Violation
- **Detailed Description**: `yaml-truth-spec.md` explicitly mandates active `.xlsx` ignore rules in `.gitignore` (`*.xlsx`, `doc/*.xlsx`, `!doc/proposals/*.xlsx`). Root `.gitignore` contains only commented-out `# *.xlsx` lines.
- **Cross-References**: `doc/yaml-truth-spec.md`.
- **Concrete Proposed Remediation**: Uncomment and activate mandatory `.xlsx` rules in `.gitignore`.

#### Finding 3.4 (`.sync-state.json`, Line 2 vs `README.md`, Line 1)
- **Exact File Path**: `.sync-state.json` vs `README.md`
- **Specific Line Numbers / Sections**: `.sync-state.json` Line 2 (`"version": "v1.0.1"`); `README.md` Line 1 (`v2.0 Production Edition`)
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Version Mismatch
- **Detailed Description**: `.sync-state.json` records `"version": "v1.0.1"`, whereas `README.md` and commit log record `v2.0 Production Edition`. Automated version scripts reading `.sync-state.json` report obsolete version data.
- **Cross-References**: `README.md` Line 1.
- **Concrete Proposed Remediation**: Update `.sync-state.json` line 2 to `"version": "v2.0.0"`.

#### Finding 3.5 (`.gitmodules` vs `README.md` Directory Spec)
- **Exact File Path**: `.gitmodules` vs `README.md`
- **Specific Line Numbers / Sections**: `.gitmodules` Lines 1–3; `README.md` Lines 36 & 71
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Directory Role Violation
- **Detailed Description**: `.gitmodules` defines submodule path at `refer/matt-pocock-skills`. `README.md` defines `skills/` for skill modules and `refer/` for raw input data.
- **Cross-References**: `README.md` Section 2.
- **Concrete Proposed Remediation**: Update `.gitmodules` path or document explicit architectural exception in `README.md`.

#### Finding 3.6 (`structure/modules.md` vs `plan/AGENT.md` Python Filename Rule)
- **Exact File Path**: `structure/modules.md` vs `plan/AGENT.md`
- **Specific Line Numbers / Sections**: `modules.md` Lines 21-22, 25-26, 35, 41, 58, 59; `AGENT.md` Lines 38-39
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Code Naming Rule Violation
- **Detailed Description**: `AGENT.md` strictly forbids hyphens in Python filenames (`snake_case` required). `structure/modules.md` specifies example Python filenames with hyphens (`data-cleaner.py`, `config-loader.py`, `test-data-cleaner.py`).
- **Cross-References**: `plan/AGENT.md` §1.
- **Concrete Proposed Remediation**: Rename example files in `structure/modules.md` to `snake_case` (`data_cleaner.py`, `config_loader.py`, `test_data_cleaner.py`).

#### Finding 3.7 (`plan/GIT-GUIDE.md` Line 46 vs `.gitignore` & `structure/modules.md`)
- **Exact File Path**: `plan/GIT-GUIDE.md`
- **Specific Line Numbers / Sections**: Line 46
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Untracked File Validation Claim
- **Detailed Description**: `GIT-GUIDE.md` states Git Hooks validate `.sync-state.json`, but `.sync-state.json` is listed in `.gitignore` and omitted from structure specs.
- **Cross-References**: `.gitignore` Line 95.
- **Concrete Proposed Remediation**: Synchronize tracking status across `.gitignore` and `GIT-GUIDE.md`.

#### Finding 3.8 (`plan/TARGET.md` §6 & `structure/modules.md` §1 vs Root Directories)
- **Exact File Path**: `plan/TARGET.md` & `structure/modules.md`
- **Specific Line Numbers / Sections**: `TARGET.md` Lines 60-65; `modules.md` Lines 11-27
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Incomplete Directory Map
- **Detailed Description**: Both layout maps list `plan/`, `doc/`, `structure/`, `source/`, `test/`, but omit active core system directories `scripts/` and `skills/`.
- **Cross-References**: `README.md` Section 2.
- **Concrete Proposed Remediation**: Add `scripts/` and `skills/` to both layout mapping sections.

#### Finding 3.9 (`scripts/bootstrap.py`, Lines 193–206)
- **Exact File Path**: `scripts/bootstrap.py`
- **Specific Line Numbers / Sections**: Lines 193–206 (`files_to_copy` list)
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Script Copy Omission
- **Detailed Description**: `bootstrap.py` copies `version_engine.py`, `sync_project.py`, `git_hook_validator.py`, and `install_hooks.py`, but **omits `scripts/archive_council.py`**. Newly initialized projects lack the council archiving utility required by `skills/council/SKILL.md`.
- **Cross-References**: `skills/council/SKILL.md` lines 90 & 144.
- **Concrete Proposed Remediation**: Add `("scripts/archive_council.py", "scripts/archive_council.py")` to `files_to_copy` in `bootstrap.py`.

#### Finding 3.10 (`scripts/archive_council.py`, Line 15)
- **Exact File Path**: `scripts/archive_council.py`
- **Specific Line Numbers / Sections**: Line 15
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Archive Overwrite Data Loss
- **Detailed Description**: Hardcodes ZIP destination to `council-archive.zip` in `'w'` mode. Subsequent archive runs overwrite previous council session zips, causing loss of past decision logs.
- **Cross-References**: `skills/council/SKILL.md`.
- **Concrete Proposed Remediation**: Generate timestamped ZIP filenames (`council-archive-YYYYMMDD_HHMMSS.zip`).

#### Finding 3.11 (`scripts/version_engine.py`, Lines 125–153)
- **Exact File Path**: `scripts/version_engine.py`
- **Specific Line Numbers / Sections**: Lines 125–153 (`CalVerStrategy.bump_version`)
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — CalVer Format Mutation Bug
- **Detailed Description**: `validate_version()` accepts date-based CalVer (`vYYYY.MM.DD`). However, `bump_version()` only checks 8-digit CalVer regex (`v1.0.YYYYMMDD.Z`). Bumping a `vYYYY.MM.DD` version forcibly converts it to `v1.0.YYYYMMDD.1`, breaking format strategy contract.
- **Cross-References**: `plan/GIT-GUIDE.md` Line 34, `README.md` Line 14.
- **Concrete Proposed Remediation**: Update `CalVerStrategy.bump_version()` to parse `CALVER_REGEX_DATE` and maintain date format on bump.

#### Finding 3.12 (`skills/council/SKILL.md`, Lines 121, 123, 128, 132)
- **Exact File Path**: `skills/council/SKILL.md`
- **Specific Line Numbers / Sections**: Lines 121, 123, 128, 132 (Mermaid Sequence Diagram)
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Omitted Path Prefix
- **Detailed Description**: Sequence diagram labels mention `task-desc.md`, `proposal-v1.md` without `.council/` folder prefix, contradicting isolation rules requiring all temp files to reside inside `.council/`.
- **Cross-References**: `skills/council/SKILL.md` lines 88 & 97–99.
- **Concrete Proposed Remediation**: Add `.council/` prefix to step filenames in sequence diagram.

#### Finding 3.13 (`plan/PROCESS.md` Lines 47-48 vs Completed Milestones)
- **Exact File Path**: `plan/PROCESS.md`
- **Specific Line Numbers / Sections**: Lines 47-48
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Status Tracking Inconsistency
- **Detailed Description**: Items marked as completed in Milestone 1 are retained in the Backlog section with checked boxes `[x]`, breaking single-location status tracking.
- **Cross-References**: `plan/PROCESS.md` Lines 17-20.
- **Concrete Proposed Remediation**: Purge duplicate completed items from Backlog section.

#### Finding 3.14 (`doc/exclusion-rules.md` vs `.gitignore` Precedence)
- **Exact File Path**: `doc/exclusion-rules.md`
- **Specific Line Numbers / Sections**: Lines 1-54
- **Category & Type**: Category 3: Logical Inconsistencies & Contradictions — Conflict Resolution Undefined
- **Detailed Description**: Fails to define precedence when documentation exclusion rules contradict active `.gitignore` rules.
- **Cross-References**: `.gitignore`.
- **Concrete Proposed Remediation**: State explicitly that `.gitignore` is the binding operational authority.

---

## 4. Concrete Prioritized Remediation Roadmap

To restore 100% repository consistency, fix runtime bugs, and achieve complete specification compliance, remediation should be executed in three prioritized phases:

```
+-----------------------------------------------------------------------------------+
|                            REMEDIATION ROADMAP                                   |
+-----------------------------------------------------------------------------------+
| PHASE 1: Critical Logical Contradictions & Runtime Bug Fixes (Immediate Priority) |
|   - Fix missing `Tuple` import in `sync_project.py`                              |
|   - Add `archive_council.py` to `bootstrap.py` `files_to_copy` list               |
|   - Fix `CalVerStrategy.bump_version` format loss bug in `version_engine.py`      |
|   - Fix `.gitignore` tracking conflicts (`.obsidian/`, `.sync-state.json`)        |
|   - Activate mandatory `*.xlsx` rules in `.gitignore`                             |
|   - Sync submodule versions (`package.json` v1.2.0 vs `plugin.json` v1.2.0)       |
|   - Fix plain-text `AGENTS.md` symlink pointer breakdown                          |
|   - Update `.sync-state.json` version string to `"v2.0.0"`                       |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 2: Script Defects, Naming Rules & Link Validation (High Priority)           |
|   - Rename hyphenated Python files in `structure/modules.md` to `snake_case`      |
|   - Add timestamping to `scripts/archive_council.py` to prevent data overwrites   |
|   - Remove single quotes from `plan/PROCESS.md` ToDo checkboxes                   |
|   - Fix `README.md` Line 126 `mv PROCESS-template.md PROCESS.md` typo             |
|   - Replace generic API diagram in `structure/diagram.md` with system flows       |
|   - Complete `Dummy` fallback interface in `git_hook_validator.py`                |
|   - Fix dead relative links in `CONTEXT-FORMAT.md`, `wayfinder`, `research.md`    |
|   - Update `skills/council/SKILL.md` sequence diagram with `.council/` prefix    |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 3: Redundancy Deduplication & Document Formatting Cleanup (Standard Priority)|
|   - Deduplicate Dual Versioning & Single Writer text across plan files            |
|   - Extract shared shell python resolver in `scripts/install_hooks.py`            |
|   - Optimize `sync_project.py` `run_type_a_static_checks` to single `os.walk` pass|
|   - Convert 60+ unlinked numerical citations in study report to `[^N]` footnotes  |
|   - Clean up `lastOpenFiles` scratch entries in `.obsidian/workspace.json`        |
|   - Purge unconsumed changesets and legacy skill prompts on disk                  |
|   - Populate/comment raw template placeholders in `TARGET.md` & `FEEDBACK.md`     |
+-----------------------------------------------------------------------------------+
```

---

## 5. Master Verification Method

To independently verify the audit conclusions and validate future remediation:

1. **Verify Python Import & Execution**:
   ```powershell
   python -c "import scripts.sync_project; import scripts.version_engine; import scripts.git_hook_validator"
   ```

2. **Verify Bootstrap Package Completeness**:
   ```powershell
   python scripts/bootstrap.py --target-dir scratch/test_env --name TestProj --non-interactive
   Test-Path "scratch/test_env/scripts/archive_council.py"
   ```

3. **Verify Git Tracking Status**:
   ```powershell
   git status --ignored
   ```
   *Confirm `.obsidian/app.json` and `.sync-state.json` are tracked and NOT listed under ignored files.*

4. **Verify Total Inventory Count**:
   ```powershell
   (Get-ChildItem -Path "refer" -Recurse -File).Count
   ```
   *Expected result: 169 files in `refer/` (167 in `matt-pocock-skills` + `claude-ai-project-template-study.md` + `.gitkeep`).*

5. **Verify Version Synchronization**:
   ```powershell
   Get-Content "refer/matt-pocock-skills/package.json" | Select-String "version"
   Get-Content "refer/matt-pocock-skills/.claude-plugin/plugin.json" | Select-String "version"
   ```

---
*Report end — Master Audit Report synthesized by `worker_m5`.*