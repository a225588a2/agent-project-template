# 通用專案結構模板 (General Project Template)

本專案是一個**高通用性**的專案結構模板，適用於各種類型的專案開發（例如：軟體程式開發、文件編撰專案、資料蒐集整理、學術研究等）。

---

## 💡 設計哲學 (Design Philosophy)

本模板的核心設計基於「**漸進式揭露 (Progressive Disclosure)**」原則——確保閱讀者（不論是人或 AI Agent）在初始階段只接觸最精華的高階地圖，並在需要時才深入細節。

三個必要核心目錄的分層正是此原則的具體實踐：

| 層級 | 目錄 | 內容定位 | 載入時機 |
| :--- | :--- | :--- | :--- |
| **第一層：地圖** | `Plan/` | 專案要做什麼（WHAT）、為什麼做（WHY） | 專案啟動時首先閱讀 |
| **第二層：規格** | `Doc/` | 具體怎麼做的細節規則（HOW in detail） | 處理特定功能時按需載入 |
| **第三層：藍圖** | `Structure/` | 物理模組關係圖與動態流程時序圖 | 需要理解全局架構時參考 |

> [!WARNING]
> **認知負載警告**：研究顯示，AI 大型語言模型在同時處理超過 150 條獨立指令時，準確率會急遽下降。因此，核心規範文件（如 `Agent.md`、`Target.md`）建議將核心指令控制在 **80 條以內**，並將具體細節分散至 `Doc/` 與 `Structure/` 中按需載入，避免在單一文件中混入過多層次的資訊。

---

## 🏢 專案結構定位 (造車公司比喻)

本專案的設計哲學遵循「造車公司」的職責分離（Separation of Concerns）原則，劃分為**必要核心**與**自由增減參考**目錄，確保專案的管理、規格、設計藍圖與成品各司其職：

### 1. 必要核心目錄 (Mandatory Cores)

這三個目錄是理清專案脈絡與工作紀律的必要基礎：

*   **[Plan/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan)** (企業目標與管理層)
    *   *職責*：定義核心目標、工作規範、開發進度與日常執行日誌。
    *   *關鍵檔案*：
        *   [Target.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan/Target.md)：定義專案核心目標與邊界。
        *   [Agent.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan/Agent.md)：參與者（人/AI）工作與命名規範。
        *   [Process.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan/Process.md)：專案開發里程碑與待辦清單 (ToDo)。
        *   [Memory.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan/Memory.md)：每日執行歷史日誌與關鍵決策備忘。
        *   [GitGuide.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan/GitGuide.md)：Git 操作的非標準情境指引（階段式揭露，日常不需翻閱）。
        *   [FeedBack.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Plan/FeedBack.md)：專案經驗回饋紀錄（⚠️ *選用*，可視專案需求刪除）。
*   **[Doc/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Doc)** (產品/專案規格書)
    *   *職責*：定義具體功能、邏輯、資料結構、檔案格式與配置規則的規格書。
    *   *模板檔案*：
        *   [Template_FunctionalSpec.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Doc/Template_FunctionalSpec.md)：詳細的功能與演算法邏輯規格模板。
        *   [Template_DataSchema.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Doc/Template_DataSchema.md)：資料表、設定檔與快取格式規格模板。
        *   [Template_ExclusionRules.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Doc/Template_ExclusionRules.md)：排除與過濾規則規格模板。
*   **[Structure/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Structure)** (工程藍圖/電路設計圖)
    *   *職責*：定義物理模組的拆分關係與靜/動態流程圖。
    *   *模板檔案*：
        *   [Template_Modules.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Structure/Template_Modules.md)：物理檔案與職責地圖模板。
        *   [Template_Diagram.md](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Structure/Template_Diagram.md)：靜態依賴圖與動態 Mermaid 時序圖/流程圖模板。

---

### 2. 自由增減參考目錄 (Optional / Reference Only)

以下為本模板預先建立的基礎目錄範例，**您可以根據專案的具體性質自由增減或完全自訂本列表以外的任何目錄**：

*   **[Source/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Source)** (最後造出來的成品車)
    *   *職責*：放置最終產出的主檔案（例如：可執行程式原始碼、文件初稿、核心資料產出）。
*   **[Test/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Test)** (驗證可靠性的實驗室)
    *   *職責*：放置單元測試、資料驗證腳本、Mock 程式或人工審查標準。
*   **[Scripts/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Scripts)** (輔助工具車間)
    *   *職責*：放置一對多輔助腳本、資料爬蟲、臨時資料清洗/轉換工具。
*   **[Logs/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Logs)** (儀表板/黑盒子)
    *   *職責*：放置系統運行日誌、排程報告、中間過程暫存檔。
*   **[Refer/](file:///C:/PersonalWS/AgentSandBox/AiProjectTemplate/Refer)** (原料倉庫/背景資料)
    *   *職責*：放置原始輸入資料（Raw Data）、客戶原始文件、參考文獻、法規標準。

---

## 🚀 如何使用本模板啟動新專案 (Quick Start)

當您要啟動一個新專案（不論是程式開發、資料分析或文件撰寫）時，請依照下列步驟：

1.  **複製結構**：將本模板的所有目錄與檔案複製到您的新專案根目錄下。
2.  **設定目標與規範 (Plan/)**：
    *   編輯 `Plan/Target.md`，填入新專案的核心目標、使用情境與功能範圍。
    *   編輯 `Plan/Agent.md`，根據專案性質微調工作規則（例如：若非 Python 程式專案，可移除最大行數 800 行的 Python 約束，改為 Markdown 檔案的排版約定）。
    *   編輯 `Plan/Process.md`，劃分出您專案的 MVP 執行階段。
3.  **定義規格 (Doc/)**：
    *   參考 `Doc/` 底下的模板，撰寫具體的功能/文件邏輯規格（如資料清洗規則、報告架構）以及資料 Schema（如 Excel 欄位定義、JSON 格式）。
4.  **繪製藍圖 (Structure/)**：
    *   參考 `Structure/` 底下的模板，繪製模組地圖與 Mermaid 流程圖，讓參與專案的人或 AI Agent 清楚理解資料如何流動。
5.  **自由增減目錄**：
    *   若此專案僅為「文件撰寫」，您可以刪除 `Test/`，並在根目錄新建一個 `Draft/` 目錄存放草稿。
    *   若此專案為「資料採集」，您可保留 `Scripts/` 與 `Refer/`，並加入 `Output/` 目錄。
6.  **開始執行**：
    *   在每次重大修改後，在 `Plan/Memory.md` 中記錄變更日誌，並以相同標題提交 Git Commit。
