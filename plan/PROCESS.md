# 專案進度與開發計畫 (Process)

本文件用於記錄專案目前的開發/執行狀態、已完成的里程碑，以及後續各階段的 MVP 實作計畫與待辦事項 (ToDo List)。

---

## 目前狀態 (Current Status)

- **當前進度**：[階段 1 完成，成功落實雙軌版本未選定機制清理 (Cleanup Rule)、重寫 bootstrap.py，並強化 Git 雙主線同步紀律與 Agent 啟動護欄]
- **目前版本**：v1.0.4

---

## 已完成的里程碑 (Completed Milestones)

- [x] 建立通用專案骨架與必要核心目錄 ([[plan/]], [[doc/]], [[structure/]])。
- [x] 建立並導入多 Agent 討論議會與協作規範 [[skills/council/SKILL.md]]。
- [x] 實作 [[scripts/version_engine.py]] 策略模式版本引擎。
- [x] 重寫 [[scripts/bootstrap.py]]，完整落實「雙軌版本未選定機制清理」與條件標記 (HTML Comments) 渲染。
- [x] 強化 [[plan/AGENT.md]] 與 [[plan/GIT-GUIDE.md]] 護欄，強制 Agent 啟動前向使用者確認，並確立 `develop` 快進同步與 `main` 附註標籤 (Annotated Tag) 紀律。
- [x] 升級 [[scripts/sync_project.py]] 與 [[scripts/git_hook_validator.py]] 支援 Type A Markdown 靜態 quality checks 與 Conventional Commits (Body 許中文)。
- [x] 完成 Skill 庫架構建立與 Council Skill 化重構 ([[skills/council/SKILL.md]])。

---

## 分階段開發計畫與待辦項目 (Development Plan & ToDo List)

### 階段 0：結構定義與環境搭建 ✅ 完成
- [x] 初始化專案目錄與設定 `.gitignore`。
- [x] 定義工作規範 [[plan/AGENT.md]]。
- [x] 定義系統/專案目標 [[plan/TARGET.md]]。

### 階段 1：核心基礎實作與模板 v2.0 升級 ✅ 完成
- [x] 實作雙軌版本模式 (SemVer 2.0 vs CalVer)。
- [x] 實作 Type A Markdown 靜態品質關卡檢驗。
- [x] 導入 Git Author Signature 初始化設定流程。

### 階段 2：延伸功能與範例補充 🚀 進行中
- [ ] 導入改良內化後的 Matt Skills
- [ ] `[建立擴充模組之自動化單元測試範例]`
- [ ] `[補充多語言介面與國際化說明範本]`

---

## 未來優化與待辦項目 (Backlog / Future ToDo)

### 高優先級 (High Priority)
- [x] 導入雙軌版本模式與動態裝配策略。
- [x] 導入單一寫入者原則 (Single Writer Rule) 防範多 Sub-Agent 並行寫入覆蓋。

### 中優先級 (Medium Priority)
- [ ] 提供一鍵轉換舊版 CalVer 日期日誌至 SemVer 2.0 的獨立 Migration 腳本 ([[scripts/migrate_version_strategy.py]])。
