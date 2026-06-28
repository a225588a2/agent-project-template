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

當您或您的 AI Agent 準備啟動一個新專案時，為避免盲目載入不必要的文件以及維護清晰的進度，**嚴禁一鍵複製所有檔案**。請遵循以下**「三階段漸進式啟動工作流」**：

---

### 1. 第一階段：複製地圖與核心規範 (建立 plan/ 與 `-template` 後綴)

此階段在目標專案中建立核心規劃目錄，並載入暫存的核心規範文件。

**🛠️ 執行指令**（請將 `<目標專案根目錄>` 與 `<範本專案根目錄>` 替換為您的真實路徑）：
```powershell
# 1. 於 {目標專案} 建立必要核心目錄
mkdir <目標專案根目錄>/plan, <目標專案根目錄>/doc, <目標專案根目錄>/structure

# 2. 複製 {範本專案} 的 plan 核心檔案至 {目標專案}，並加上 -template 後綴
cp <範本專案根目錄>/plan/TARGET.md <目標專案根目錄>/plan/TARGET-template.md
cp <範本專案根目錄>/plan/AGENT.md <目標專案根目錄>/plan/AGENT-template.md
cp <範本專案根目錄>/plan/PROCESS.md <目標專案根目錄>/plan/PROCESS-template.md
cp <範本專案根目錄>/plan/COUNCIL.md <目標專案根目錄>/plan/COUNCIL-template.md # 討論議會規範 (選用)
cp <範本專案根目錄>/plan/GIT-GUIDE.md <目標專案根目錄>/plan/GIT-GUIDE.md   # 指引文件不需後綴
cp <範本專案根目錄>/plan/MEMORY.md <目標專案根目錄>/plan/MEMORY.md         # 日誌直接建立
```

**🤝 討論查核點**：
* 執行上述指令後，Agent **必須暫停**，主動向使用者發起討論：
  > 「我已載入專案的基礎地圖與規範範本。請問本專案的具體目標與核心範圍為何？是否有特殊的開發規範需要寫入 `plan/AGENT-template.md`？」

**解鎖與啟用**：
* 與使用者確認後，Agent 編輯 `<目標專案根目錄>/plan/TARGET-template.md` 與 `<目標專案根目錄>/plan/AGENT-template.md`。
* 編輯完成後，執行重命名，移除 `-template` 後綴以解鎖啟用：
  ```powershell
  mv <目標專案根目錄>/plan/TARGET-template.md <目標專案根目錄>/plan/TARGET.md
  mv <目標專案根目錄>/plan/AGENT-template.md <目標專案根目錄>/plan/AGENT.md
  mv <目標專案根目錄>/plan/PROCESS-template.md <目標專案根目錄>/plan/PROCESS.md
  mv <目標專案根目錄>/plan/COUNCIL-template.md <目標專案根目錄>/plan/COUNCIL.md # 若有啟用
  ```

---

### 2. 第二階段：建立專案門面與規劃 (README.md & .gitignore)

此階段建立專案首頁，並決定後續開發需要的選用目錄與規格範本。

**🛠️ 執行指令**：
```powershell
# 複製專案門面與 gitignore 至 {目標專案}
cp <範本專案根目錄>/README.md <目標專案根目錄>/README-template.md
cp <範本專案根目錄>/.gitignore <目標專案根目錄>/.gitignore
```

**🤝 討論查核點**：
* 複製完畢後，Agent **必須暫停**，主動與使用者討論：
  > 「請問我們這個專案接下來需要哪些規格書與架構藍圖？另外，是否需要建立選用目錄（如 source, test, scripts, logs, refer）？」

**解鎖與決策**：
* 根據討論結果，Agent 編輯 `<目標專案根目錄>/README-template.md` 寫入專案簡介與名稱，並移除後綴：
  ```powershell
  mv <目標專案根目錄>/README-template.md <目標專案根目錄>/README.md
  ```
* 依據討論決策，建立需要的選用目錄，例如：
  ```powershell
  mkdir <目標專案根目錄>/source, <目標專案根目錄>/test
  ```

**🔒 Git 初始化**：
* 核心結構與規則就緒後，在 `{目標專案}` 執行 Git 初始化並進行首次零點 Commit 存檔：
  ```powershell
  git -C <目標專案根目錄> init
  git -C <目標專案根目錄> add .
  git -C <目標專案根目錄> commit -m "2026xxxx-1 Initialize project structure and core guidelines"
  ```

---

### 3. 第三階段：按需載入規格與藍圖 (從 doc/ 與 structure/ 複製)

根據第二階段的討論結果，Agent 按需複製所需要的規格書範本，拒絕拷貝不必要的檔案，以防專案目錄膨脹。

**🛠️ 執行指令 (以資料庫/設定檔規格為例)**：
```powershell
# 按需複製 data-schema 範本至 {目標專案}，並加上 -template 後綴
cp <範本專案根目錄>/doc/data-schema.md <目標專案根目錄>/doc/data-schema-template.md
```

**🤝 討論查核點**：
* 複製後，Agent 配合使用者填寫相關規格細節，確保規格與設計精確。

**解鎖與啟用**：
* 填寫完畢後，重命名移除後綴以解鎖：
  ```powershell
  mv <目標專案根目錄>/doc/data-schema-template.md <目標專案根目錄>/doc/data-schema.md
  ```
