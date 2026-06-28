# 討論議會與協作規範 (Council & Collaboration Guidelines)

本文件定義了在 AI 額度/Token 預算充裕且面臨重大決策與挑戰時，如何啟動並運行「討論議會 (Discussion Council)」或「多 Agent 協作」的具體流程與規範，以最大化利用 AI 的並線思維與批判特性，提升最終產出品質。

---

## 🌟 核心理念與適用情境 (Core Philosophy & Triggers)

單一 Agent 容易陷入思考盲區（Confirmation Bias）或在長對話中產生思維退化。引進「多角色並線討論」可以透過不同的視角、獨立的推理脈絡以及互相質疑，達到防禦性設計與全面驗證的效果。

### 1. 啟用門檻與動態機制 (Dynamic Trigger Threshold)
為防範認知載荷過高與 Token 浪費，議會流程僅在重大決策時啟用：
- **T3 重大決策級別**（如核心架構修改、資料庫 Schema 變更、新框架引入、重大重構）：**強制啟用**完整議會流程，包含 `Phase 0: Research` 先行流程與檔案式交接。
- **T1/T2 常規決策級別**（如常規 Bug 修復、變數命名、文件微調、輔助函式）：**直接跳過**議會流程與 Phase 0，採用 in-context 記憶體直接處理與交接，避免不必要的臨時檔案產生與 Token 消耗。

---

## 👥 討論議會角色與 Profile 定義 (Council Roles & Profiles)

在議會中，主 Agent（協調者）需 spawn 複數個具備不同 System Prompt 與任務目標的 Sub Agent。每個 Sub Agent 應被視為一個獨立的 **Profile**，具備隔離的上下文與專屬職責。

