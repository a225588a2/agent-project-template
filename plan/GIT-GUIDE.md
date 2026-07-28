# Git 操作與發布規範指引 (Git Guide - v2.0)

本文件定義本專案之版本控制、Git Commit 規範、雙軌版本策略與 Git Hook 驗證機制。

---

## 1. 作者簽名與身份規範 (Author Signature)

本專案要求所有 Commit 必須具備明確的作者簽名，防止提交身份混亂：
- 於專案初始化時，`python scripts/bootstrap.py` 會自動檢查並引導配置。
- 手動配置指令：
  ```bash
  git config user.name "Your Name"
  git config user.email "your.email@example.com"
  ```

---

## 2. 雙軌版本策略規範 (Dual Versioning Strategy)

本專案支援 **雙軌版本模式**，於專案初始化 (`bootstrap.py`) 時鎖定寫入 `.sync-state.json`：

### 模式 A：SemVer 2.0 語意化版本 (適用於程式碼/軟體/套件專案)
- **版本號格式**：`vMAJOR.MINOR.PATCH[-PRERELEASE]` (例如 `v1.0.0`, `v1.2.3`)
- **Commit 標題格式**：**Conventional Commits** (`<type>(<scope>): <summary>`)
  - *合法 Type*：`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
  - *範例*：`feat(core): implement semver version engine`
- **Commit 規範**：Header 強制規範 (Conventional Commits)，Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。
- **分支模型**：**Gitflow 雙主線 (`main` + `develop` + 主題分支 `feature/*`)**
  - `main` 分支上每個 Commit 點必須對應一個發布 Tag。
  - `develop` 合併至 `main` 時建議強制使用 `git merge --no-ff` 並附帶 Release Summary。

### 模式 B：CalVer 日期導向版本 (適用於筆記/日誌/資料專案)
- **版本號格式**：`vYYYY.MM.DD` 或 `v1.0.YYYYMMDD.Z` (例如 `v1.0.20260728.1`)
- **Commit 標題格式**：以版本號開頭加上摘要 (`v1.0.20260728.1 Summary`)
- **Commit 規範**：Header 強制規範 (CalVer 前綴)，Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。
- **分支模型**：**輕量單主線 (`main` + 隨選分支)**，允許直接提交至 `main`。

---

## 3. Git Hook 自動驗證與修復機制

專案配置了 `pre-commit` 與 `commit-msg` Git Hooks（位於 `.git/hooks/`）：

### 驗證規則
1. **版號一致性**：確保 `plan/PROCESS.md`、`plan/cold-history.log` 與 `.sync-state.json` 的版號一致。
2. **Commit Header 格式**：依選定策略檢查 Header 正則 (Conventional Commits / CalVer 前綴)。
3. **Commit Body 說明**：Body 不限制/允許使用中文說明 (Permitted CJK, not forced)。

### 💡 自我糾錯限制 (Self-Correction Cap)
- 若提交遭到 Git Hook 攔截，AI Agent 最多執行 **2 次修復重試**。
- 若連續 2 次修正仍失敗，必須加上 `--no-verify` 參數執行 `WIP` 提交（如 `git commit -m "WIP" --no-verify`），並即刻暫停轉交 HITL 人工介入除錯。
