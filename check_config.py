#!/usr/bin/env python3
"""
快速檢查 CHANNEL_ACCESS_TOKEN 和 USER_ID 設定
"""

import os
import sys
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

def main():
    print("=" * 60)
    print("檢查 Channel Token 和 User ID 設定")
    print("=" * 60)
    print()
    
    # 檢查環境變數
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    # 顯示設定狀態
    print("【環境變數檢查】")
    print("-" * 60)
    
    if channel_token:
        token_preview = channel_token[:15] + "..." + channel_token[-15:] if len(channel_token) > 30 else "***"
        print(f"✓ CHANNEL_ACCESS_TOKEN: 已設定")
        print(f"  預覽: {token_preview}")
        print(f"  長度: {len(channel_token)} 字元")
    else:
        print("✗ CHANNEL_ACCESS_TOKEN: 未設定")
        print("  請執行: export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
    
    print()
    
    if user_id:
        print(f"✓ USER_ID: 已設定")
        print(f"  值: {user_id}")
        print(f"  長度: {len(user_id)} 字元")
    else:
        print("✗ USER_ID: 未設定")
        print("  請執行: export USER_ID='您的_USER_ID'")
    
    print()
    print("=" * 60)
    
    # 如果兩個都有設定，進行驗證
    if channel_token and user_id:
        print("【驗證 Channel Token】")
        print("-" * 60)
        
        try:
            line_bot_api = LineBotApi(channel_token)
            profile = line_bot_api.get_bot_info()
            print(f"✓ Channel Token 有效")
            print(f"  Bot 名稱: {profile.display_name}")
            print(f"  Bot ID: {profile.user_id}")
        except LineBotApiError as e:
            print(f"✗ Channel Token 無效或已過期")
            print(f"  錯誤代碼: {e.status_code}")
            print(f"  錯誤訊息: {e.message}")
            if e.status_code == 401:
                print("  建議: 請前往 LINE Developers Console 重新獲取 Token")
        except Exception as e:
            print(f"✗ 驗證過程發生錯誤: {e}")
        
        print()
        print("【驗證 User ID】")
        print("-" * 60)
        
        try:
            line_bot_api = LineBotApi(channel_token)
            # 嘗試發送測試訊息
            from linebot.models import TextSendMessage
            test_message = "🔍 設定確認測試\n\n如果您收到這則訊息，表示 Channel Token 和 User ID 都正確設定！"
            line_bot_api.push_message(user_id, TextSendMessage(text=test_message))
            print(f"✓ User ID 有效")
            print(f"✓ 測試訊息已成功發送")
            print(f"  請檢查您的 LINE 是否收到測試訊息")
        except LineBotApiError as e:
            error_code = e.status_code
            error_message = e.message
            
            if error_code == 400:
                if "invalid" in error_message.lower() or "'to'" in error_message.lower():
                    print(f"✗ User ID 無效 (HTTP {error_code})")
                    print(f"  錯誤訊息: {error_message}")
                    print(f"  可能的原因:")
                    print(f"  1. User ID 格式錯誤")
                    print(f"  2. 用戶未加入 Bot 為好友")
                    print(f"  3. User ID 不存在")
                else:
                    print(f"✗ 發送失敗 (HTTP {error_code})")
                    print(f"  錯誤訊息: {error_message}")
            elif error_code == 404:
                print(f"✗ User ID 不存在或用戶未加入 Bot (HTTP {error_code})")
                print(f"  錯誤訊息: {error_message}")
                print(f"  請確認:")
                print(f"  1. User ID 是否正確")
                print(f"  2. 用戶是否已加入您的 LINE Bot 為好友")
            elif error_code == 401:
                print(f"✗ Channel Token 無效 (HTTP {error_code})")
                print(f"  錯誤訊息: {error_message}")
            else:
                print(f"✗ 發送失敗 (HTTP {error_code})")
                print(f"  錯誤訊息: {error_message}")
        except Exception as e:
            print(f"✗ 驗證過程發生錯誤: {e}")
        
        print()
        print("=" * 60)
        print("檢查完成")
        print("=" * 60)
    else:
        print()
        print("⚠️  無法進行完整驗證：環境變數未完全設定")
        print()
        print("設定方式:")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("  export USER_ID='您的_USER_ID'")
        print()
        print("然後重新執行此腳本進行驗證")


if __name__ == "__main__":
    main()

