# 黃金價格監控系統

[![黃金價格監控](https://github.com/cty2014/gold-price-line-alter/actions/workflows/gold-price-check.yml/badge.svg)](https://github.com/cty2014/gold-price-line-alter/actions/workflows/gold-price-check.yml)

自動監控黃金現貨價格，並透過 LINE Bot 發送通知。

## 功能

- **每日報告**：每天固定時間發送一次黃金價格報告（UTC 06:30，台灣時間 14:30）
- **波動警報**：每小時檢查一次，如果當天價格波動超過 5% 會立即發送通知
- **智能通知**：避免重複發送，每天最多發送一次每日報告
- **優先使用 GoldAPI.io API** 獲取價格數據，失敗時自動切換到備用 API（鉅亨網）

## GitHub Actions 設定

### 1. 設定 Secrets

在 GitHub 倉庫設定中，前往 **Settings → Secrets and variables → Actions**，新增以下 Secrets：

- `CHANNEL_ACCESS_TOKEN`: LINE Bot 的 Channel Access Token
- `USER_ID`: LINE User ID
- `GOLDAPI_KEY`: GoldAPI.io API Key（選填，未設定時會使用備用 API）

#### 如何獲取 GoldAPI.io API Key

1. 前往 [GoldAPI.io 官網](https://www.goldapi.io/)
2. 註冊帳號並登入
3. 在控制台中獲取您的 API Key
4. 在 GitHub Secrets 中新增 `GOLDAPI_KEY`

**注意**：
- GoldAPI.io 提供即時黃金價格數據
- 如果未設定 API Key，程式會自動使用備用 API（鉅亨網）
- 請確認 API Key 有足夠的請求配額

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
export GOLDAPI_KEY="您的_API_KEY"  # 選填

# 執行
python3 main.py
```

## 檔案說明

- `main.py`: 主程式
- `get_gold_price.py`: 價格獲取功能（優先使用 GoldAPI.io API，備用鉅亨網 API）
- `line_notify.py`: LINE 通知功能
- `.github/workflows/gold-price-check.yml`: GitHub Actions workflow 設定
- `verify_line_config.py`: LINE Bot 設定驗證工具
- `get_user_id.py`: USER_ID 獲取輔助工具

