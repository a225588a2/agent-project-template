# 資料與配置規格書模板 (Data Schema)

本文件詳細定義專案中所有資料存儲媒介的結構設計，包含關係型資料表 (DDL)、NoSQL、快取快照、外部配置檔格式 (JSON/YAML) 等。

---

## 1. 資料庫表結構設計 (Database Schema / DDL)

> [說明：如果專案有使用資料庫（如 SQLite, PostgreSQL 等），請在此列出資料表結構與索引設計]

### 資料表：`[表名稱，例如：files]`
- **職責**：`[記錄目錄下所有同步的檔案基本屬性]`
- **建表 SQL (DDL)**：
  ```sql
  CREATE TABLE IF NOT EXISTS files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      path TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      size INTEGER NOT NULL,
      mtime REAL NOT NULL,
      is_active INTEGER DEFAULT 1
  );
  ```
- **索引設計 (Indexes)**：
  - `idx_files_path` (ON `path`)：加速基於檔案路徑的單條或範圍查詢。

---

## 2. 外部配置檔案格式 (Configuration Format)

> [說明：如果專案有本機設定檔（如 config.json, settings.yaml），請在此列出其欄位定義與範例]

- **檔案路徑**：`[例如：根目錄/config.json]`
- **JSON 配置範例**：
  ```json
  {
    "debug_mode": false,
    "last_selected_root": "",
    "max_results_limit": 100,
    "processing_rules": {
      "ignore_patterns": ["*.tmp", "~$*"],
      "timeout_seconds": 30
    }
  }
  ```
- **欄位說明**：
  - `debug_mode` (Boolean)：是否開啟全域詳細日誌輸出。
  - `last_selected_root` (String)：上次使用者選擇並載入的工作根目錄。
  - `processing_rules.ignore_patterns` (Array)：資料同步與掃描時要自動忽略的 Glob 通配符列表。

---

## 3. 暫存與快取機制 (Caching & TTL)

> [說明：定義快取（如記憶體暫存、Redis 或資料庫快取表）的過期策略與更新機制]
>
> - **快取更新策略**：`[說明，例如：當檔案的修改時間 (mtime) 變更時，立即將對應的特徵快取標記為過期 (is_stale=1)，並於背景重新計算]`
> - **生存時間 (TTL)**：`[說明，例如：暫存資料預設保存 90 天，過期後由垃圾回收機制 (GC) 自動刪除]`
