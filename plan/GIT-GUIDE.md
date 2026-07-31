# Git 操作與發布規範指引 (Git Guide - v2.0)

本文件定義本專案之版本控制、Git Commit 規範、雙軌版本策略與 Git Hook 驗證機制。

---

## 1. 作者簽名與身份規範 (Author Signature)

本專案要求所有 Commit 必須具備明確的作者簽名，防止提交身份混亂：
- 於專案初始化時，[[scripts/bootstrap.py]] 會自動檢查並引導配置。
- 手動配置指令：
  ```bash
  git config user.name "Your Name"
  git config user.email "your.email@example.com"
  ```

---

## 2. 雙軌版本策略規範 (Dual Versioning Strategy)

本專案支援 **雙軌版本模式**，於專案初始化 ([[scripts/bootstrap.py]]) 時鎖定寫入 `.sync-state.json`：
- **未選定機制清理規範 (Unselected Mechanism Cleanup Rule)**：於專案初始化 ([[scripts/bootstrap.py]]) 完成特定 Git 維護機制（SemVer 2.0 或 CalVer）選擇後，必須明確移除未選定機制之相應設定、邏輯與說明檔，確保專案僅保留所選定之單一維護機制。

<!-- @KEEP:SEMVER -->
### 模式 A：SemVer 2.0 語意化版本 (適用於程式碼/軟體/套件專案)
- **版本號格式**：`vMAJOR.MINOR.PATCH[-PRERELEASE]` (例如 `v1.0.0`, `v1.2.3`)
- **進版條件對照**：

| 層級    | 遞增時機                 | 典型觸發                   |
| ----- | -------------------- | ---------------------- |
| MAJOR | 不向下相容的架構重構或 API/協定變更 | 全面重構、破壞性介面改動           |
| MINOR | 新增向下相容的功能或模組         | `feat` 類型 Commit       |
| PATCH | 向下相容的修復、優化或純文件修訂     | `fix`、`docs` 類型 Commit |
  
- **Commit 標題格式**：**Conventional Commits** (`<type>(<scope>): <summary>`)
  - *合法 Type*：`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
  - *範例*：`feat(core): implement semver version engine`
- **Commit 規範**：Header 強制規範 (Conventional Commits)，Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。
- **分支模型**：**Gitflow 雙主線 (`main` + `develop` + 主題分支 `feature/*`)**
  - ⚠️ **main 分支不變律**：`main` 上的每個 Commit 點**必須且只能**對應一個發布 Tag（如 `v1.0.0`）。建立 Tag 時**必須**使用附註標籤 (`git tag -a vX.X.X -m "..."`)，並在訊息中清楚條列該版本的重點改進內容 (Release Notes)。日常開發嚴禁推進無 Tag 的 Commit 至 `main`。
  - ⚠️ **強制 `--no-ff` 合併**：`develop` 合併至 `main` 時**必須**使用 `git merge --no-ff`，並在 Merge Commit 訊息中條列本版本的變動摘要 (Release Summary)。
  - ⚠️ **維持雙主線同步 (Fast-forward develop)**：當 `develop` 成功 `--no-ff` 合併至 `main` 且發布完成後，**必須立即**將 `develop` 切換並快進 (`git checkout develop && git merge main --ff-only`) 至 `main` 的最新 HEAD。這可確保下次在 `develop` 上的 Commit 能維持 Git Tree 完美的拱門結構。
- **主題分支生命週期**：
  1. 從 `develop` 切出（`git checkout -b <type>/<short-name> develop`）
  2. 完成開發並通過 DoD 驗證（參照 [[plan/AGENT.md]] §5）
  3. 以 `--no-ff` 合併回 `develop`
  4. 本地清理（`git branch -d <type>/<short-name>`，若 `-d` 失敗禁止使用 `-D` 強刪，參照 [[plan/AGENT.md]] §6）
<!-- @END:SEMVER -->

<!-- @KEEP:CALVER -->
### 模式 B：CalVer 日期導向版本 (適用於筆記/日誌/資料專案)
- **版本號格式**：`vYYYY.MM.DD` 或 `v1.0.YYYYMMDD.Z` (例如 `v1.0.20260728.1`)
- **Commit 標題格式**：以版本號開頭加上摘要 (`v1.0.20260728.1 Summary`)
- **Commit 規範**：Header 強制規範 (CalVer 前綴)，Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。
- **分支模型**：**輕量單主線 (`main` + 隨選分支)**，允許直接提交至 `main`。
<!-- @END:CALVER -->

---

## 3. Git Hook 自動驗證與修復機制

專案配置了 `pre-commit` 與 `commit-msg` Git Hooks（位於 `.git/hooks/`）：

### 驗證規則
1. **版號一致性**：確保 [[plan/PROCESS.md]]、[[plan/cold-history.log]] 與 `.sync-state.json` 的版號一致。
<!-- @KEEP:SEMVER -->
2. **Commit Header 格式**：檢查 Conventional Commits 正則。
<!-- @END:SEMVER -->
<!-- @KEEP:CALVER -->
2. **Commit Header 格式**：檢查 CalVer 前綴正則。
<!-- @END:CALVER -->
3. **Commit Body 說明**：Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。

### 💡 自我糾錯限制 (Self-Correction Cap)
- 若提交遭到 Git Hook 攔截，AI Agent 最多執行 **2 次修復重試**。
- 若連續 2 次修正仍失敗，必須加上 `--no-verify` 參數執行 `WIP` 提交（如 `git commit -m "WIP" --no-verify`），並即刻暫停轉交 HITL 人工介入除錯。

---

## 4. 歷史維護與回退速查 (History Hygiene & Quick Recovery)

- **乾淨主線**：避免大量零碎 Commit 留存主線，必要時以 `git rebase -i` 或 squash 整合為語意明確的單一 Commit。
- **舊歷史封存**：大規模重構或階段切換時，使用語意化 Tag 封存舊歷史（如 `archive/v1.x-legacy`）。
- **常用回退操作**：

| 情境 | 指令 | 備註 |
|------|------|------|
| 撤銷未暫存的檔案變更 | `git checkout -- <file>` | 僅影響工作目錄 |
| 修改最近一次 Commit 訊息 | `git commit --amend` | 僅限尚未 push 的 Commit |
| 對已 push 的歷史做 rebase/reset | 需經 T3 決策流程 | 參照 [[plan/AGENT.md]] §3.1 取得使用者授權 |
