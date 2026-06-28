# 討論議會與協作規範 (Council & Collaboration Guidelines)

本文件定義了在 AI 額度/Token 預算充裕且任務極具挑戰性（如重大架構調整、高難度 Bug 診斷、安全性設計評估等）的情況下，如何啟動並運行「討論議會 (Discussion Council)」或「多 Agent 協作」的具體流程與規範，以最大化利用 AI 的並線思維與批判特性，提升最終產出品質。

---

## 🌟 核心理念與適用情境 (Core Philosophy & Triggers)

單一 Agent 容易陷入思考盲區（Confirmation Bias）或在長對話中產生思維退化。引進「多角色並線討論」可以透過不同的視角、獨立的推理脈絡以及互相質疑，達到防禦性設計與全面驗證的效果。

### 1. 啟用條件 (Trigger Conditions)
主 Agent 在符合以下所有條件時，應主動向使用者提議啟用本機制，或由使用者下達指令啟動：
- **預算與額度充裕**：目前模型使用額度無虞，可容忍多輪討論與並行調用所帶來的 Token 消耗。
- **任務極具挑戰性/開放性**：
  * 面臨重大系統架構決策（如資料庫重大重構、底層通信協定變更、核心流程重新設計）。
  * 遭遇極難重現、跨多個模組的邊界型 Bug 診斷。
  * 需要針對複雜的系統安全或極端性能進行審查或威脅建模。
  * 開放式的技術選型與利弊評估。

---

## 👥 討論議會角色與 Profile 定義 (Council Roles & Profiles)

在議會中，主 Agent（協調者）需 spawn 複數個具備不同 System Prompt 與任務目標的 Sub Agent。每個 Sub Agent 應被視為一個獨立的 **Profile**，具備隔離的上下文與專屬職責。

```mermaid
graph TD
    User([使用者 User]) <--> Coordinator[共識協調者 Coordinator / 主 Agent]
    Coordinator <--> Executor[提案執行者 Executor]
    Coordinator <--> Critic[批判評審者 Critic]
    Executor <--> Critic
```

### 1. 共識協調者 (Consensus Coordinator / Lead) - 由主 Agent 擔任
- **職責**：主持討論、分配工作、維護看板狀態、整合兩方意見、做最終裁決與共識總結，並與 User 進行主要溝通。
- **特質**：中立客觀、善於歸納整理、注重效率與安全護欄。

### 2. 提案執行者 (Proposer / Executor)
- **職責**：根據原始需求起草具體的技術方案、程式碼實作、或規格變更。
- **特質**：積極主動、偏向以行動解決問題，專注於功能實作與細節編碼。

### 3. 批判評審者 (Devil's Advocate / Critic)
- **職責**：專門尋找 Executor 提案中的漏洞、潛在風險、邊界條件遺漏、安全漏洞與效能瓶頸。
- **特質**：極度挑剔、防禦性極強、關注代碼健壯性與系統演進的可維護性。

### 4. 特化專家 (Specialist) - 選用
- **職責**：依任務性質動態引入的專門角色。例如：專注網路資料檢索的 **Researcher**，或專注測試套件編寫的 **Tester**。

---

## 🔒 工作區與上下文隔離原則 (Workspace & Context Isolation)

為防範認知負載過高與 Prompt 污染（避免無效對話或相互影響），必須嚴格遵守以下隔離規則：
1. **資訊最小化原則 (Need-to-Know Basis)**：主 Agent 在啟動 Sub Agent時，僅能傳遞與該子任務直接相關的代碼區塊、文件或 API 說明。**嚴禁**將主 Agent 整個冗長的對話歷史或無關的系統 log 丟入子代理的 context。
2. **獨立的 Workspace**：視需要為 Executor 建立獨立的分支或臨時工作區，防止多個 Agent 同時編輯同一個物理檔案而產生衝突。

---

## 🔄 看板式交接協議 (Kanban Handoff Protocol)

