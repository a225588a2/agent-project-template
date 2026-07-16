# Council Decision: YAML as Single Source of Truth for Structured Data

**Status**: Consensus Approved (Review Passed)  
**Date**: 2026-07-16  
**Participants**:
- Consensus Coordinator (Lead Agent)
- Proposal Executor (`council_executor`)
- Devil's Advocate Critic (`council_critic`)

---

## 1. Context and Objective
In projects managing complex structural metadata (e.g., register maps, packet definitions), duplicating specifications across human-editable files (Excel), markdown documentation, and multiple source code header structures (C/Python) creates consistency drift ("split-brain" syndrome).

This decision details the design and security consensus for adopting a **YAML-as-Truth** architecture. The architecture enforces `spec.yaml` as the sole authoritative copy, from which all documentation and code structures are generated.

---

## 2. Technical Architecture & Security Consensus

The Council debated the security and operational risks of bidirectional spreadsheet editing (Excel ◄► YAML) and approved the following technical safety mechanisms:

1. **Fingerprint Lock (Conflict Check)**:
   - To prevent overwriting updates made in Git, the `export-excel` tool writes the SHA-256 hash of `spec.yaml` into a hidden sheet `_metadata`.
   - On `import-excel`, the tool calculates the local `spec.yaml` hash and compares it with the sheet. If they differ, the import is aborted.
   
2. **Formula Injection Shield**:
   - The excel importer inspects cell string values. Any cell string starting with `=`, `+`, `-`, or `@` triggers a Fail-Safe abort to block Excel formula execution or XSS injection during generation.

3. **Comment Preservation (`ruamel.yaml`)**:
   - Standard PyYAML strips developer comments. We mandate using `ruamel.yaml` in Round-Trip mode (`typ='rt'`) to preserve exact formatting, comments, and empty lines when writing back to YAML.

4. **Explicit Relational Linkage**:
   - Flattened Excel sheets explicitly associate every field row with its parent register through a `Parent Register` foreign-key column. Sorting rows in Excel does not corrupt relational hierarchies.

5. **Local Excel Isolation**:
   - Excel templates are strictly local untracked files. `*.xlsx` and `doc/*.xlsx` must be added to the project's `.gitignore`.

---

## 3. Implemented Components
The following files are added/modified:
- **[NEW] [yaml-truth-spec.md](file:///c:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/yaml-truth-spec.md)**: Main architecture specification and conversion template.
- **[MODIFY] [PROCESS.md](file:///c:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/PROCESS.md)**: Registered the task.

---

## 4. Key Critic Audits Resolved
- **Safe Loader Enforcement**: Mandated YAML 1.2 mode and safe loader initialization to block arbitrary python object instantiation (RCE defense).
- **Norwegian Option Bypass**: Enforced string matching regex on fields to prevent words like `ON`/`OFF` from being coerced into booleans in YAML 1.1 parsers.
- **Source Code Keyword Collision**: Mandated check against compiler keyword blacklists (e.g., `register`, `volatile`), adding suffixes (`_val`) and warnings when names collide.
