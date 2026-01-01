# 檢查 GitHub Secrets 設定指南

## 需要設定的 Secrets

您的 GitHub Actions workflow 需要以下三個 Secrets：

1. **CHANNEL_ACCESS_TOKEN** - LINE Bot 的 Channel Access Token
2. **USER_ID** - LINE User ID  
3. **GOLDAPI_KEY** - GoldAPI.io API Key

## 檢查方法

### 方法 1：透過 GitHub 網頁檢查

1. 前往您的 GitHub 倉庫：
   https://github.com/cty2014/gold-price-line-alter

2. 點擊 **Settings** → **Secrets and variables** → **Actions**

3. 查看是否有以下 Secrets：
   - `CHANNEL_ACCESS_TOKEN`
   - `USER_ID`
   - `GOLDAPI_KEY`

### 方法 2：透過 GitHub Actions 執行日誌檢查

1. 前往 Actions 頁面：
   https://github.com/cty2014/gold-price-line-alter/actions

2. 點擊最近的執行記錄

3. 查看 "執行價格檢查" 步驟的日誌，應該會顯示：
   ```
   ✓ CHANNEL_ACCESS_TOKEN 已設定
   ✓ USER_ID 已設定
   ✓ GOLDAPI_KEY 已設定
   ```

## 如果 Secrets 未設定

### 設定 CHANNEL_ACCESS_TOKEN

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇您的 Channel (Goldprice)
3. 在 Messaging API 頁面獲取 Channel Access Token
4. 在 GitHub Secrets 中新增：
   - Name: `CHANNEL_ACCESS_TOKEN`
   - Value: `您的_TOKEN`

### 設定 USER_ID

1. 確保用戶已加入 LINE Bot 為好友
2. 透過 Webhook 事件或 LINE Official Account Manager 獲取 USER_ID
3. 在 GitHub Secrets 中新增：
   - Name: `USER_ID`
   - Value: `U39ae43e351f819abaef6083d27d3369e`（您的實際 USER_ID）

### 設定 GOLDAPI_KEY

1. 前往 [GoldAPI.io](https://www.goldapi.io/)
2. 註冊並獲取 API Key
3. 在 GitHub Secrets 中新增：
   - Name: `GOLDAPI_KEY`
   - Value: `goldapi-g2zyesmjucbyr3-io`（您的實際 API Key）

## 快速檢查腳本

您可以使用以下命令檢查本地環境變數（僅用於測試）：

```bash
echo "CHANNEL_ACCESS_TOKEN: $([ -z "$CHANNEL_ACCESS_TOKEN" ] && echo '未設定' || echo '已設定')"
echo "USER_ID: $([ -z "$USER_ID" ] && echo '未設定' || echo '已設定')"
echo "GOLDAPI_KEY: $([ -z "$GOLDAPI_KEY" ] && echo '未設定' || echo '已設定')"
```

## 注意事項

- GitHub Secrets 是加密儲存的，無法直接查看內容
- 只能確認 Secret 是否存在，無法查看實際值
- 如果 Secret 未設定，GitHub Actions 執行時會顯示錯誤訊息



