#!/usr/bin/env python3
"""
觸發 GitHub Actions workflow
需要設定 GITHUB_TOKEN 環境變數
"""
import os
import requests
import sys

def trigger_workflow():
    # GitHub 設定
    repo = "cty2014/gold-price-line-alter"
    workflow_file = "黃金價格監控.yml"
    
    # 從環境變數獲取 token
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("錯誤: 請設定 GITHUB_TOKEN 環境變數")
        print("使用方式: export GITHUB_TOKEN='您的_GitHub_Token'")
        print("\n或直接在 GitHub 網頁上手動觸發:")
        print(f"1. 前往: https://github.com/{repo}/actions")
        print("2. 選擇 '黃金價格監控' workflow")
        print("3. 點擊 'Run workflow' 按鈕")
        return False
    
    # GitHub API URL
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_file}/dispatches"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    data = {
        "ref": "main"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 204:
            print("✓ 成功觸發 GitHub Actions workflow")
            print(f"查看執行狀態: https://github.com/{repo}/actions")
            return True
        else:
            print(f"✗ 觸發失敗，狀態碼: {response.status_code}")
            print(f"回應: {response.text}")
            return False
    
    except Exception as e:
        print(f"✗ 發生錯誤: {e}")
        return False

if __name__ == "__main__":
    trigger_workflow()

