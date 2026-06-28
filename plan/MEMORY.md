# 專案執行紀錄與決策歷史 (Memory)

本文件用於詳細記錄專案的執行軌跡、重大技術/架構決策以及每日的變更歷史。紀錄應依時間順序「由舊到新，由上到下」累積。

每筆紀錄的標題與格式應與 Git Commit 的標題保持一致，以便於日後追溯。

---

## 2026/06/11 (範例日期)

### 20260611-1 專案初始化與結構搭設

**變更摘要**：
- 建立了核心目錄結構（`plan/`、`doc/`、`structure/`）。
- 建立了基礎工作規範文件 `plan/AGENT.md` 與專案目標文件 `plan/TARGET.md`。
- 建立了通用的 `.gitignore` 與 `README.md`。

**重要決策與備忘**：
- 決定採用「核心必要（plan/doc/structure）+ 自由增減參考（source/test/scripts/logs/refer）」的目錄設計，以兼顧規範性與高度的專案適用性。
- 專案檔案命名全面導入 kebab-case，重要行為核心 Markdown 檔案使用 UPPER-CASE。

---

## 2026/06/12 (範例日期)

### 20260612-1 [簡述本次變更項目]

**變更摘要**：
- `[變更項目一]`
- `[變更項目二]`

**重要決策與備忘**：
- `[重大技術決定、參數微調理由或與使用者討論後的決策備忘]`

---

## 2026/06/28

### 20260628-1 Add Multi-Agent Council guidelines and Kanban Handoff Protocol

**變更摘要**：
- 建立了全新核心規範文件 `plan/COUNCIL.md`，定義了高預算與高難度任務時的討論議會流程與看板式交接機制。
- 修改了 `plan/AGENT.md`，串接 Sub Agent 啟動條件，並將 `plan/COUNCIL.md` 加入啟動閱讀清單與核心檔案範例。
- 更新了 `README.md`，將 `plan/COUNCIL.md` 加入核心目錄描述與三階段 Quick Start 中。
- 更新了 `plan/PROCESS.md`，將本里程碑標記為已完成。

**重要決策與備忘**：
- 引進 **Hermes Agent** 的看板管理理念，透過 Kanban 狀態防範無條理群聊導致的認知混亂。
- 借鏡 **OpenClaw** 與 **Claude** 的隔離設計，明確規定 Sub Agent 工作區與上下文隔離規則，減少認知負載與 Token 消耗。
- 設計了主 Agent（協調者）、執行者（Executor）、批判者（Critic）與特化專家的三方協同流程。
