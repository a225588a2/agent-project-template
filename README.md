# 通用專案結構模板 (General Project Template)

本專案是一個**高通用性**的專案結構模板，適用於各種類型的專案開發（例如：軟體程式開發、文件編撰專案、資料蒐集整理、學術研究等）。

---

## 💡 設計哲學 (Design Philosophy)

本模板的核心設計基於「**漸進式揭露 (Progressive Disclosure)**」原則——確保閱讀者（不論是人或 AI Agent）在初始階段只接觸最精華的高階地圖，並在需要時才深入細節。

三個必要核心目錄的分層正是此原則的具體實踐：

| 層級 | 目錄 | 內容定位 | 載入時機 |
| :--- | :--- | :--- | :--- |
| **第一層：地圖** | `plan/` | 專案要做什麼（WHAT）、為什麼做（WHY） | 專案啟動時首先閱讀 |
| **第二層：規格** | `doc/` | 具體怎麼做的細節規則（HOW in detail） | 處理特定功能時按需載入 |
| **第三層：藍圖** | `structure/` | 物理模組關係圖與動態流程時序圖 | 需要理解全局架構時參考 |

> [!WARNING]
> **認知負載警告**：研究顯示，AI 大型語言模型在同時處理超過 150 條獨立指令時，準確率會急遽下降。因此，核心規範文件（如 `AGENT.md`、`TARGET.md`）建議將核心指令控制在 **80 條以內**，並將具體細節分散至 `doc/` 與 `structure/` 中按需載入，避免在單一文件中混入過多層次的資訊。

---

## 🏢 專案結構定位 (造車公司比喻)

本專案的設計哲學遵循「造車公司」的職責分離（Separation of Concerns）原則，劃分為**必要核心**與**自由增減參考**目錄，確保專案的管理、規格、設計藍圖與成品各司其職：

### 1. 必要核心目錄 (Mandatory Cores)

這三個目錄是理清專案脈絡與工作紀律的必要基礎：

*   **[plan/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan)** (企業目標與管理層)
    *   *職責*：定義核心目標、工作規範、開發進度與日常執行日誌。
    *   *關鍵檔案*：
        *   [TARGET.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/TARGET.md)：定義專案核心目標與邊界。
        *   [AGENT.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/AGENT.md)：參與者（人/AI）工作與命名規範。
        *   [PROCESS.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/PROCESS.md)：專案開發里程碑與待辦清單 (ToDo)。
        *   [MEMORY.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/MEMORY.md)：每日執行歷史日誌與關鍵決策備忘。
        *   [GIT-GUIDE.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/GIT-GUIDE.md)：Git 操作的非標準情境指引（階段式揭露，日常不需翻閱）。
        *   [COUNCIL.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/COUNCIL.md)：多 Agent 討論議會與看板式交接規範（⚠️ *選用*，高額度/高難度任務時啟用）。
        *   [FEEDBACK.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/FEEDBACK.md)：專案經驗回饋紀錄（⚠️ *選用*，可視專案需求刪除）。
*   **[doc/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc)** (產品/專案規格書)
    *   *職責*：定義具體功能、邏輯、資料結構、檔案格式與配置規則的規格書。
    *   *模板檔案*：
        *   [functional-spec.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/functional-spec.md)：詳細的功能與演算法邏輯規格模板。
        *   [data-schema.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/data-schema.md)：資料表、設定檔與快取格式規格模板。
        *   [exclusion-rules.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/exclusion-rules.md)：排除與過濾規則規格模板。
*   **[structure/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/structure)** (工程藍圖/電路設計圖)
    *   *職責*：定義物理模組的拆分關係與靜/動態流程圖。
    *   *模板檔案*：
        *   [modules.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/structure/modules.md)：物理檔案與職責地圖模板。
        *   [diagram.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/structure/diagram.md)：靜態依賴圖與動態 Mermaid 時序圖/流程圖模板。

---

### 2. 自由增減參考目錄 (Optional / Reference Only)

以下為本模板預先建立的基礎目錄範例，**您可以根據專案的具體性質自由增減或完全自訂本列表以外的任何目錄**：

*   **[source/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/source)** (最後造出來的成品車)
    *   *職責*：放置最終產出的主檔案（例如：可執行程式原始碼、文件初稿、核心資料產出）。
*   **[test/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/test)** (驗證可靠性的實驗室)
    *   *職責*：放置單元測試、資料驗證腳本、Mock 程式或人工審查標準。
