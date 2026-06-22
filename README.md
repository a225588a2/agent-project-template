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
        *   [FEEDBACK.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/plan/FEEDBACK.md)：專案經驗回饋紀錄（⚠️ *選用*，可視專案需求刪除）。
*   **[doc/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc)** (產品/專案規格書)
    *   *職責*：定義具體功能、邏輯、資料結構、檔案格式與配置規則的規格書。
    *   *模板檔案*：
        *   [template-functional-spec.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/template-functional-spec.md)：詳細的功能與演算法邏輯規格模板。
        *   [template-data-schema.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/template-data-schema.md)：資料表、設定檔與快取格式規格模板。
        *   [template-exclusion-rules.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/doc/template-exclusion-rules.md)：排除與過濾規則規格模板。
*   **[structure/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/structure)** (工程藍圖/電路設計圖)
    *   *職責*：定義物理模組的拆分關係與靜/動態流程圖。
    *   *模板檔案*：
        *   [template-modules.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/structure/template-modules.md)：物理檔案與職責地圖模板。
        *   [template-diagram.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/structure/template-diagram.md)：靜態依賴圖與動態 Mermaid 時序圖/流程圖模板。

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

當您要啟動一個新專案（不論是程式開發、資料分析或文件撰寫）時，請依照下列步驟：

1.  **複製結構**：將本模板的所有目錄與檔案複製到您的新專案根目錄下。
2.  **設定目標與規範 (plan/)**：
    *   編輯 `plan/TARGET.md`，填入新專案的核心目標、使用情境與功能範圍。
    *   編輯 `plan/AGENT.md`，根據專案性質微調工作規則（例如：若非 Python 程式專案，可移除最大行數 800 行的 Python 約束，改為 Markdown 檔案的排版約定）。
    *   編輯 `plan/PROCESS.md`，劃分出您專案的 MVP 執行階段。
3.  **定義規格 (doc/)**：
    *   參考 `doc/` 底下的模板，撰寫具體的功能/文件邏輯規格（如資料清洗規則、報告架構）以及資料 Schema（如 Excel 欄位定義、JSON 格式）。
4.  **繪製藍圖 (structure/)**：
    *   參考 `structure/` 底下的模板，繪製模組地圖與 Mermaid 流程圖，讓參與專案的人或 AI Agent 清楚理解資料如何流動。
5.  **自由增減目錄**：
    *   若此專案僅為「文件撰寫」，您可以刪除 `test/`，並在根目錄新建一個 `draft/` 目錄存放草稿。
    *   若此專案為「資料採集」，您可保留 `scripts/` 與 `refer/`，並加入 `output/` 目錄。
6.  **開始執行**：
    *   在每次重大修改後，在 `plan/MEMORY.md` 中記錄變更日誌，並以相同標題提交 Git Commit。
