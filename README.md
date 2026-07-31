# 通用 AI 專案結構模板 (AI Project Template)

本專案是一個**高通用性、高工程嚴謹度**的 AI 專案結構模板，適用於軟體開發、筆記資料整理、學術研究與自動化管線等各類專案。

---

## 💡 核心設計哲學 (Design Philosophy)

1. **兩階段漸進式啟動 (Progressive Disclosure - Two-Stage Bootstrap)**：
   - **Stage 1 (熱載入)**：讀取 [[plan/MEMORY.md]]（約 1.5k Token 滾動摘要與最近變更）。
   - **Stage 2 (標籤掃描)**：輕量掃描 [[plan/TARGET.md]] 的 Scope 與 [[plan/AGENT.md]] 的 Guardrails 標籤區段，控制 Token 於極小範疇，杜絕失憶越界。
<!-- @KEEP:SEMVER -->
1. **git 版本控制 - SemVer 2.0 (`vMAJOR.MINOR.PATCH`)**：
   - 配合 Conventional Commits 與 Gitflow 雙主線模型。
<!-- @END:SEMVER -->
<!-- @KEEP:CALVER -->
1. **git 版本控制 - CalVer 日期導向 (`vYYYY.MM.DD` / `v1.0.YYYYMMDD.Z`)**：
   - 適用於個人筆記、每日日誌、資料整理專案，輕量單主線模型。
<!-- @END:CALVER -->
3. **單一寫入者原則 (Single Writer Rule)**：
   - 開放 AI 主動調度 Sub-Agent，但 Sub-Agent 僅具備唯讀或 [[skills/council/]] 暫存寫入權限。所有全局狀態同步與 Log / Memory 寫入統一由 Parent Agent 單線執行，防範 Race Condition。
4. **三維客觀 DoD 矩陣 (Three-Dimensional DoD Matrix)**：
   - **Type C (代碼改動)**：強制 100% 單元測試綠燈通過。
   - **Type A (純 Markdown/文檔)**：自動校驗檔案大小寫命名、內嵌 JSON/YAML/Mermaid 語法解析與 [[Obsidian Wiki Link]] 存在性。

---

## 🏢 專案結構與職責劃分 (造車公司比喻 Separation of Concerns)

本專案的設計哲學遵循「造車公司」的職責分離 (Separation of Concerns) 原則，劃分為**必要核心**與**自由增減參考**目錄，確保專案的管理、規格、設計藍圖與成品各司其職：

### 1. 必要核心目錄 (Mandatory Cores)

這四個目錄是理清專案脈絡、工作紀律與專業技能 SOP 的必要基礎：

| 目錄 | 職責定位 (造車公司比喻) | 關鍵檔案 |
| :--- | :--- | :--- |
| **[[plan/]]** | 企業目標與管理層（開工必讀入口） | [[plan/TARGET.md]] (專案目標與邊界)<br>[[plan/AGENT.md]] (工作與命名規範)<br>[[plan/PROCESS.md]] (里程碑與待辦 ToDo)<br>[[plan/MEMORY.md]] (熱記憶索引)<br>[[plan/cold-history.log]] (完整歷史日誌，Grep 代替 RAG)<br>[[plan/GIT-GUIDE.md]] (Git 雙軌規範與發布指引) |
| **[[doc/]]** | 產品與專案規格書（按需載入） | [[doc/functional-spec-template.md]] (功能與邏輯規格)<br>[[doc/data-schema-template.md]] (資料表與 Schema 規格)<br>[[doc/exclusion-rules-template.md]] (排除與過濾規則規格)<br>[[doc/yaml-truth-spec-template.md]] (YAML 唯一真理規格範本) |
| **[[structure/]]** | 工程藍圖與電路設計圖 | [[structure/modules-template.md]] (物理模組與職責地圖)<br>[[structure/diagram-template.md]] (Mermaid 時序與動態流程圖) |
| **[[skills/]]** | 技能庫與專業 SOP 車間（按需觸發與載入） | [[skills/README-SKILLS.md]] (Skill 庫規範說明)<br>[[skills/council/SKILL.md]] (多 Agent 議會討論 Skill) |

### 2. 自由增減參考目錄 (Optional / Reference Only)

以下為本模板可選的基礎目錄，**您可以根據專案的具體性質自由增減或自訂**：

