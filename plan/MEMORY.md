# 專案執行紀錄與決策歷史 (Hot Memory)

本文件僅記錄專案的「熱記憶 (Hot Memory)」，包含專案滾動式摘要 (Rolling Summary) 以及最近 3~5 筆重大變更的索引摘要。
詳細的歷史變更日誌與細節已物理分離至 `logs/cold-history.log`，供 Agent 使用 `grep_search` 等工具檢索，免除 RAG 複雜度，且杜絕 HTML 註記標籤遭毀損的風險。

---

## 📌 專案滾動式摘要 (Rolling Summary)

- **當前核心目標**：搭建具備漸進式揭露、安全性防禦與極簡化架構的 AI 專案模板。
- **當前系統架構關鍵決策**：
  - 專案配置與初始化工具 (`bootstrap.py`) 全面採用內建 JSON 格式，廢除脆弱的 TOML/YAML 自研解析。
  - 議會交接暫存文件儲存於 `.council/`，自動化結案歸檔清理，僅保留最終 `doc/proposals/COUNCIL_DECISION.md` 與專案特定的 `doc/proposals/COUNCIL_DECISION_*.md`。
  - 狀態同步工具 `sync_project.py` 採用單一 JSON/YAML 檔案，取消 SQLite 與雙重狀態，解析失敗直接報錯拋出 Traceback 觸發 Self-Correction。
  - 記憶系統採用物理分離（熱記憶 `plan/MEMORY.md` 與冷記憶 `logs/cold-history.log`），以 grep 代替 RAG。
  - 議會流程二次優化，正式納入專職「唯讀」的 Researcher 角色與 Phase 0 調研先行流程，實施「連網不讀檔，讀檔不連網」的雙重沙箱防護。
  - 導入「YAML 作為唯一真理來源 (SSoT)」架構規範，支援低阻力雙向 Excel 同步，具備 Fingerprint 雜湊衝突防鎖、公式注入防禦與 `ruamel.yaml` 註釋保留讀寫。
- **下一步執行重點**：持續維護模板並將變更推送至遠端。

---

## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)

### v1.0.20260716.1 Implement YAML as Single Source of Truth specification template (v1.0.20260716.1)
- **變更項目**：
  * Initiate Multi-Agent Council to debate and design the YAML-as-SSoT architecture.
  * Add doc/yaml-truth-spec.md as the main specification and conversion template.
  * Add doc/proposals/COUNCIL_DECISION_YAML.md to document the council decision and safety controls.
  * Archive and clean up the temporary .council/ workspace files to logs/archived/council-archive.zip.

### v1.0.20260716.1 Implement YAML as Single Source of Truth specification template (v1.0.20260716.1)
- **變更項目**：
  * Initiate Multi-Agent Council to debate and design the YAML-as-SSoT architecture.
  * Add doc/yaml-truth-spec.md as the main specification and conversion template.
  * Add doc/proposals/COUNCIL_DECISION_YAML.md to document the council decision and safety controls.
  * Archive and clean up the temporary .council/ workspace files to logs/archived/council-archive.zip.

### v1.0.20260707.2 Update project documentation to describe the Git Hook validation mechanism (v1.0.20260707.2)
- **變更項目**：
  * Update README.md to describe Git Commit Validation Hooks, CJK filter, and manual setup step.
  * Update plan/AGENT.md to include Git Hook validation in commit guidelines and task completion checklist.
  * Update plan/GIT-GUIDE.md to introduce a dedicated section explaining hook checks and validation rules.

### v1.0.20260707.1 Introduce Git Hook mechanism for commit check validation (v1.0.20260707.1)
- **變更項目**：
  * Implement scripts/git_hook_validator.py for commit format, CJK filter, and project version check.
  * Implement scripts/install_hooks.py to setup CWD-independent and alias-safe hook wrappers.
  * Integrate hook installation into scripts/bootstrap.py.
  * Refactor scripts/sync_project.py to remove redundant git check warnings and add log diagnostics.
  * Write final design consensus to doc/proposals/COUNCIL_DECISION.md.

### v1.0.20260701.7 Update directory definitions and clean up obsolete checklists in AGENT.md (v1.0.20260701.7)
- **變更項目**：
  * 於 AGENT.md 新增 4 個核心目錄的職責定義，並說明規則需隨物理目錄現況進行增補與動態更新。
  * 清理 AGENT.md 護欄與 DoD 完成條件中殘存的舊版 MEMORY.md 手動同步描述，統一對齊為 sync_project.py 自動化工作流。
