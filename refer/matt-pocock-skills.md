# Matt Pocock Agent Skills 參考指南

## 狀態說明 (Submodule Decoupled)

本專案原以 Git Submodule 形式引入於 `refer/matt-pocock-skills`，現已**正式解耦並移除子模組連結**。
此舉旨在降低專案體積與維護複雜度，避免子模組版本指針與 CI/CD 異常，改以外部文件化方式提供指引與按需引用。

- **原始 GitHub 倉庫**：[mattpocock/skills (commit ed37663)](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d)
- **最新發布與社群工具**：[skills.sh](https://skills.sh/mattpocock/skills)

---

## 專案用途與核心理念 (Purpose & Principles)

Matt Pocock 的 Skills 集合專為 Claude Code、Codex 等現代編程 Agent 設計，核心宗旨是落實「真實工程實踐 (Real Engineering)」而非單純的意圖編碼 (Vibe Coding)。

其主要解決 Agent 開發過程中的四大常見失效模式 (Failure Modes)：

1. **需求與意圖錯位 (Misalignment)**：
   - 核心技能：`/grill-me`、`/grill-with-docs`
   - 機制：透過「詰問模式 (Grilling)」深入釐清使用者需求，確保在下筆寫代碼前已完全對齊分支情境。
2. **Agent 冗長與術語歧異 (Verbosity & Lack of Shared Language)**：
   - 核心理念：建立領域通用語言 (Ubiquitous Language)，收錄於 `CONTEXT.md` 與 ADR。
   - 機制：大幅縮減溝通與思考 Token 成本，提升 Agent 在專案中的專注度與代碼命名一致性。
3. **代碼無法正確執行 (Broken Code & Feedback Loops)**：
   - 核心技能：`/tdd`、`/diagnosing-bugs`
   - 機制：要求紅綠重構循環 (Red-Green-Refactor) 與科學化排錯迴圈 (重現 ➜ 最小化 ➜ 假設 ➜ 觀測 ➜ 修復 ➜ 回歸測試)。
4. **架構劣化與泥球系統 (Ball of Mud & Architecture Entropy)**：
   - 核心技能：`/improve-codebase-architecture`、`/to-spec`、`/codebase-design`
   - 機制：強調深模組設計 (Deep Modules) 與定期架構檢視，抑制 Agent 快速編碼帶來的熵增。

---

## 核心參考價值 (Key Reference Value for agent-project-template)

1. **SOP 技能庫架構參考**：本模板中的 `skills/` 設計精神與觸發機制，部分借鑑了其簡潔、可組合 (Composable) 且與特定模型無關的 Skill 規範。
2. **決策與詰問模式 (Grilling Protocol)**：可作為本模板 Council 議會機制與決策分級流程的極佳輔助手段。
3. **安裝與按需整合方式**：
   - 若未來專案需完整引入，建議透過 `npx skills@latest add mattpocock/skills` 或 Claude Code 插件市場 (`claude plugin install mattpocock-skills@mattpocock`) 動態按需安裝，無需綁定 Git Submodule。
