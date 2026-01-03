#!/usr/bin/env python3
"""
LINE Bot 設定驗證腳本
用於檢查 CHANNEL_ACCESS_TOKEN 和 USER_ID 是否正確設定
"""

import os
import sys
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage


def verify_environment_variables():
    """檢查環境變數是否設定"""
    print("=" * 60)
    print("步驟 1: 檢查環境變數設定")
    print("=" * 60)
    
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    # 檢查 CHANNEL_ACCESS_TOKEN
    if not channel_token or channel_token.strip() == "":
        print("✗ CHANNEL_ACCESS_TOKEN: 未設定")
        print("  請設定環境變數: export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        return False, None, None
    else:
        # 只顯示前後幾個字元，保護隱私
        token_preview = channel_token[:10] + "..." + channel_token[-10:] if len(channel_token) > 20 else "***"
        print(f"✓ CHANNEL_ACCESS_TOKEN: 已設定 ({token_preview})")
    
    # 檢查 USER_ID
    if not user_id or user_id.strip() == "":
        print("✗ USER_ID: 未設定")
        print("  請設定環境變數: export USER_ID='您的_USER_ID'")
        return False, None, None
    else:
        print(f"✓ USER_ID: 已設定 ({user_id})")
    
    print("\n✓ 環境變數檢查通過\n")
    return True, channel_token, user_id


def verify_token_validity(channel_token):
    """驗證 CHANNEL_ACCESS_TOKEN 是否有效"""
    print("=" * 60)
    print("步驟 2: 驗證 CHANNEL_ACCESS_TOKEN 有效性")
    print("=" * 60)
    
    try:
        line_bot_api = LineBotApi(channel_token)
        # 嘗試獲取 Bot 資訊來驗證 token
        profile = line_bot_api.get_bot_info()
        print(f"✓ Token 有效")
        print(f"  Bot 名稱: {profile.display_name}")
        print(f"  Bot ID: {profile.user_id}")
        return True
    except LineBotApiError as e:
        error_code = e.status_code
        error_message = e.message
        
        if error_code == 401:
            print(f"✗ Token 無效或已過期 (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
            print(f"  請檢查 LINE Developers Console 並更新 CHANNEL_ACCESS_TOKEN")
        else:
            print(f"✗ Token 驗證失敗 (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
        return False
    except Exception as e:
        print(f"✗ 驗證過程發生錯誤: {e}")
        return False


def verify_user_id(channel_token, user_id):
    """驗證 USER_ID 是否有效並可接收訊息"""
    print("\n" + "=" * 60)
    print("步驟 3: 驗證 USER_ID 並測試發送訊息")
    print("=" * 60)
    
    try:
        line_bot_api = LineBotApi(channel_token)
        
        # 嘗試發送測試訊息
        test_message = "🔍 LINE Bot 設定驗證測試\n\n如果您收到這則訊息，表示設定正確！"
        line_bot_api.push_message(user_id, TextSendMessage(text=test_message))
        
        print(f"✓ USER_ID 有效")
        print(f"✓ 測試訊息已成功發送")
        print(f"  請檢查您的 LINE 是否收到測試訊息")
        return True
        
    except LineBotApiError as e:
        error_code = e.status_code
        error_message = e.message
        
        if error_code == 400:
            if "invalid" in error_message.lower() or "'to'" in error_message.lower():
                print(f"✗ USER_ID 無效 (HTTP {error_code})")
                print(f"  錯誤訊息: {error_message}")
                print(f"  可能的原因:")
                print(f"  1. USER_ID 格式錯誤")
                print(f"  2. 用戶未加入 Bot 為好友")
                print(f"  3. USER_ID 不存在")
            else:
                print(f"✗ 發送失敗 (HTTP {error_code})")
                print(f"  錯誤訊息: {error_message}")
        elif error_code == 404:
            print(f"✗ USER_ID 不存在或用戶未加入 Bot (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
            print(f"  請確認:")
            print(f"  1. USER_ID 是否正確")
            print(f"  2. 用戶是否已加入您的 LINE Bot 為好友")
        elif error_code == 401:
            print(f"✗ Token 無效 (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
        else:
            print(f"✗ 發送失敗 (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
        return False
        
    except Exception as e:
        print(f"✗ 發送過程發生錯誤: {e}")
        return False


def main():
    """主函數"""
    print("\n" + "🔍 LINE Bot 設定驗證工具" + "\n")
    
    # 步驟 1: 檢查環境變數
    success, channel_token, user_id = verify_environment_variables()
    if not success:
        print("\n✗ 驗證失敗: 環境變數未設定")
        print("\n設定方式:")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("  export USER_ID='您的_USER_ID'")
        sys.exit(1)
    
    # 步驟 2: 驗證 Token
    if not verify_token_validity(channel_token):
        print("\n✗ 驗證失敗: CHANNEL_ACCESS_TOKEN 無效")
        sys.exit(1)
    
    # 步驟 3: 驗證 USER_ID
    if not verify_user_id(channel_token, user_id):
        print("\n✗ 驗證失敗: USER_ID 無效或無法發送訊息")
        sys.exit(1)
    
    # 全部通過
    print("\n" + "=" * 60)
    print("✅ 所有驗證通過！LINE Bot 設定正確")
    print("=" * 60)
    print("\n您的設定:")
    print(f"  ✓ CHANNEL_ACCESS_TOKEN: 有效")
    print(f"  ✓ USER_ID: {user_id}")
    print(f"  ✓ 訊息發送功能: 正常")
    print("\n現在可以正常使用 LINE Bot 通知功能了！\n")


if __name__ == "__main__":
    main()