```mermaid
graph TD
    User([使用者 User]) <--> Coordinator[共識協調者 Coordinator / 主 Agent]
    Coordinator <--> Executor[提案執行者 Executor]
    Coordinator <--> Critic[批判評審者 Critic]
    Executor <--> Critic
    Coordinator <--> Researcher[外部調研者 Researcher]
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

### 4. 外部調研者 (Researcher)
- **職責**：專職外部資料檢索、網頁搜尋、官方技術文件閱讀與競品調研，為議會提供基於事實的外部資訊支持。
- **安全隔離防線**：嚴格實施 **「連網不讀檔，讀檔不連網」** 的雙重沙箱隔離模式。
  - **連網搜尋時**：Researcher 僅能調用 `search_web` 與 `read_url_content` 工具，其執行 Workspace 嚴禁掛載或讀取任何本地敏感檔案（如 `.env` 等）。
  - **讀取本地檔時**：若 Researcher 獲准讀取本地文件（如 `view_file`），則物理上必須完全停用其網路存取工具。
  - **會話級隔離 (Session-level Reset)**：當 Researcher 每次從本地讀檔切換到外網連網時，必須強制重置（Reset）其對話上下文，防止 Memory 殘留本地數據外洩。
  - **簡報無害化過濾 (Sanitization)**：在傳遞調研簡報（`.council/research-brief.md`）給議會其他角色之前，必須透過無害化過濾機制，強制過濾所有 HTML/Markdown 腳本標籤及疑似間接提示注入的指令標籤，以防惡意注入指令在議會鏈路中散播。

---

## 🔒 工作區與上下文隔離原則 (Workspace & Context Isolation)

為防範認知負載過高與 Prompt 污染（避免無效對話或相互影響），必須嚴格遵守以下隔離規則：
1. **資訊最小化原則 (Need-to-Know Basis)**：主 Agent 在啟動 Sub Agent 時，僅能傳遞與該子任務直接相關的代碼區塊、文件或 API 說明。**嚴禁**將主 Agent 整個冗長的對話歷史或無關的系統 log 丟入子代理的 context。
2. **獨立的 Workspace**：為 Executor 建立獨立的分支或臨時工作區，防止多個 Agent 同時編輯同一個物理檔案而產生衝突。
3. **安全隔離**：落實 Researcher 的「連網不讀檔，讀檔不連網」與會話重置原則，防止本地敏感資訊外洩。

---

## 🔄 看板式交接協議與暫存檔案生命週期 (Kanban Handoff & Temp File Lifecycle)

為了避免多 Agent 討論流於「無條理群聊」，本機制導入**看板式交接協議 (Kanban Handoff)** 與**嚴格的生命週期管理**：

### 1. 協作看板狀態 (Kanban States)
討論過程中，主 Agent 必須在看板中維護一個子任務狀態，追蹤當前每個角色的狀態：
- `[Todo]`：等待分配。
- `[Drafting]`：Executor 正在撰寫提案。
- `[Pending Review]`：Executor 已提交，等待 Critic 審查。
- `[Resolving]`：Critic 已提出反饋，Executor 正在修改中。
- `[Review Passed]`：Critic 確認無重大風險，準備結案。

### 2. 暫存檔案生命週期管理 (Temp File Lifecycle)
- **暫存目錄隔離**：所有議會交接的臨時文件（如 `task-desc.md`, `proposal-v1.md`, `critic-report-r1.md` 等）必須統一寫入獨立的 **`.council/`** 目錄中。該目錄必須列入 `.gitignore` 中，禁止提交至 Git 版本控制。
- **結案歸檔與清理**：當狀態變更為 `Review Passed` 結案後，系統/後台腳本將整個 `.council/` 目錄壓縮打包（如 `.council-archive.zip`）移入 `logs/archived/` 目錄中以供未來審查稽核，隨後**自動清理並刪除**整個 `.council/` 目錄下的所有暫存檔，僅保留最終的決策檔案：**`doc/proposals/COUNCIL_DECISION.md`**，以防污染工作區。

### 3. Handoff 規範 (Handoff Requirements)
每次角色交接時，產出的交付物必須寫入 `.council/` 目錄，並符合以下標準格式：

| 交出角色 | 接手角色 | 必須包含的交付物欄位 (Payload) | 暫存檔案路徑 |
| :--- | :--- | :--- | :--- |
| **Coordinator** | **Executor** | 1. 原始需求說明<br>2. 輸入檔案路徑與 API 規格<br>3. 預期產出與限制 | `.council/task-desc.md` |
| **Executor** | **Critic** | 1. 設計草案或 Diff<br>2. 變更的理據與設計考量<br>3. 自我驗證結果 | `.council/proposal-v1.md` |
| **Critic** | **Executor** | 1. 漏洞/風險清單（註記嚴重度：High/Medium/Low）<br>2. 具體修改建議<br>3. 通過審查的條件 | `.council/critic-report-rX.md` |

---

## 💬 議會討論與辯論流程 (Discussion & Debate Flow)

標準的討論議會以「調研 ➜ 提案 ➜ 辯論 ➜ 修正 ➜ 共識 ➜ 歸檔清理」的迭代流進行：

```mermaid
sequenceDiagram
    autonumber
    participant Coord as Coordinator (主 Agent)
    participant Res as Researcher (研究者)
    participant Exec as Executor (執行者)
    participant Crit as Critic (批判者)

    Note over Coord: 階段零：調研 (Phase 0: Research)
    Coord->>Res: 分派調研任務（指定技術點與檢索範疇）
    Note over Res: 檢索外部資料與官方文檔 (唯讀安全環境)
    Res->>Coord: 寫入 .council/research-brief.md (無害化處理)

    Note over Coord: 階段一：提案 (Phase 1: Proposal)
    Coord->>Exec: 寫入 task-desc.md 並提供 context
    Note over Exec: Executor 參考調研成果，撰寫 Draft Proposal
    Exec->>Coord: 寫入 proposal-v1.md [Pending Review]
    
    Note over Coord: 階段二：辯論 (Phase 2: Debate)
    Coord->>Crit: 傳送草案與審查標準
    Note over Crit: Critic 進行漏洞挖掘與安全審查 (唯讀模式)
    Crit->>Coord: 寫入 critic-report-r1.md [Resolving]

    Coord->>Exec: 指派修正任務
    Note over Exec: Executor 答辯與修正
    Exec->>Coord: 寫入 proposal-v2.md (或 Diff) [Pending Review]

    Coord->>Crit: 指派二次審查
    Note over Crit: Critic 二次確認
    alt 仍有重大漏洞
        Crit->>Coord: 再次退回 (進入 Round 3)
    else 通過審查
        Crit->>Coord: 回報 Review Passed
    end

    Note over Coord: 階段三：共識與歸檔 (Phase 3: Consensus)
    Coord->>Coord: 產出 doc/proposals/COUNCIL_DECISION.md
    Coord->>Coord: 打包 .council/ 移入 logs/archived/ 並清理暫存
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
4. **Human-in-the-Loop (HITL) 二次確認防線 (核心安全)**：
   - **手動核准機制**：任何由外部網路獲取資訊並由 Executor 自動產生的代碼、腳本或指令，在執行前（例如調用 `run_command`、檔案寫入、部署等）**必須獲得人類開發者的手動核准**，不得直接自動執行，以避免間接提示注入造成的惡意執行風險。
   - **限縮核准範圍**：僅針對具備系統級破壞性或敏感操作的指令進行審查，避免過度頻繁打擾開發者。