* **[[source/]]** (最後造出來的成品車)：放置最終產出的主檔案（例如：可執行程式原始碼、核心交付物）。
* **[[test/]]** (驗證可靠性的實驗室)：放置單元測試、自動化驗證腳本或 Mock 程式。
* **[[scripts/]]** (輔助工具車間)：放置一對多輔助腳本（[[scripts/version_engine.py]], [[scripts/bootstrap.py]], [[scripts/sync_project.py]], [[scripts/git_hook_validator.py]]）。
* **[[logs/]]** (儀表板與黑盒子)：選用目錄，放置系統運行階段日誌、排程報告與中間過程暫存檔（冷歷史日誌已劃歸 [[plan/cold-history.log]]）。
* **[[refer/]]** (原料倉庫與背景資料)：放置原始輸入資料（Raw Data）、客戶原始文件與參考文獻。

---

## 🌿 專案目錄增減決策樹 (Directory Decision Tree)

為保持專案結構極簡並防範 Token 浪費，不應盲目建立所有選用目錄。請在初始化專案時核對以下 4 大決策問題，以決定是否建立各選用目錄（腳本啟動時可透過 `--modules` 參數指定，如 `--modules "source,test"`）：

1. **`source/` (程式原始碼與主成品)**
   - *決策問題*：「本專案的目標是否包含『編寫/建構實體程式碼、軟體成品、或核心交付物』？」
   - *若有* ➜ 啟用 `source/`。
2. **`test/` (測試與驗證實驗室)**
   - *決策問題*：「本專案是否包含需要被測試、跑自動化驗證、或進行資料校對的程式模組？」
   - *若有* ➜ 啟用 `test/`（若無可執行代碼則跳過）。
3. **`scripts/` (輔助小工具與腳本車間)**
   - *決策問題*：「我們是否需要編寫第三方資料爬蟲、臨時資料清洗/轉換小工具、或輔助部署的腳本？」
   - *若有* ➜ 啟用 `scripts/`。
4. **`refer/` (原料倉庫與背景資料)**
   - *決策問題*：「本專案是否包含大量外部原始資料、參考文獻、法規標準、或客戶提供的背景資料？」
   - *若有* ➜ 啟用 `refer/`。

---

<!-- @KEEP:TEMPLATE -->
## 🤖 如何在「Agent 層面」與「檔案層面」調用本範本 (Usage Guide)

使用本模板時，**使用者完全無需手動複製整包專案檔案**，可透過 AI Agent 一指 Prompt 指引或 CLI 工具腳本輕鬆建立新專案：

### 🤖 1. Agent 層面使用指引 (Agent-Driven Initialization)
若您是在 IDE (如 Antigravity / Cursor / VSCode) 或對話環境中搭配 AI Agent 開發，您**只需向您環境中的 AI Agent 下達指令**，讓 Agent 讀取本範本並執行啟動：

> **💬 Prompt 範例**：
> 「請閱讀這個 AI 專案模板 `c:/PersonalWS/AgentSandBox/AiProjectTemplate`，並幫我在 `c:/PersonalWS/MyNewProject` 建立一個名為 `MyNewProject` 的新專案，版本策略採用 SemVer 2.0 (或 CalVer)。」

#### 📁 運作原理 (File-Level Mechanism & Lifecycle)
- **檔案複製與一次性裝配**：[[scripts/bootstrap.py]] 腳本執行時，會將本範本中的必要核心目錄 ([[plan/]], [[doc/]], [[structure/]], [[scripts/]], [[skills/]]) 與工具檔複製並渲染寫入至指定的「目標目錄」。
- **獨立運作與範本純淨**：初始化完成後，目標目錄將成為一個包含獨立 `.git` 儲存庫與 Git Hooks 的完整專案。本範本儲存庫仍維持乾淨純潔，可隨時被重複調用或持續升級。
- **選用目錄決策樹**：初始化時可透過 `--modules` 參數（例如 `--modules "source,test"`）按需建立選用目錄，防範無用目錄堆疊。

---

### 🚀 2. 啟動路徑 Option A vs Option B

當您或您的 AI Agent 準備啟動一個新專案時，我們提供以下兩種啟動路徑（推薦優先使用 **Option A 腳本啟動**以提高準確率並節省 Token）：

#### 💡 Option A：腳本快速啟動 (推薦)

自行在 CLI 終端機調用，直接執行範本內建的初始化腳本 [[scripts/bootstrap.py]]：

```bash
python scripts/bootstrap.py --target-dir <目標目錄> --name "專案名稱" --version-strategy semver
```

* **參數說明**：
  - `--version-strategy` (`-v`)：可指定 `semver` (程式碼/軟體專案) 或 `calver` (筆記/日誌專案)。
  - 於 TTY 互動模式下會顯示對話選單；於 `--non-interactive` 模式下會自動進行**啟發式自動推斷 (Smart Auto-Detection)** 檢測專案特徵檔案。
  - 初始化過程會檢查並引導設定 Git `user.name` 與 `user.email` 作者簽名。

