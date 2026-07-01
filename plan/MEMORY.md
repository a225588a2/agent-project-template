# 專案執行紀錄與決策歷史 (Hot Memory)

本文件僅記錄專案的「熱記憶 (Hot Memory)」，包含專案滾動式摘要 (Rolling Summary) 以及最近 3~5 筆重大變更的索引摘要。
詳細的歷史變更日誌與細節已物理分離至 `logs/cold-history.log`，供 Agent 使用 `grep_search` 等工具檢索，免除 RAG 複雜度，且杜絕 HTML 註記標籤遭毀損的風險。

---

## 📌 專案滾動式摘要 (Rolling Summary)

- **當前核心目標**：搭建具備漸進式揭露、安全性防禦與極簡化架構的 AI 專案模板。
- **當前系統架構關鍵決策**：
  - 專案配置與初始化工具 (`bootstrap.py`) 全面採用內建 JSON 格式，廢除脆弱的 TOML/YAML 自研解析。
  - 議會交接暫存文件儲存於 `.council/`，自動化結案歸檔清理，僅保留最終 `doc/proposals/COUNCIL_DECISION.md`。
  - 狀態同步工具 `sync_project.py` 採用單一 JSON/YAML 檔案，取消 SQLite 與雙重狀態，解析失敗直接報錯拋出 Traceback 觸發 Self-Correction。
  - 記憶系統採用物理分離（熱記憶 `plan/MEMORY.md` 與冷記憶 `logs/cold-history.log`），以 grep 代替 RAG。
  - 議會流程二次優化，正式納入專職「唯讀」的 Researcher 角色與 Phase 0 調研先行流程，實施「連網不讀檔，讀檔不連網」的雙重沙箱防護。
- **下一步執行重點**：實作 JSON 限制的 `bootstrap.py` 與 strict parsing & 單一 JSON/YAML 狀態的 `sync_project.py`。

---

## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)

### v1.0.20260701.6 Add directory selection decision tree in AGENT.md (v1.0.20260701.6)
- **變更項目**：
  * 於 AGENT.md 新增「專案目錄增減決策樹」。
  * 提供明確且結構化的決策問題，指引 Agent 在專案初始化時，能快速與使用者核對並判斷選用目錄（source, test, scripts, refer）之必要性。

### v1.0.20260701.5 Soften code naming rules in AGENT.md (v1.0.20260701.5)
- **變更項目**：
  * 修改 AGENT.md，將程式碼命名原則由「強制 snake_case」調整為「依程式語言標準慣例建議命名」（例如 Python 使用 snake_case）。
  * 避免強加 snake_case 於其他有各自標準命名慣例之語言中（如 JS/TS 的 camelCase 等）。

### v1.0.20260701.4 Refine naming convention: docs kebab-case, code snake_case (v1.0.20260701.4)
- **變更項目**：
  * 更新 AGENT.md 命名規範，區分文件（kebab-case）與程式碼/腳本（snake_case）命名原則。
  * 將 scripts/sync-project.py 重新命名為 scripts/sync_project.py，並修正所有相關引用以防止 Python import 語法錯誤。

### v1.0.20260701.3 Add log version verification and transactional writing in sync_project.py (v1.0.20260701.3)
- **變更項目**：
  * 實作日誌宣告版本號與腳本計算版本的強一致性比對，若不合立即 exit(1)。
  * 調整 sync_project.py 將版本修改寫入延遲至驗證通過後執行，避免中斷時檔案遭受污染。

### v1.0.20260701.2 Support flexible task checkbox parsing in sync_project.py (v1.0.20260701.2)
- **變更項目**：
  * 引入正則表達式重構 sync_project.py 待辦判定。
  * 支援不同層級縮排、列表符號（-, *, +）與反引號括號（`[ ]`, `[/]`）樣式，並完美保留原始格式。
