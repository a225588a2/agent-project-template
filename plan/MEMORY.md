# 專案執行紀錄與決策歷史 (Hot Memory)

本文件僅記錄專案的「熱記憶 (Hot Memory)」，包含專案滾動式摘要 (Rolling Summary) 以及最近 3~5 筆重大變更的索引摘要。
詳細的歷史變更日誌與細節已物理分離至 `logs/cold-history.log`，供 Agent 使用 `grep_search` 等工具檢索，免除 RAG 複雜度，且杜絕 HTML 註記標籤遭毀損的風險。

---

## 📌 專案滾動式摘要 (Rolling Summary)

- **當前核心目標**：搭建具備漸進式揭露、安全性防禦與極簡化架構的 AI 專案模板。
- **當前系統架構關鍵決策**：
  - 專案配置與初始化工具 (`bootstrap.py`) 全面採用內建 JSON 格式，廢除脆弱的 TOML/YAML 自研解析。
  - 議會交接暫存文件儲存於 `.council/`，自動化結案歸檔清理，僅保留最終 `doc/proposals/COUNCIL_DECISION.md`。
  - 狀態同步工具 `sync-project.py` 採用單一 JSON/YAML 檔案，取消 SQLite 與雙重狀態，解析失敗直接報錯拋出 Traceback 觸發 Self-Correction。
  - 記憶系統採用物理分離（熱記憶 `plan/MEMORY.md` 與冷記憶 `logs/cold-history.log`），以 grep 代替 RAG。
  - 議會流程二次優化，正式納入專職「唯讀」的 Researcher 角色與 Phase 0 調研先行流程，實施「連網不讀檔，讀檔不連網」的雙重沙箱防護。
- **下一步執行重點**：實作 JSON 限制的 `bootstrap.py` 與 strict parsing & 單一 JSON/YAML 狀態的 `sync-project.py`。

---

## ⚡ 最近變更索引 (Recent Change Indexes - Last 3~5 Entries)

### v1.0.20260701.3 Add log version verification and transactional writing in sync-project.py (v1.0.20260701.3)
- **變更項目**：
  * 實作日誌宣告版本號與腳本計算版本的強一致性比對，若不合立即 exit(1)。
  * 調整 sync-project.py 將版本修改寫入延遲至驗證通過後執行，避免中斷時檔案遭受污染。

### v1.0.20260701.2 Support flexible task checkbox parsing in sync-project.py (v1.0.20260701.2)
- **變更項目**：
  * 引入正則表達式重構 sync-project.py 待辦判定。
  * 支援不同層級縮排、列表符號（-, *, +）與反引號括號（`[ ]`, `[/]`）樣式，並完美保留原始格式。

### v1.0.20260701.1 Implement project template automation scripts (v1.0.20260701.1)
- **變更項目**：
  * 實作 scripts/bootstrap.py，建立零依賴、參數驅動之初始化工具，並提供手動與腳本並存路徑。
  * 實作 scripts/sync-project.py，實現 ToDo 看板打勾、版本號遞增與熱記憶更新。
  * 文件並存優化，於 README.md、AGENT.md、COUNCIL.md 寫入對應工具鏈規範。

### 20260628-2 優化議會協作規範與記憶系統物理分離 (v20260628.2)
- **變更項目**：
  - 實施 Researcher 「連網不讀檔，讀檔不連網」雙重沙箱與簡報無害化。
  - 重申 HITL 原則，任何外網資訊生成的代碼指令須人類手動核准。
  - 廢除 SQLite 與寬鬆解析，改為單一 JSON 檔案狀態追蹤與 Strict Parsing。
  - 廢除 `MEMORY.md` 內嵌 HTML 註記與 RAG 檢索，物理分離為熱記憶 (`plan/MEMORY.md`) 與冷歷史日誌 (`logs/cold-history.log`)。
  - 議會交接臨時檔移入 `.council/` 並設定 `.gitignore`，結案時自動清理，只留 `doc/proposals/COUNCIL_DECISION.md`。
  - 限制 `bootstrap.py` 配置檔格式僅限內建 JSON 支援。

### 20260628-1 導入多 Agent 討論議會與看板式交接協議 (v20260628.1)
- **變更項目**：建立 `plan/COUNCIL.md`，定義主 Agent（協調者）、執行者（Executor）、批判者（Critic）三方流程。
