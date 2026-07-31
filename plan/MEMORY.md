# 專案執行紀錄與決策歷史 (Hot Memory)

本文件僅記錄專案的「熱記憶 (Hot Memory)」，包含專案滾動式摘要 (Rolling Summary) 以及最近 3~5 筆重大變更的索引摘要。
詳細的歷史變更日誌與細節已物理分離至 [[plan/cold-history.log]]，供 Agent 使用 `grep_search` 等工具檢索，免除 RAG 複雜度，且杜絕 HTML 註記標籤遭毀損的風險。

---

## 📌 專案滾動式摘要 (Rolling Summary)

- **當前核心目標**：搭建具備漸進式揭露、安全性防禦與極簡化架構的 AI 專案模板。
- **當前系統架構關鍵決策**：
  - 全面升級 AI 專案模板至 v2.0 Production Edition。
  - 建立 **Skill 庫架構 ([[skills/]] 目錄)**，並將議會機制徹底 Skill 化 ([[skills/council/SKILL.md]])。
  - 導入 **「雙軌版本模式 (Dual Versioning Strategy)」**：模式 A (SemVer 2.0: `vMAJOR.MINOR.PATCH` + Conventional Commits + Gitflow) 與 模式 B (CalVer: `vYYYY.MM.DD` / `v1.0.YYYYMMDD.Z`)。
  - 新增獨立 [[scripts/version_engine.py]] 模組採用策略模式解耦腳本邏輯。
  - 完全重寫 [[scripts/bootstrap.py]]，導入 **未選定機制清理規範 (Cleanup Rule)**，透過 HTML 條件標記完美切割雙軌版本與專案說明。
  - 升級開工協定為 **「兩階段漸進式啟動 (Two-Stage Bootstrap Protocol)」**，並確立「新專案初始化守則 (Agent Lazy Prompt 詢問)」。
  - 搬移冷歷史日誌至 [[plan/cold-history.log]]，讓 [[logs/]] 恢復為純選用暫存目錄。
  - 綜觀全局復原 [[README.md]] (造車公司比喻、目錄增減決策樹、Option A/B 啟動、Agent 一指 Prompt)。
  - 導入 **「單一寫入者原則 (Single Writer Rule)」** 限制 Sub-Agent 寫入權限，並實施 **「三維客觀 DoD 矩陣」**（Type A Markdown 檔名大小寫、內嵌 JSON/YAML/Mermaid 語法與禁止內部 `file:///` 連結校驗）。
  - Git Commit 規範修訂：Header 強制規範 (Conventional Commits / CalVer 前綴)，Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。

---

## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)

### v1.0.3 feat(bootstrap): dual versioning cleanup and agent guardrails
- **變更項目**：
  * 實作未選定機制清理規範 (Cleanup Rule)，於 [[plan/GIT-GUIDE.md]]、[[plan/AGENT.md]] 及 [[README.md]] 植入條件標記。
  * 重寫 [[scripts/bootstrap.py]] 實作條件標記渲染，徹底切割雙軌版本與專案說明的殘留。
  * 更新 [[README.md]] 新增 Agent 專用惰性啟動提示詞 (Lazy Prompt)。
  * 強化 Agent 新專案啟動護欄，強制於執行 bootstrap 前向使用者確認設定。
  * 確立 `main` 分支必須使用附註標籤 (Annotated Tag) 撰寫發布重點，與 `develop` 必須強制快進同步 (`--ff-only`) 的雙主線紀律。

### v1.0.0 feat(template): upgrade template to v2.0 Production Edition with Skill Library and Dual Versioning
- **變更項目**：
  * 全面升級 AI 專案模板至 v2.0 Production Edition。
  * 建立 [[skills/]] 技能庫架構，將 Council 徹底 Skill 化 ([[skills/council/SKILL.md]])。
  * 實作雙軌版本模式 (SemVer 2.0 vs CalVer) 與 [[scripts/version_engine.py]] 策略模式引擎。
  * 搬移 cold-history.log 至 [[plan/cold-history.log]]，讓 [[logs/]] 恢復為純選用目錄。
  * 綜觀全局復原 [[README.md]] (造車公司比喻、目錄決策樹、Option A/B 啟動、Agent 一指 Prompt)。
  * 嚴格禁止專案內部使用 file:/// 絕對路徑，全面強制採用 Obsidian Wiki Link [[FileName]]。
  * 升級 [[scripts/sync_project.py]] 與 [[scripts/git_hook_validator.py]] 靜態品質檢驗關卡。
  * 實作兩階段 Bootstrapping、Single Writer Rule 與 Git Author 簽名檢查。

### v1.0.20260716.1 Implement YAML as Single Source of Truth specification template (v1.0.20260716.1)
- **變更項目**：
  * Initiate Multi-Agent Council to debate and design the YAML-as-SSoT architecture.
  * Add [[doc/yaml-truth-spec-template.md]] as the main specification and conversion template.
  * Archive temporary .council/ workspace files to [[logs/archived/template-audit/]].
