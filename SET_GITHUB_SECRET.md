# 設定 GitHub Secrets 指南

## GoldAPI.io API Key

**Secret 名稱**: `GOLDAPI_KEY`  
**Secret 值**: `goldapi-g2zyesmjucbyr3-io`

## 手動設定步驟

1. 前往您的 GitHub 倉庫：
   https://github.com/cty2014/gold-price-line-alter

2. 點擊 **Settings** → **Secrets and variables** → **Actions**

3. 點擊 **New repository secret**

4. 填寫：
   - **Name**: `GOLDAPI_KEY`
   - **Secret**: `goldapi-g2zyesmjucbyr3-io`

5. 點擊 **Add secret**

## 使用腳本自動設定（進階）

如果您有 GitHub Personal Access Token，可以使用腳本自動設定：

```bash
# 1. 獲取 GitHub Personal Access Token
# 前往 https://github.com/settings/tokens
# 創建一個有 'repo' 權限的 Token

# 2. 設定環境變數
export GITHUB_TOKEN='您的_GITHUB_TOKEN'

# 3. 安裝依賴（如果需要）
pip install PyNaCl requests

# 4. 執行腳本
python3 set_github_secret.py
```

## 驗證設定

設定完成後，可以：

1. 前往 Actions 頁面
2. 手動觸發 workflow
3. 查看執行日誌，確認 API Key 是否正確讀取

