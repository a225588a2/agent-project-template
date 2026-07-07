# Git 版本控制指引 (Git Guide)

本文件採用「階段式揭露」設計，**日常工作中無需主動翻閱**。僅在以下情境發生時，才需要查閱對應章節：

| 查閱時機 | 對應章節 |
| :--- | :--- |
| 首次初始化專案的 Git 儲存庫 | §1 |
| 遇到 Git 操作錯誤或衝突 | §2 |
| 需要進行分支操作或合併策略 | §3 |
| 需要調整 `.gitignore` 排除規則 | §4 |
| 需要回退、撤銷或修改歷史 Commit | §5 |

---

## 1. 初始化準則 (Initialization)

- 專案初始化時，先確認根目錄已存在 `.gitignore`（本模板已預先提供）。
- 首次 Commit 標題建議為：`20260618-1 Initialize project structure`。
- 若從模板複製而來，首次 Commit 應包含所有模板檔案，作為專案的「零點快照」。

---

## 2. 錯誤處理與衝突解決 (Error Handling & Conflict Resolution)

### 合併衝突 (Merge Conflict)
- 優先保留**最新且經過驗證的版本**，而非盲目選擇「ours」或「theirs」。
- 衝突解決後，在 Commit 描述中明確標註衝突的檔案與選擇的策略。
- 若衝突涉及 `plan/` 下的文件（如 PROCESS.md 或 MEMORY.md），應合併雙方內容而非覆蓋，因為這些檔案的紀錄是累積式的。

### 常見錯誤處理
- **`fatal: not a git repository`**：確認目前工作目錄是否正確，或是否已執行 `git init`。
- **`error: failed to push some refs`**：先執行 `git pull --rebase` 同步遠端，解決衝突後再推送。
- **大檔案警告**：若 Git 警告檔案過大（>100MB），應將該檔案類型加入 `.gitignore`，或使用 Git LFS。
- **遇到無法自行判斷的 Git 錯誤時**：將完整錯誤訊息回報給使用者，由使用者決定處理方式（屬於 T3 決策）。

---

## 3. 分支策略 (Branching Strategy)

- **預設策略**：小型專案直接在 `main` 分支工作即可，無需過度設計分支流程。
- **功能分支**：當專案規模增長或有多人/多 Agent 協作時，建議採用功能分支：
  - 分支命名格式：`feature/{簡短英文描述}`，例如 `feature/add-search-engine`。
  - 完成後合併回 `main` 並刪除功能分支。
- **何時該建立分支（T2 知會即可）**：
  - 預計進行大規模重構或實驗性嘗試時。
  - 使用者明確要求「先在分支上做」時。
- **何時不需要分支（T1 自主決定）**：
  - 小幅修正、文件更新、Bug 修復等可輕易撤銷的變更。

---

## 4. .gitignore 管理準則

- 本模板已預先提供通用的 `.gitignore`，涵蓋 Python 虛擬環境、IDE 暫存、本機資料庫與日誌等。
- **新增排除規則時**：將新規則加入對應的分類區塊（程式/資料/日誌），並附上簡短註解說明理由。
- **特定檔案需要排除忽略時**：使用驚嘆號語法 `!FileName` 強制追蹤，並在旁邊註解為何此檔案例外。
- 避免將整個資料目錄（如 `Refer/`）加入 `.gitignore`——應針對具體的大型檔案類型進行排除。

---

## 5. 回退與撤銷操作指引 (Revert & Undo)

> ⚠️ **回退操作屬於 T3 決策**——在執行任何破壞性的歷史修改前，必須與使用者確認。

### 撤銷最近的未提交變更
- 撤銷單一檔案：`git checkout -- <file>`
- 撤銷所有未提交變更：`git checkout -- .`

### 撤銷最近一次 Commit（保留變更）
- `git reset --soft HEAD~1`：撤銷 Commit 但保留修改在暫存區。
- 適用場景：Commit 訊息寫錯、遺漏了某個檔案。

### 完全回退到某個歷史版本
- `git reset --hard <commit-hash>`：**會丟失所有未提交的變更**，務必確認已備份。
- 使用前必須告知使用者即將丟失的內容範圍。

### 修改歷史 Commit 訊息
- 最近一次：`git commit --amend -m "new message"`
- 更早的 Commit：使用 `git rebase -i`，但**絕不對已推送至遠端的 Commit 進行 rebase**。

---

## 6. Git Hook 自動化驗證機制 (Git Hooks)

本專案配置了 `pre-commit` 與 `commit-msg` 提交攔截驗證機制，用以自動保證專案狀態與 Commit 品質。

### 驗證規則
- **同步檢核 (`pre-commit`)**：比對 `plan/PROCESS.md`、`logs/cold-history.log` 與 `.sync-state.json` 的版號，若未同步則阻擋提交。
- **Commit 訊息檢核 (`commit-msg`)**：
  - 強制 Commit 標題必須以當前同步版號為前綴，格式為 `vX.Y.YYYYMMDD.Z English Summary`。
  - 強制 Commit 訊息（標題與描述）只能使用英文（不允許中、日、韓 CJK 字元與全形標點）。

### 安裝方式
- **新建立專案**：使用 `scripts/bootstrap.py` 時會自動安裝。
- **手動/重新安裝**：在專案根目錄執行 `python scripts/install_hooks.py` 即可。

### 繞過驗證 (Bypass)
- 若有臨時或 WIP 備份需求，必須在 commit 時加入 `--no-verify`（例如 `git commit -m "WIP" --no-verify`）來繞過 Hook 驗證。