*   **[scripts/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/scripts)** (輔助工具車間)
    *   *職責*：放置一對多輔助腳本、資料爬蟲、臨時資料清洗/轉換工具。
*   **[logs/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/logs)** (儀表板/黑盒子)
    *   *職責*：放置系統運行日誌、排程報告、中間過程暫存檔。
*   **[refer/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/refer)** (原料倉庫/背景資料)
    *   *職責*：放置原始輸入資料（Raw Data）、客戶原始文件、參考文獻、法規標準。

---

## 🚀 如何使用本模板啟動新專案 (Quick Start)

當您或您的 AI Agent 準備啟動一個新專案時，為避免盲目載入不必要的文件以及維護清晰的進度，我們提供以下兩種啟動路徑（推薦優先使用 **Option A 腳本啟動**以提高準確率並節省 Token）：

### 🌿 專案目錄增減決策樹 (Directory Decision Tree)

為保持專案結構極簡並防範 Token 浪費，不應盲目建立所有選用目錄。請在初始化專案時核對以下問題，以決定是否建立各選用目錄（腳本啟動時可透過 `--modules` 參數指定，如 `--modules "source,test"`）：

1.  **`source/` (程式原始碼與主成品)**
    *   *決策問題*：「本專案的目標是否包含『編寫/建構實體程式碼、軟體成品、或核心交付物』？」
    *   *若有* ➜ 啟用 `source/`。
2.  **`test/` (測試與驗證實驗室)**
    *   *決策問題*：「本專案是否包含需要被測試、跑自動化驗證、或進行資料校對的程式模組？」
    *   *若有* ➜ 啟用 `test/`（若無可執行代碼則跳過）。
3.  **`scripts/` (輔助小工具與腳本車間)**
    *   *決策問題*：「我們是否需要編寫第三方資料爬蟲、臨時資料清洗/轉換小工具、或輔助部署的腳本？」
    *   *若有* ➜ 啟用 `scripts/`。
4.  **`refer/` (原料倉庫與背景資料)**
    *   *決策問題*：「本專案是否包含大量外部原始資料、參考文獻、法規標準、或客戶提供的背景文件？」
    *   *若有* ➜ 啟用 `refer/`。

---

### 💡 Option A：腳本快速啟動 (推薦)

您可以直接調用範本內建的初始化腳本 `scripts/bootstrap.py`，一鍵自動化建立專案結構、解鎖文件並初始化 Git。

**🛠️ 執行指令**（請將路徑與參數替換為您的真實屬性）：
```bash
python scripts/bootstrap.py --target-dir <目標專案根目錄> --name "專案名稱" --agent "AI主要代理"
```
*   **非互動模式**：在沙盒或 CI/CD 無 TTY 環境下，腳本會自動以 `--non-interactive` 模式執行，自動填寫預設值。
*   **Git 本地安全偵測**：腳本僅檢查目標目錄本身是否存在 `.git`。若不存在（即使父目錄有 Git 管控且忽略了本專案），仍會獨立初始化 Git 並自動進行首次零點 Commit（格式為 `v1.0.YYYYMMDD.1 Initialize project template`）。

---

### 📝 Option B：手動逐步啟動 (保留備份)

如果您傾向於不依賴腳本，或在特殊環境下開發，可以完全保留原有的手動解鎖啟動流程：

#### 1. 第一階段：複製地圖與核心規範 (建立 plan/ 與 `-template` 後綴)
```powershell
# 1. 於 {目標專案} 建立必要核心目錄
mkdir <目標專案根目錄>/plan, <目標專案根目錄>/doc, <目標專案根目錄>/structure

# 2. 複製 {範本專案} 的 plan 核心檔案，並加上 -template 後綴
cp <範本專案根目錄>/plan/TARGET.md <目標專案根目錄>/plan/TARGET-template.md
cp <範本專案根目錄>/plan/AGENT.md <目標專案根目錄>/plan/AGENT-template.md
cp <範本專案根目錄>/plan/PROCESS.md <目標專案根目錄>/plan/PROCESS-template.md
cp <範本專案根目錄>/plan/COUNCIL.md <目標專案根目錄>/plan/COUNCIL-template.md
cp <範本專案根目錄>/plan/GIT-GUIDE.md <目標專案根目錄>/plan/GIT-GUIDE.md
cp <範本專案根目錄>/plan/MEMORY.md <目標專案根目錄>/plan/MEMORY.md
```
*   **查核點**：Agent 暫停並與使用者對齊專案目標後，編輯並重命名解鎖：
    ```powershell
    mv <目標專案根目錄>/plan/TARGET-template.md <目標專案根目錄>/plan/TARGET.md
    mv <目標專案根目錄>/plan/AGENT-template.md <目標專案根目錄>/plan/AGENT.md
    mv <目標專案根目錄>/plan/PROCESS-template.md <目標專案根目錄>/plan/PROCESS.md
    mv <目標專案根目錄>/plan/COUNCIL-template.md <目標專案根目錄>/plan/COUNCIL.md
    ```

