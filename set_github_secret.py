#!/usr/bin/env python3
"""
GitHub Secrets 設定輔助腳本
使用 GitHub API 設定 Secrets（需要 GitHub Personal Access Token）
"""

import os
import sys
import base64
import json
from nacl import encoding, public
import requests


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """使用 GitHub 公鑰加密 Secret"""
    try:
        from nacl import encoding, public
    except ImportError:
        print("錯誤: 需要安裝 PyNaCl 套件")
        print("請執行: pip install PyNaCl")
        sys.exit(1)
    
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
    print("GitHub Secrets 設定工具\n")
    
    # 從環境變數獲取 GitHub Token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("錯誤: 需要設定 GITHUB_TOKEN 環境變數")
        print("\n如何獲取 GitHub Personal Access Token:")
        print("1. 前往 https://github.com/settings/tokens")
        print("2. 點擊 'Generate new token (classic)'")
        print("3. 選擇 'repo' 權限")
        print("4. 複製產生的 Token")
        print("\n然後執行:")
        print("  export GITHUB_TOKEN='您的_TOKEN'")
        print("  python3 set_github_secret.py")
        sys.exit(1)
    
    # 倉庫資訊
    owner = "cty2014"
    repo = "gold-price-line-alter"
    
    # 要設定的 Secrets
    secrets = {
        "ALPHA_VANTAGE_API_KEY": "R241TYN8MNBILQAF"
    }
    
    print(f"倉庫: {owner}/{repo}\n")
    print("準備設定以下 Secrets:")
    for name, value in secrets.items():
        print(f"  - {name}: {value[:10]}...")
    
    print("\n開始設定...\n")
    
    success_count = 0
    for secret_name, secret_value in secrets.items():
        if set_secret(owner, repo, secret_name, secret_value, github_token):
            success_count += 1
        print()
    
    print(f"完成！成功設定 {success_count}/{len(secrets)} 個 Secrets")


if __name__ == "__main__":
    main()




