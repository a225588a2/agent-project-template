# Agent 工作與執行規範 (Agent Guidelines) - v2.0 Production Edition

本文件定義了參與本專案的開發人員或 AI Agent 應遵循的核心規範，以確保專案的結構完整性、歷史可追溯性與高品質產出。

> [!IMPORTANT]
> **🌟 最高指導原則 (Supreme Directive)：「先思考，再提問討論，再執行」**
> 在執行任何非瑣碎 (Non-trivial)、具有風險或涉及結構/架構變更的操作前，Agent 必須先思考其後果與潛在影響。若對需求、技術選型或範疇存在任何模糊或疑慮，應優先主動與使用者提問討論，在雙方確認無誤後方能開始執行。

---

## 0. 會話啟動協定 (Session Bootstrap Protocol - Two-Stage)

AI Agent 每次開啟新對話時屬於無狀態起點。為防範 Context 膨脹與記憶失憶，實施 **「兩階段漸進式啟動 (Two-Stage Bootstrap Protocol)」**：

1. **Stage 1 (熱記憶載入 - Hot Memory Load)**：
   - 優先讀取 **[[plan/MEMORY.md]]**（約 1.5k Token），快速掌握當前專案滾動摘要與最近 3~5 筆變更。
2. **Stage 2 (邊界、護欄與 Skill 掃描 - Header & Skill Scan)**：
   - 掃描 **[[plan/TARGET.md]]** 的 `Scope of Work (In/Out of Scope)` 標籤區段，確認專案邊界。
   - 掃描 **[[plan/AGENT.md]]** 的 `Behavioral Guardrails (§6)` 標籤區段，確認安全紅線。
   - 掃描 **[[skills/]]** 目錄結構與技能 Frontmatter（例如 [[skills/README-SKILLS.md]]），掌握專案可用技能庫與觸發機制。
3. **按需延伸與 Skill 觸發載入 (On-Demand Loading & Skill Triggering)**：
   - 只有在處理具體功能、任務打勾或架構重構時，才按需載入 [[plan/PROCESS.md]]、[[doc/]] 或 [[structure/]]。
   - 當面臨特定的決策分級（如 T3 重大決策）或觸發關鍵字時，按需載入對應的 Skill 指引檔（例如 [[skills/council/SKILL.md]]）。

<!-- @KEEP:SEMVER -->
> 讀取完畢後，以一段簡短摘要向使用者回報：「我已掌握專案現況，目前處於 [階段 X]，本專案版本策略為 SemVer 2.0，準備執行 [簡述下一步]。」
<!-- @END:SEMVER -->
<!-- @KEEP:CALVER -->
> 讀取完畢後，以一段簡短摘要向使用者回報：「我已掌握專案現況，目前處於 [階段 X]，本專案版本策略為 CalVer，準備執行 [簡述下一步]。」
<!-- @END:CALVER -->

4. **新專案初始化守則 (New Project Bootstrap Rule)**：
   - 當被指派從本範本初始化新專案時，Agent **必須先與使用者確認**以下三項設定後方可執行 [[scripts/bootstrap.py]]：
     1. **版本策略**：SemVer 2.0 或 CalVer？
     2. **專案名稱** (`--name`)
     3. **選用目錄** (`--modules`)：參照 [[README.md]] 目錄增減決策樹。
   - **禁止**使用 `--non-interactive` 參數自行跳過確認。

---

## 1. 命名與文件規則 (Naming & Documentation Rules)