為了避免多 Agent 討論流於「無條理群聊 (Unstructured Chat Log)」，本機制導入**看板式交接協議 (Kanban Handoff)**：

### 1. 協作看板狀態 (Kanban States)
討論過程中，主 Agent 必須在 `task.md` 中維護一個子任務看板，追蹤當前每個角色的狀態：
- `[Todo]`：等待分配。
- `[Drafting]`：Executor 正在撰寫提案。
- `[Pending Review]`：Executor 已提交，等待 Critic 審查。
- `[Resolving]`：Critic 已提出反饋，Executor 正在修改中。
- `[Review Passed]`：Critic 確認無重大風險，準備結案。

### 2. Handoff 規範 (Handoff Requirements)
每次角色交接時，產出的交付物必須符合以下標準格式：

| 交出角色 | 接手角色 | 必須包含的交付物欄位 (Payload) |
| :--- | :--- | :--- |
| **Coordinator** | **Executor** | 1. 原始需求說明<br>2. 輸入檔案路徑與 API 規格<br>3. 預期產出與限制 |
| **Executor** | **Critic** | 1. 設計草案或 Diff<br>2. 變更的理據與設計考量<br>3. 自我驗證結果 |
| **Critic** | **Executor** | 1. 漏洞/風險清單（註記嚴重度：High/Medium/Low）<br>2. 具體修改建議<br>3. 通過審查的條件 |

---

## 💬 議會討論與辯論流程 (Discussion & Debate Flow)

標準的討論議會以「提案 ➜ 辯論 ➜ 修正 ➜ 共識」的迭代流進行：

```mermaid
sequenceDiagram
    autonumber
    participant Coord as Coordinator (主 Agent)
    participant Exec as Executor (執行者)
    participant Crit as Critic (批判者)

    Note over Coord: 步驟 1: 建立議會並分派 [Drafting]
    Coord->>Exec: 傳送任務需求與 Context

    Note over Exec: 步驟 2: Executor 撰寫 Draft Proposal
    Exec->>Coord: 提交設計草案 [Pending Review]
    
    Coord->>Crit: 傳送草案與審查標準
    Note over Crit: 步驟 3: Critic 進行漏洞挖掘與質疑
    Crit->>Coord: 提交風險清單 & 改進建議 [Resolving]

    Coord->>Exec: 傳送風險清單要求修正
    Note over Exec: 步驟 4: Executor 答辯與修正
    Exec->>Coord: 提交第二版方案/代碼 [Pending Review]

    Coord->>Crit: 傳送第二版方案
    Note over Crit: 步驟 5: Critic 二次確認
    alt 仍有重大漏洞
        Crit->>Coord: 再次退回 (進入 Round 3)
    else 通過審查
        Crit->>Coord: 回報 Review Passed
    end

    Note over Coord: 步驟 6: 總結方案並結案
```

---

## 🛡️ 安全與資源防禦護欄 (Safety & Resource Guardrails)

多 Agent 協作是一把雙刃劍，為防止 Token 燒乾或陷入無限迴圈爭論，必須嚴格執行以下護欄：

1. **輪數硬性限制 (Max Iteration Cap)**：
   - Executor 與 Critic 之間的反覆討論與修改，**最高限制為 3 輪**。
   - 若達到 3 輪討論仍無法達成共識，主 Agent (Coordinator) **必須強制介入**，進行人工裁決或整理爭論焦點，並暫停向使用者回報等待裁示。
2. **快速終止條件 (Early Termination)**：
   - 若 Critic 的反饋中僅包含「代碼美化、非關鍵命名調整、或個人偏好」等低嚴重度 (Low) 項目，且不影響安全性與正確性時，Coordinator 應直接通過審查。
3. **使用者覆寫 (User Overrule)**：
   - 使用者在任何討論階段中下達的明確指示或架構決定，擁有最高權力，議會各角色必須無條件遵循並立刻終止該爭論點。
