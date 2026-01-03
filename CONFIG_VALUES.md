# GitHub Secrets 設定值

## 已確認的設定值

### CHANNEL_ACCESS_TOKEN
```
g+KcmhaZeUrdd+rwZnCNMTDWwJzT7Vwnkkksl0UFcDdiF3dGr41zPZy6YR7OXLqEf167GuCIgEaj0qVtmwrRa5LMSaNVwp2j4vQMKTRAW+qi2nyo+6ECsOhFwhzhzahTLrjnXCxCFVZ3qbp9qpwt3QdB04t89/1O/w1cDnyilFU=
```

**驗證狀態**: ✅ 有效
- Bot 名稱: Goldprice
- Bot ID: U9ef1e4477554739d333bb321576dde1f

### USER_ID
```
U39ae43e351f819abaef6083d27d3369e
```

**驗證狀態**: ✅ 有效
- 測試訊息已成功發送

## 更新 GitHub Secrets 的方法

### 方法 1: 手動更新（推薦）

1. 前往 GitHub 倉庫設定頁面：
   https://github.com/cty2014/gold-price-line-alter/settings/secrets/actions

2. 更新以下 Secrets：
   - **CHANNEL_ACCESS_TOKEN**: 貼上上面的 Token
   - **USER_ID**: 貼上上面的 User ID

3. 點擊 "Update secret" 保存

### 方法 2: 使用 GitHub API 自動更新

1. 前往 https://github.com/settings/tokens
2. 創建一個有 'repo' 權限的 Personal Access Token
3. 執行以下命令：

```bash
export GITHUB_TOKEN='您的_GITHUB_TOKEN'
python3 update_github_secrets.py
```

## 驗證設定

設定完成後，可以執行以下命令驗證：

```bash
export CHANNEL_ACCESS_TOKEN='g+KcmhaZeUrdd+rwZnCNMTDWwJzT7Vwnkkksl0UFcDdiF3dGr41zPZy6YR7OXLqEf167GuCIgEaj0qVtmwrRa5LMSaNVwp2j4vQMKTRAW+qi2nyo+6ECsOhFwhzhzahTLrjnXCxCFVZ3qbp9qpwt3QdB04t89/1O/w1cDnyilFU='
export USER_ID='U39ae43e351f819abaef6083d27d3369e'
python3 verify_line_config.py
```

## 最後更新時間

- Channel Token 驗證時間: 2024年（已通過驗證）
- User ID 驗證時間: 2024年（已通過驗證，測試訊息已發送）