- **檔案命名規則 (全局)**：
  - **核心計畫與管理 Markdown 檔案**：強制使用 **UPPER-CASE (全大寫並以破折號 `-` 連接)**。
    * *範例*：[[README.md]]、[[plan/TARGET.md]]、[[plan/AGENT.md]]、[[plan/PROCESS.md]]、[[plan/MEMORY.md]]、[[plan/GIT-GUIDE.md]]
  - **Skill 庫檔案**：Skill 目錄統一使用 kebab-case，主要指引檔案統一命名為 `SKILL.md`（包含 YAML Frontmatter 規範）。
    * *範例*：[[skills/council/SKILL.md]]
  - **一般專案文件與規格書**：強制使用 **kebab-case (全小寫並以破折號 `-` 連接)**。
    * *範例*：[[doc/functional-spec-template.md]]、[[doc/data-schema-template.md]]
  - **程式原始碼與腳本**：依據語言慣例（例如 Python 專案強制使用 **snake_case**），嚴禁在 Python 檔名中使用破折號 `-` 以避免 import 語法錯誤。
    * *範例*：[[scripts/version_engine.py]]、[[scripts/sync_project.py]]
- **Markdown 優先與 Obsidian Wiki Link 鐵律 (禁止內部 file:///)**：
  - 所有非程式碼文件一律採用 Markdown 撰寫。
  - **🚫 禁止內部 `file:///` 鐵律**：專案內部檔案之間的互相引用與知識庫關聯，**嚴禁使用 `file:///` 本地絕對路徑**（以防專案移動或複製時連結全數失效）。**只要在專案內部，一律強制使用 Obsidian Wiki Link 格式 (`[[plan/TARGET.md]]` 或 `[[doc/functional-spec-template.md#區段]]`)**。
  - **`file:///` 的唯一允許情境**：`file:///` **僅作為指向本機專案外部實體路徑（如系統全域環境資源）的最後避難手段 (Last Resort)**。
  - AI Agent 在閱讀與導覽專案時，應能原生識別 Wiki Link 並精確跳轉至對應物理檔案。

---

## 2. 專案架構與程式撰寫規則 (Architecture & Code Design)

- **核心架構設計模式**：
  - **Supervisor Pattern**：主模組僅負責調度與異常處理，不包含具體業務邏輯。
  - **DataPool 批次原子性**：資料處理模組必須支援批次寫入與 Transaction 失敗回滾。
- **SRP 單一職責原則 (Single Responsibility Principle)**：
  - 取消硬性 800 行切碎限制。程式碼模組拆分改以 SRP 原則評估。
  - 對於高內聚且職責單一之模組（如 GUI 面板或 Protocol Spec 映射表），單檔上限放寬至 **1,200 行** 軟性警示。超過 1,200 行時應進行重構拆分並同步更新專案模組架構說明。

---

## 3. 溝通決策與 Sub-Agent 協作規範 (Communication & Sub-Agent Protocol)

### 3.1 決策分級制度 (Decision Tiers)
| 級別 | 定義 | Agent 行為 | 範例與處理流程 |
| :--- | :--- | :--- | :--- |
| **T1 自主決定** | 輕微改動、格式修正 | 直接執行，記錄至 [[plan/cold-history.log]] | 變數命名、排版、小幅文案修飾。 |
| **T2 知會即可** | 常規功能微調、參數優化 | 執行後主動簡報告知使用者 | 新增輔助函式、單元測試調整。 |
| **T3 必須討論** | 核心架構變更、Schema 修改 | 暫停執行，提出選項討論後方可執行 | 變更資料庫 Schema、引進新套件、重大重構 (啟用 Council Skill: [[skills/council/SKILL.md]])。 |

### 3.2 Sub-Agent 主動調度與單一寫入者原則 (Single Writer Rule)
- **開放主動調度**：面對大範圍搜尋、獨立單元測試或議會辯論時，主 Agent 可主動調用 `invoke_subagent` 派生子代理。
- **派生限制**：單次任務子代理派生深度 `max_depth = 1`，最大併列數 `max_children = 2`。
- **🔒 單一寫入者原則 (Single Writer Rule)**：
  - 子代理 (Sub-Agent) **僅具備唯讀權限，或僅能將產出寫入 `.council/` 暫存檔**。
  - **嚴禁 Sub-Agent 直接呼叫 [[scripts/sync_project.py]] 或寫入 [[plan/MEMORY.md]] / [[plan/cold-history.log]]**。所有狀態同步與記憶更新必須統一回傳給 Parent Agent 審核後單線寫入，徹底防範並行寫入覆蓋 (Race Condition)。

---

## 4. 版本控制與 Git 規範 (Version Control & Git Rules)

<!-- @KEEP:SEMVER -->
- **版本模式 (SemVer 2.0)**：
  - 版號 `vMAJOR.MINOR.PATCH`（如 `v1.0.0`），Commit 標題遵守 Conventional Commits (`type(scope): subject`)。
- **Commit 語意規範**：
  - **Header 強制規範**：嚴格符合 Conventional Commits 正則。
<!-- @END:SEMVER -->
<!-- @KEEP:CALVER -->
- **版本模式 (CalVer)**：
  - 版號 `vYYYY.MM.DD` 或 `v1.0.YYYYMMDD.Z`，Commit 標題開頭附帶版號前綴。
- **Commit 語意規範**：
  - **Header 強制規範**：嚴格符合 CalVer 前綴正則。
<!-- @END:CALVER -->
  - **Body 不限制 / 允許使用中文說明 (Permitted CJK, not forced)**：方便詳細說明變更脈絡與設計理據。
- **Git Hook 自動代勞與 2 次自我糾錯限制**：
  - 變更完成後，一律執行 [[scripts/sync_project.py]] 自動計算版號、打勾 ToDo 與格式化 Commit 標題。
  - 若 Git Hook 攔截報錯，Agent 最多執行 **2 次 Self-Correction** 修正。若連續 2 次失敗，自動附加 `--no-verify` 提交 `WIP` 並觸發 HITL 人工介入。

---

## 5. 測試驗證與 Definition of Done (DoD)

Agent 在宣告任務完成前，必須通過 **「三維客觀 DoD 矩陣 (Three-Dimensional DoD Matrix)」** 審驗：

### DoD 審驗矩陣
1. **Type C (代碼變更)**：`git diff` 包含 `.py` 等程式碼時，必須執行單元測試且 100% 綠燈通過。
2. **Type A (純 Markdown/文檔變更)**：豁免單元測試，但**強制通過 [[scripts/sync_project.py]] 靜態檢驗**：
   - 校驗 Markdown 檔內所有 `file:///` 本地連結是否存在。
   - 校驗 Markdown 內嵌 JSON / YAML 語法解析正確。
   - 校驗檔名大小寫與 kebab-case 格式。
3. **狀態同步**：執行 [[scripts/sync_project.py]]，確認 [[plan/PROCESS.md]] 待辦已打勾，[[plan/MEMORY.md]] 索引已更新。

---

## 6. 行為邊界護欄 (Behavioral Guardrails)

### ✅ 總是執行 (Always Do)
- 每次開工前，執行兩階段 Bootstrapping 掃描熱記憶與護欄。
- 每次編輯檔案前，貫徹 **先讀後寫 (Read-before-Write)** 原則。
- 變更完成後，執行 [[scripts/sync_project.py]] 完成同步與 DoD 靜態檢查。

### ⚠️ 先詢問再行動 (Ask First)
- 涉及 T3 門檻之架構修改、 Schema 變更或引進新依賴套件。
- 涉及機敏憑證或刪除物理核心目錄。

### 🚫 絕不執行 (Never Do)
- 絕不將 API Key、密碼或憑證硬編碼於代碼或 Git 版本庫中。
- 絕不上傳或外洩 `.env` 或機敏設定檔至外部網路。
- 絕不下達未經確認的破壞性清空指令 (如 `rm -rf /` 或 `git reset --hard` 未暫存變更)。
- 絕不自動執行 `git push origin --delete` 刪除遠端分支（遠端分支清理必須由人類開發者或 PR/MR 工具處置）。
- 絕不自動執行 `git branch -D` 強制刪除本地分支（若 `git branch -d` 失敗代表存有未整合 Commit，必須停止並回報）。

---

## 7. 忽略清單 (Ignore List)

`\.git`, `\.obsidian`, `\.vscode`, `\.idea`, `\.venv`, `\.pytest_cache`, `\logs\archived`, `\.council`
