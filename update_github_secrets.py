#!/usr/bin/env python3
"""
更新 GitHub Secrets 中的 CHANNEL_ACCESS_TOKEN 和 USER_ID
"""

import os
import sys
import base64
import requests

try:
    from nacl import encoding, public
except ImportError:
    print("錯誤: 需要安裝 PyNaCl 套件")
    print("請執行: pip install PyNaCl")
    sys.exit(1)


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """使用 GitHub 公鑰加密 Secret"""
    public_key_bytes = base64.b64decode(public_key)
    public_key_obj = public.PublicKey(public_key_bytes)
    sealed_box = public.SealedBox(public_key_obj)
    encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')


def get_repo_public_key(owner: str, repo: str, token: str):
    """獲取倉庫的公鑰"""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"獲取公鑰失敗: {response.status_code}")
        print(f"錯誤訊息: {response.text}")
        return None


def set_secret(owner: str, repo: str, secret_name: str, secret_value: str, token: str):
    """設定 GitHub Secret"""
    # 獲取公鑰
    public_key_data = get_repo_public_key(owner, repo, token)
    if not public_key_data:
        return False
    
    # 加密 Secret
    encrypted_value = encrypt_secret(public_key_data['key'], secret_value)
    
    # 設定 Secret
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_data['key_id']
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201 or response.status_code == 204:
        print(f"✓ 成功設定 Secret: {secret_name}")
        return True
    else:
        print(f"✗ 設定 Secret 失敗: {response.status_code}")
        print(f"錯誤訊息: {response.text}")
        return False


def main():
    """主函數"""
    print("=" * 60)
    print("更新 GitHub Secrets - CHANNEL_ACCESS_TOKEN 和 USER_ID")
    print("=" * 60)
    print()
    
    # 從 update_channel_token.py 讀取 Channel Token
    channel_token = None
    try:
        with open("update_channel_token.py", "r", encoding="utf-8") as f:
            import re
            content = f.read()
            match = re.search(r'channel_token\s*=\s*"([^"]+)"', content)
            if match:
                channel_token = match.group(1)
    except Exception as e:
        print(f"⚠️  無法從 update_channel_token.py 讀取 Token: {e}")
    
    # 如果沒有找到，使用預設值
    if not channel_token:
        channel_token = "g+KcmhaZeUrdd+rwZnCNMTDWwJzT7Vwnkkksl0UFcDdiF3dGr41zPZy6YR7OXLqEf167GuCIgEaj0qVtmwrRa5LMSaNVwp2j4vQMKTRAW+qi2nyo+6ECsOhFwhzhzahTLrjnXCxCFVZ3qbp9qpwt3QdB04t89/1O/w1cDnyilFU="
    
    # User ID
    user_id = "U39ae43e351f819abaef6083d27d3369e"
    
    # 從環境變數獲取 GitHub Token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("⚠️  需要設定 GITHUB_TOKEN 環境變數才能自動更新")
        print()
        print("方法 1: 手動設定（推薦）")
        print("1. 前往 https://github.com/cty2014/gold-price-line-alter/settings/secrets/actions")
        print("2. 更新以下 Secrets:")
        print()
        print("   CHANNEL_ACCESS_TOKEN:")
        print(f"   {channel_token}")
        print()
        print("   USER_ID:")
        print(f"   {user_id}")
        print()
        print("方法 2: 使用 GitHub API 自動設定")
        print("1. 前往 https://github.com/settings/tokens")
        print("2. 創建一個有 'repo' 權限的 Personal Access Token")
        print("3. 執行:")
        print("   export GITHUB_TOKEN='您的_GITHUB_TOKEN'")
        print("   python3 update_github_secrets.py")
        sys.exit(0)
    
    # 倉庫資訊
    owner = "cty2014"
    repo = "gold-price-line-alter"
    
    print(f"倉庫: {owner}/{repo}")
    print()
    print("準備更新以下 Secrets:")
    print(f"  - CHANNEL_ACCESS_TOKEN: {channel_token[:20]}...{channel_token[-20:]}")
    print(f"  - USER_ID: {user_id}")
    print()
    
    # 設定 Secrets
    success_count = 0
    total_count = 2
    
    # 更新 CHANNEL_ACCESS_TOKEN
    print("更新 CHANNEL_ACCESS_TOKEN...")
    if set_secret(owner, repo, "CHANNEL_ACCESS_TOKEN", channel_token, github_token):
        success_count += 1
    print()
    
    # 更新 USER_ID
    print("更新 USER_ID...")
    if set_secret(owner, repo, "USER_ID", user_id, github_token):
        success_count += 1
    print()
    
    # 顯示結果
    print("=" * 60)
    if success_count == total_count:
        print("✅ 所有 Secrets 更新成功！")
        print("=" * 60)
        print()
        print("建議:")
        print("1. 前往 GitHub Actions 頁面手動觸發一次工作流程")
        print("2. 確認通知是否正常發送")
    else:
        print(f"⚠️  部分更新失敗 ({success_count}/{total_count})")
        print("=" * 60)
        print()
        print("請檢查:")
        print("1. GITHUB_TOKEN 是否有效")
        print("2. Token 是否有 'repo' 權限")
        print("3. 或者使用手動方式設定")


if __name__ == "__main__":
    main()

