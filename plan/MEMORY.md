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

## 2026/06/19

### 20260619-1 Initialize project structure and templates

**變更摘要**：
- 完成通用專案模板升級與實務回饋整合（包含 AGENT.md、TARGET.md、README.md、doc/ 及 structure/ 模板更新）。
- 新增 `plan/GIT-GUIDE.md` 作為階段式揭露指引。
- 新增 `plan/FEEDBACK.md` 作為經驗回饋機制。

**重要決策與備忘**：
- 將專案模板初始化為 Git 儲存庫，並設定自訂 SSH 金鑰 `LaptopFork` 完成 GitHub 推送與託管。

---

## 2026/06/22

### 20260622-1 Change file naming conventions to kebab-case and UPPER-CASE

**變更摘要**：
- 全面將專案的目錄改為小寫（如 `plan/`、`doc/`、`structure/` 等）。
- 將重要行為核心 Markdown 檔案命名更改為全大寫（如 `README.md`、`TARGET.md`、`AGENT.md`、`PROCESS.md`、`MEMORY.md`、`GIT-GUIDE.md`、`FEEDBACK.md`）。
- 將一般規格模板與程式檔案命名更改為 `kebab-case`（如 `template-data-schema.md`、`template-exclusion-rules.md`、`template-functional-spec.md` 等）。
- 更新 `plan/AGENT.md` 的命名規範說明，並將所有檔案內部的連結路徑同步修正。

**重要決策與備忘**：
- 為了使專案更貼近現代專案與 LLM 處理的命名習慣，將命名邏輯由 UpperCamelCase 大駝峰法全面轉移至 kebab-case（一般程式碼/檔案）搭配 UPPER-CASE（核心政策/流程規範），以提升清晰度與一致性。


