#!/usr/bin/env python3
"""
顯示並確認 Channel Token 和 User ID 設定
"""

import os
import re

def main():
    print("=" * 60)
    print("Channel Token 和 User ID 設定狀態")
    print("=" * 60)
    print()
    
    # 檢查環境變數
    env_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    env_user_id = os.getenv("USER_ID")
    
    print("【環境變數】")
    print("-" * 60)
    
    if env_token:
        token_preview = env_token[:15] + "..." + env_token[-15:] if len(env_token) > 30 else "***"
        print(f"✓ CHANNEL_ACCESS_TOKEN: 已設定")
        print(f"  預覽: {token_preview}")
        print(f"  長度: {len(env_token)} 字元")
    else:
        print("✗ CHANNEL_ACCESS_TOKEN: 未設定")
    
    print()
    
    if env_user_id:
        print(f"✓ USER_ID: 已設定")
        print(f"  值: {env_user_id}")
        print(f"  長度: {len(env_user_id)} 字元")
    else:
        print("✗ USER_ID: 未設定")
    
    print()
    print("=" * 60)
    print("【檔案中的 Token】")
    print("-" * 60)
    
    # 檢查 update_channel_token.py 中的 token
    found_token = None
    try:
        with open("update_channel_token.py", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'channel_token\s*=\s*"([^"]+)"', content)
            if match:
                found_token = match.group(1)
                token_preview = found_token[:15] + "..." + found_token[-15:] if len(found_token) > 30 else "***"
                print(f"✓ 在 update_channel_token.py 中找到 Token")
                print(f"  預覽: {token_preview}")
                print(f"  長度: {len(found_token)} 字元")
            else:
                print("✗ 在 update_channel_token.py 中未找到 Token")
    except Exception as e:
        print(f"✗ 無法讀取 update_channel_token.py: {e}")
    
    print()
    print("=" * 60)
    print("【驗證建議】")
    print("-" * 60)
    print()
    
    if env_token and env_user_id:
        print("✓ 環境變數已設定，可以使用以下命令驗證:")
        print()
        print("  python3 verify_line_config.py")
        print()
        print("或使用:")
        print()
        print("  python3 check_config.py")
    elif found_token:
        print("發現 Token，但環境變數未設定。")
        print()
        print("方法 1: 設定環境變數後驗證")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("  export USER_ID='您的_USER_ID'")
        print("  python3 verify_line_config.py")
        print()
        print("方法 2: 使用找到的 Token 驗證（需要提供 User ID）")
        print("  export CHANNEL_ACCESS_TOKEN='找到的_TOKEN'")
        print("  export USER_ID='您的_USER_ID'")
        print("  python3 verify_line_config.py")
    else:
        print("未找到任何 Token 設定。")
        print()
        print("請執行以下步驟:")
        print("1. 獲取 Channel Access Token:")
        print("   - 前往 https://developers.line.biz/console/")
        print("   - 選擇您的 Channel")
        print("   - 在 Messaging API 頁面獲取 Channel Access Token")
        print()
        print("2. 獲取 User ID:")
        print("   - 使用 get_user_id.py 腳本")
        print("   - 或透過 Webhook 事件獲取")
        print()
        print("3. 設定環境變數:")
        print("   export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("   export USER_ID='您的_USER_ID'")
        print()
        print("4. 驗證設定:")
        print("   python3 verify_line_config.py")
    
    print()
    print("=" * 60)
    print("【快速驗證命令】")
    print("=" * 60)
    print()
    
    if found_token:
        print("如果要在 GitHub Secrets 中設定，可以使用:")
        print()
        print("  CHANNEL_ACCESS_TOKEN = (從 update_channel_token.py 中的值)")
        print("  USER_ID = (您的 User ID)")
        print()
        print("或使用 update_channel_token.py 腳本更新 GitHub Secrets")
    
    print("驗證腳本:")
    print("  - verify_line_config.py: 完整驗證（需要環境變數）")
    print("  - check_config.py: 快速檢查（需要環境變數）")
    print("  - get_user_id.py: 獲取 User ID 的說明")


if __name__ == "__main__":
    main()

