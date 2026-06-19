# 系統流程與時序圖模板 (Diagrams)

本文件使用圖表詳細描繪系統的動態執行流程、資料流向以及各組件之間的時序互動關係。

---

## 1. 核心業務執行流程圖 (Process Flowchart)

> [說明：使用 Mermaid `graph` 流程圖展示業務運作或資料處理的各個階段與分支判定]

```mermaid
graph TD
    Start([開始執行]) --> ReadConfig[1. 載入本機配置檔]
    ReadConfig --> ScanDir[2. 掃描目錄檔案]
    
    ScanDir --> CheckStale{3. 檢測資料是否變更?}
    CheckStale -- 是 --> RunProcess[4. 執行增量資料處理]
    CheckStale -- 否 --> ReturnCache[5. 直接自本機快取讀取]
    
    RunProcess --> WriteCache[6. 回寫新結果至快取]
    WriteCache --> Output[7. 輸出結果與報告]
    ReturnCache --> Output
    
    Output --> End([結束])
```

---

## 2. 跨組件時序互動圖 (Sequence Diagram)

> [說明：使用 Mermaid `sequenceDiagram` 展示當使用者或排程觸發特定事件時，多個組件/角色之間的動態呼叫關係]

```mermaid
sequenceDiagram
    autonumber
    actor User as 使用者/觸發源
    participant UI as 互動介面 (UI/Script)
    participant Engine as 處理引擎 (Engine)
    participant Storage as 存儲組件 (Storage/DB)
    participant External as 外部服務 (API/Service)
    
    User->>UI: 1. 輸入參數並按下執行
    UI->>Engine: 2. 啟動處理常式 run_process(params)
    
    rect rgb(240, 248, 255)
        Note over Engine, Storage: 本機快速比對階段
        Engine->>Storage: 3. 查詢是否存在本機快取
        Storage-->>Engine: 回傳快取數據 (或無快取)
    end
    
    opt 當本機無快取或資料過期時
        Engine->>External: 4. 向外部服務發送 API 請求
        External-->>Engine: 回傳最新結果數據
        Engine->>Storage: 5. 更新本地存儲與快取時間 (TTL)
    end
    
    Engine->>Engine: 6. 執行計分與結果排序
    Engine-->>UI: 7. 回傳最終排序與篩選後的結果列表
    UI-->>User: 8. 於畫面上渲染結果 (或輸出至報告檔案)
```
