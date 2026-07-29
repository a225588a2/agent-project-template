# Original User Request

## Initial Request — 2026-07-28T13:32:58Z

Perform a comprehensive, file-by-file audit across all files in the AI project template (`c:\PersonalWS\AgentSandBox\AiProjectTemplate`), identifying errors, duplicate text, broken links, and logical contradictions, and generate a detailed remediation report.

Working directory: `c:\PersonalWS\AgentSandBox\AiProjectTemplate`
Integrity mode: development

## Requirements

### R1. Systematic File-by-File Inspection
Iterate through every document, configuration, guide, and script in the project workspace (including `README.md`, `doc/`, `plan/`, `structure/`, `skills/`, `scripts/`, `source/`, `test/`, `refer/`, etc.) to ensure complete coverage.

### R2. Three-Tier Defect Classification
Categorize all detected issues into three primary categories:
1. **Syntax & Structural Defects**: Syntax errors, broken internal file links, unresolved placeholder markers, or invalid schema references.
2. **Redundancies & Duplicate Content**: Repeated descriptions, overlapping rule statements, or redundant instructions across different files.
3. **Logical Inconsistencies & Contradictions**: Conflicting guidance between specifications (e.g. `doc/` vs `plan/` or `structure/`), contradictory workflow instructions, or mismatching interface definitions.

### R3. Comprehensive Audit Report Output
Produce a complete markdown audit report saved in `audit_report.md` within the working directory. The report must contain:
- Summary of audit scope and overall status.
- Detailed list of issues grouped by file path, featuring exact line numbers/sections, defect type, description, and concrete proposed fixes.

## Acceptance Criteria

### Coverage & Completeness
- [ ] 100% of non-git files in the repository are explicitly listed and audited in `audit_report.md`.
- [ ] Every directory (`doc/`, `plan/`, `structure/`, `skills/`, `scripts/`, etc.) is covered.

### Accuracy & Quality
- [ ] All reported issues cite precise file paths and specific line numbers/sections.
- [ ] Duplicate text blocks across files are identified with cross-references.
- [ ] Conflicting logic between specification files (e.g. `yaml-truth-spec.md` vs `data-schema.md` or `plan/PROCESS.md`) is clearly explained.
- [ ] Proposed resolutions are concrete and ready for execution.