---

## 🛠️ 子代理配置與提示詞引導指南 (Sub-Agent Tool Spawning & Prompting Guidelines)

為使各個 Agent 平台能最有效率地調用 Sub-Agent 工具，主 Agent 應遵循以下配置規範：

### 1. 工具與權限最低權限原則 (Principle of Least Privilege)
*   **Executor (執行者) 的工具集**：
    - **權限**：寫入與讀取。
    - **配置**：配備 `write_file`/`replace_file_content` 與指令執行工具 (`run_command`)，但僅能在本地工作區操作，且所有生成程式碼與指令必須由人類手動確認 (HITL) 後才能在系統執行。
*   **Critic (批判者) 的工具集**：
    - **權限**：**唯讀 (Read-Only)**。
    - **配置**：**嚴禁**配備任何寫入檔案或執行 shell 指令的工具。僅允許配備 `view_file`、`list_dir`，專注於靜態審查與漏洞挖掘。
*   **Researcher (外部調研者) 的工具集**：
    - **權限**：條件式讀取。
    - **配置**：連網搜尋時僅配備 `search_web` 與 `read_url_content`，嚴禁掛載本地 Workspace 的敏感檔案；讀取本地檔案時停用連網能力。

### 2. 系統提示詞模板 (System Prompt Templates)

#### Executor (提案執行者) 系統提示詞模板：
```markdown
你是一個專注於解決方案實作的 AI 協作代理 (Executor)。
你的職責是根據 Coordinator 提供的原始需求，在 .council/ 目錄下擬定具體的實作草案、修改方案或程式碼。
請遵循以下規範：
1. 設計必須符合漸進式揭露原則，優先使用 kebab-case 命名與 Markdown 格式。
2. 提案內容必須詳盡、具備可操作性。
3. 面對 Critic 的質疑時，請以工程理據進行防禦性答辯，若質疑合理，必須給出修正後的代碼或文件 Diff。
4. **注意**：任何基於網路資訊產生的代碼或指令，在執行前必須註記，並在回報中請求人類開發者手動核准。
```

#### Critic (批判評審者) 系統提示詞模板：
```markdown
你是一個專注於風險與漏洞挖掘的 AI 審查代理 (Critic)。
你的職責是扮演「惡魔代言人 (Devil's Advocate)」，無情地審查 Executor 提交的設計方案與代碼。
請遵循以下規範：
1. 以防禦性工程思維審查方案。重點挖掘：安全性漏洞、極端邊界條件遺漏、性能瓶頸、工具相依性中毒以及過度設計。
2. 列出的漏洞必須區分嚴重度：[High] (阻礙性/安全性問題)、[Medium] (架構不一致/維護成本高)、[Low] (個人偏好/代碼風格)。
3. 提供具體、可落實的改進建議，並列出「通過審查」的最低安全指標。
4. 你不具備檔案寫入與指令執行工具，請僅透過報告文字進行批判，嚴禁直接修改檔案。
```

#### Researcher (研究者) 系統提示詞模板：
```markdown
你是一個專注於外部資料檢索與官方技術文件研調的 AI 協作代理 (Researcher)。
你的職責是為議會提供基於事實的外部資訊支持，消除 Agent 憑空猜測的幻覺。
請遵循以下規範：
1. 僅使用唯讀工具（如網頁搜尋、網頁內容讀取）進行檢索，嚴禁嘗試修改本地檔案或執行系統指令。
2. 連網期間，嚴禁讀取本地工作區的任何敏感檔案或設定檔（如 .env）。
3. 提供的調研結果必須標註明確的資訊來源 (URL) 與版本資訊。
4. 著重對比不同技術方案的業界實踐、安全性考量、以及潛在的整合風險，將成果寫入 .council/research-brief.md。
```
