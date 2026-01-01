#!/usr/bin/env python3
"""
直接測試 LINE 通知功能
"""

import os
import sys
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

def test_line_notification():
    """測試 LINE 通知"""
    print("=" * 60)
    print("LINE 通知測試")
    print("=" * 60)
    
    # 獲取環境變數
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    print(f"\n1. 檢查環境變數...")
    if not channel_token or channel_token.strip() == "":
        print("✗ CHANNEL_ACCESS_TOKEN 未設定")
        print("  請在 GitHub Secrets 中設定 CHANNEL_ACCESS_TOKEN")
        return False
    else:
        print(f"✓ CHANNEL_ACCESS_TOKEN: 已設定 (長度: {len(channel_token)} 字元)")
        print(f"  前10字元: {channel_token[:10]}...")
    
    if not user_id or user_id.strip() == "":
        print("✗ USER_ID 未設定")
        print("  請在 GitHub Secrets 中設定 USER_ID")
        return False
    else:
        print(f"✓ USER_ID: 已設定")
        print(f"  值: {user_id}")
    
    # 初始化 LineBotApi
    print(f"\n2. 初始化 LINE Bot API...")
    try:
        line_bot_api = LineBotApi(channel_token)
        print("✓ LineBotApi 初始化成功")
    except Exception as e:
        print(f"✗ LineBotApi 初始化失敗: {e}")
        return False
    
    # 測試發送訊息
    print(f"\n3. 發送測試訊息...")
    test_message = "🧪 LINE Bot 測試訊息\n\n這是一則測試訊息，用於驗證 LINE Bot 設定是否正確。\n\n如果您收到此訊息，表示設定正確！"
    
    try:
        user_id_str = str(user_id).strip()
        print(f"   發送給 USER_ID: {user_id_str}")
        print(f"   訊息內容: {test_message[:50]}...")
        
        line_bot_api.push_message(user_id_str, TextSendMessage(text=test_message))
        print("✓ 訊息發送成功！請檢查您的 LINE")
        return True
        
    except LineBotApiError as e:
        error_code = e.status_code
        error_message = str(e)
        
        print(f"✗ LINE API 錯誤")
        print(f"  錯誤代碼: {error_code}")
        print(f"  錯誤訊息: {error_message}")
        
        if error_code == 401:
            print("\n   問題: CHANNEL_ACCESS_TOKEN 無效或已過期")
            print("   解決方法:")
            print("   1. 前往 LINE Developers Console")
            print("   2. 檢查 Channel Access Token 是否正確")
            print("   3. 如果過期，重新生成 Token")
            print("   4. 更新 GitHub Secrets 中的 CHANNEL_ACCESS_TOKEN")
            
        elif error_code == 400:
            if "invalid" in error_message.lower() or "'to'" in error_message.lower():
                print("\n   問題: USER_ID 無效或用戶未加入 Bot 為好友")
                print("   解決方法:")
                print("   1. 確認 USER_ID 是否正確")
                print("   2. 用戶必須先加入您的 LINE Bot 為好友")
                print("   3. 確認 Bot 的 Channel ID 是否正確")
            else:
                print("\n   問題: 請求格式錯誤")
                print(f"   詳細錯誤: {error_message}")
                
        elif error_code == 404:
            print("\n   問題: USER_ID 無效或用戶未加入 Bot 為好友")
            print("   解決方法:")
            print("   1. 確認 USER_ID 是否正確")
            print("   2. 用戶必須先加入您的 LINE Bot 為好友")
            print("   3. 確認 Bot 的 Channel ID 是否正確")
            
        elif error_code == 429:
            print("\n   問題: API 請求頻率過高")
            print("   解決方法: 請稍後再試")
            
        else:
            print(f"\n   未知錯誤: {error_code}")
            print(f"   詳細錯誤: {error_message}")
        
        return False
        
    except Exception as e:
        print(f"✗ 發生未預期的錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_line_notification()
    sys.exit(0 if success else 1)