#### 2. 第二階段：建立專案門面與規劃 (README.md & .gitignore)
```powershell
cp <範本專案根目錄>/README.md <目標專案根目錄>/README-template.md
cp <範本專案根目錄>/.gitignore <目標專案根目錄>/.gitignore
```
*   **查核點**：編輯 `README-template.md` 寫入專案簡介，並解鎖：
    ```powershell
    mv <目標專案根目錄>/README-template.md <目標專案根目錄>/README.md
    ```
*   **Git 初始化**：
    ```powershell
    git -C <目標專案根目錄> init
    git -C <目標專案根目錄> add .
    git -C <目標專案根目錄> commit -m "v1.0.YYYYMMDD.1 Initialize project structure and core guidelines"
    ```

#### 3. 第三階段：按需載入規格與藍圖
```powershell
cp <範本專案根目錄>/doc/data-schema.md <目標專案根目錄>/doc/data-schema-template.md
# 編輯完成後解鎖
mv <目標專案根目錄>/doc/data-schema-template.md <目標專案根目錄>/doc/data-schema.md
```

> [!TIP]
> **啟動完成後清理**：當專案成功初始化並解鎖啟用後，使用者或 Agent 可自行決定是否將本 README.md 中關於手動啟動的冗長指令說明刪除，僅保留專案介紹，以保持專案根目錄文件清爽。

---

## 🔄 進度與版本同步自動化 (DoD Sync Automation)

本專案模板內建了自動化同步腳本 `scripts/sync_project.py`，用於在任務完成時自動為 `plan/PROCESS.md` 待辦事項打勾，並推進版本號與更新熱記憶日誌。

### 1. 使用方式 (Usage)
完成任務或日常變更後，在專案根目錄執行：
```bash
python scripts/sync_project.py [--bump patch|minor|major]
```

### 2. 核心規範 (Rules)
*   **日誌格式**：同步前，必須確保 `logs/cold-history.log` 的最新一筆日誌中寫有 `todo_ref: 待辦項目名稱` (或與任務無關變更時寫 `todo_ref: null`) 以及 `commit: vX.Y.YYYYMMDD.Z Summary`。
*   **版本號規格**：版本號強制遵循 `vX.Y.YYYYMMDD.Z` 規格，且必須作為對應 Git Commit 標題的前綴。
    *   *Commit 範例*：`v1.0.20260701.1 Add database connection`
*   **自我糾錯限制**：若同步腳本因格式不符拋出 `exit(1)`，Agent 最多執行 2 次自我糾錯重試，若仍失敗必須轉為 HITL 人工介入。

---

## ⚓ Git Commit 驗證機制 (Git Commit Validation Hooks)

本專案配置了 `pre-commit` 與 `commit-msg` git hooks，在 commit 時自動強制驗證專案狀態與 Commit 格式，避免非合規變更被提交。

### 1. 驗證內容
- **檔案一致性**：確保 `plan/PROCESS.md`、`logs/cold-history.log` 與 `.sync-state.json` 版號完全一致（即 commit 前有確實執行 `sync_project.py`）。
- **Commit 標題**：必須以當前同步版號為前綴，格式為 `vX.Y.YYYYMMDD.Z English Summary`。
- **語系限制**：Commit 訊息（標題與描述）強制使用英文（阻擋中日韓 CJK 字元及全形標點）。

### 2. 安裝與部署
若是新專案透過 `scripts/bootstrap.py` 初始化，Hooks 將自動啟用。若是手動 clone 本儲存庫，請在專案根目錄執行以下指令啟用 Hooks：
```bash
python scripts/install_hooks.py
```

### 3. 繞過檢查
若需要提交臨時/未完成之 WIP 變更，可使用 `git commit -m "WIP" --no-verify` 繞過 Hook 驗證。