---

#### 📝 Option B：手動解鎖啟動流程 (保留備份)

若您傾向於不依賴腳本，或在特殊環境下開發，可以完全保留原有的手動解鎖啟動流程：

##### 1. 第一階段：複製地圖與核心規範 (建立 `plan/` 與 `-template` 後綴)
```powershell
# 1. 於 {目標專案} 建立必要核心目錄
mkdir <目標專案根目錄>/plan, <目標專案根目錄>/doc, <目標專案根目錄>/structure, <目標專案根目錄>/skills

# 2. 複製 {範本專案} 的 plan 核心檔案與 skills 技能庫，並加上 -template 後綴
cp <範本專案根目錄>/plan/TARGET.md <目標專案根目錄>/plan/TARGET-template.md
cp <範本專案根目錄>/plan/AGENT.md <目標專案根目錄>/plan/AGENT-template.md
cp <範本專案根目錄>/plan/PROCESS.md <目標專案根目錄>/plan/PROCESS-template.md
cp <範本專案根目錄>/plan/GIT-GUIDE.md <目標專案根目錄>/plan/GIT-GUIDE.md
cp <範本專案根目錄>/plan/MEMORY.md <目標專案根目錄>/plan/MEMORY.md
cp -r <範本專案根目錄>/skills/* <目標專案根目錄>/skills/
```
* **查核點**：Agent 暫停並與使用者對齊專案目標後，編輯並重命名解鎖：
  ```powershell
  mv <目標專案根目錄>/plan/TARGET-template.md <目標專案根目錄>/plan/TARGET.md
  mv <目標專案根目錄>/plan/AGENT-template.md <目標專案根目錄>/plan/AGENT.md
  mv <目標專案根目錄>/plan/PROCESS-template.md <目標專案根目錄>/plan/PROCESS.md
  ```

##### 2. 第二階段：建立專案門面與規劃 (README.md & .gitignore)
```powershell
cp <範本專案根目錄>/README.md <目標專案根目錄>/README-template.md
cp <範本專案根目錄>/.gitignore <目標專案根目錄>/.gitignore
```
* **查核點**：編輯 `README-template.md` 寫入專案簡介，並解鎖：
  ```powershell
  mv <目標專案根目錄>/README-template.md <目標專案根目錄>/README.md
  ```
* **Git 初始化與首次 Commit**：
  ```powershell
  git -C <目標專案根目錄> init
  git -C <目標專案根目錄> add .
  git -C <目標專案根目錄> commit -m "v1.0.YYYYMMDD.1 Initialize project structure and core guidelines"
  ```

##### 3. 第三階段：按需載入規格與藍圖
```powershell
cp <範本專案根目錄>/doc/data-schema-template.md <目標專案根目錄>/doc/data-schema.md
```

> [!TIP]
> **啟動完成後清理**：當專案成功初始化並解鎖啟用後，使用者或 Agent 可自行決定是否將本 [[README.md]] 中關於手動啟動的說明刪除，僅保留專案介紹，以保持專案根目錄文件清爽。
<!-- @END:TEMPLATE -->

---

## 🔄 進度與 DoD 同步自動化 (DoD Sync Automation)

每次完成變更或寫入 [[plan/cold-history.log]] 後，在專案根目錄執行：

```bash
python scripts/sync_project.py [--bump patch|minor|major]
```

### 核心功能與規範：
1. **Type A 靜態品質關卡**：自動檢查 Markdown 中的 `file:///` 連結有效性、檔名大小寫與內嵌 JSON/YAML/Mermaid 語法解析。
2. **自動推升版本**：依選定策略（SemVer 2.0 或 CalVer）自動計算下一版號。
3. **自動打勾 ToDo**：比對 log 中的 `todo_ref` 自動打勾 [[plan/PROCESS.md]]。
4. **自動更新熱記憶**：將變更索引回寫至 [[plan/MEMORY.md]]。
5. **Git Commit 語意規範**：
<!-- @KEEP:SEMVER -->
   - **Header 強制規範**：嚴格符合 Conventional Commits 正則 (`type(scope): summary`)。
<!-- @END:SEMVER -->
<!-- @KEEP:CALVER -->
   - **Header 強制規範**：嚴格符合 CalVer 前綴正則 (`vX.Y.YYYYMMDD.Z summary`)。
<!-- @END:CALVER -->
   - **Body 不限制 / 允許使用中文說明 (Permitted CJK, not forced)**：方便詳細說明變更脈絡與設計理據。
