# 黃金價格監控系統

自動監控黃金現貨價格，並透過 LINE Bot 發送通知。

## 功能

- 每 10 分鐘檢查一次黃金價格（透過 GitHub Actions）
- 每次執行都發送每日黃金價格報告
- 使用鉅亨網 API 獲取價格數據

## GitHub Actions 設定

### 1. 設定 Secrets

在 GitHub 倉庫設定中，前往 **Settings → Secrets and variables → Actions**，新增以下 Secrets：

- `CHANNEL_ACCESS_TOKEN`: LINE Bot 的 Channel Access Token
- `USER_ID`: LINE User ID

### 2. 手動觸發測試

1. 前往 https://github.com/cty2014/gold-price-line-alter/actions
2. 選擇 "黃金價格監控" workflow
3. 點擊 "Run workflow" 按鈕手動觸發

### 3. 檢查執行狀態

- 在 Actions 頁面查看 workflow 運行狀態
- 點擊執行記錄查看詳細日誌
- 確認是否有錯誤訊息

## 報告格式

```
📊 每日黃金價格報告
報告時間: 2025-12-31 17:37:04
日期: 2025-12-31
當前價格: $4274.00
-------------------
當天最高: $4274.00
當天最低: $4274.00
波動幅度: 0.00%
```

## 本地測試

```bash
# 設定環境變數
export CHANNEL_ACCESS_TOKEN="您的_TOKEN"
export USER_ID="您的_USER_ID"

# 執行
python3 main.py
```

## 檔案說明

- `main.py`: 主程式
- `get_gold_price.py`: 價格獲取功能（使用鉅亨網 API）
- `line_notify.py`: LINE 通知功能
- `.github/workflows/gold-price-check.yml`: GitHub Actions workflow 設定

