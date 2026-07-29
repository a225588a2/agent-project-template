# Skill 庫架構規範 (Skill Library Specification)

本目錄 ([[skills/]]) 為專案的 **技能庫與專業 SOP 車間**，存放各類高階作業流程、決策機制與領域 SOP (Standard Operating Procedures)。AI Agent 或開發者可在特定情境下按需檢索、觸發與載入對應 Skill。

---

## 📁 結構與命名規範 (Directory & File Structure)

每個 Skill 獨立存放於 `skills/` 下的子目錄，並統一以 **`SKILL.md`** 作為主要指引檔案：

```text
skills/
├── README-SKILLS.md        # 本規範文件
├── council/                # 討論議會與多 Agent 協作 Skill
│   └── SKILL.md            # Council 技能核心指引 (YAML Frontmatter + Markdown)
└── <skill-name>/           # 其他專屬技能目錄 (kebab-case)
    ├── SKILL.md            # 技能主要規範 (必要)
    └── references/         # (可選) 輔助參考文件或範本
```

---

## 📝 SKILL.md 格式規範 (Format Specification)

每個 `SKILL.md` **必須** 以標準的 **YAML Frontmatter** 開頭，定義該 Skill 的名稱、簡述與觸發條件 (Triggers)，隨後接 Markdown 指引與作業 SOP。

### 格式範例：

```markdown
---
name: skill-name
description: 簡短描述本 Skill 的用途與適用場景。
triggers:
  - 觸發關鍵字 1
  - 觸發關鍵字 2
  - 適用情境 (如 T3 重大決策)
---

# Skill 標題 (Markdown 指引開始)

## 核心理念與適用情境
...

## 執行步驟與 SOP
...
```

### 關鍵欄位說明：
- **`name`**：Skill 的唯一識別名稱 (建議與子目錄名一致，使用 kebab-case)。
- **`description`**：精簡說明該 Skill 的職責，幫助 Agent 快速判斷是否需要載入。
- **`triggers`**：觸發清單。當 Agent 在會話、任務需求或決策分級中遇到這些關鍵字/情境時，應主動載入並執行該 Skill。

---

## 🔄 Agent 發現與觸發機制 (Discovery & Triggering)

1. **熱啟動掃描 (Stage 2)**：Agent 於會話啟動時了解 `skills/` 目錄結構。
2. **按需觸發 (On-Demand Triggering)**：
   - 當面臨 **T3 重大決策** 時，主動觸發並載入 [[skills/council/SKILL.md]]。
   - 當任務符合某些 `triggers` 關鍵字時，主動讀取對應 Skill 指引檔案。
