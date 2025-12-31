#!/usr/bin/env python3
"""
獲取 LINE User ID 的輔助腳本
需要先設定 CHANNEL_ACCESS_TOKEN，然後透過 Webhook 或直接查詢來獲取 USER_ID
"""

import os
import sys
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage


def get_user_id_from_followers(channel_token):
    """
    嘗試從追蹤者列表獲取 USER_ID
    注意：此方法需要 Bot 有追蹤者，且可能需要特殊權限
    """
    print("=" * 60)
    print("方法 1: 從追蹤者列表獲取 USER_ID")
    print("=" * 60)
    
    try:
        line_bot_api = LineBotApi(channel_token)
        # 注意：LINE Bot API 可能不支援直接獲取追蹤者列表
        # 這需要透過 Webhook 事件來獲取
        print("⚠️  直接獲取追蹤者列表需要 Webhook 設定")
        print("   建議使用方法 2：透過 Webhook 事件獲取")
        return None
    except Exception as e:
        print(f"✗ 獲取失敗: {e}")
        return None


def print_instructions():
    """顯示獲取 USER_ID 的說明"""
    print("\n" + "=" * 60)
    print("如何獲取 USER_ID")
    print("=" * 60)
    print("\n方法 1: 透過 Webhook 事件（推薦）")
    print("-" * 60)
    print("1. 前往 LINE Developers Console:")
    print("   https://developers.line.biz/console/")
    print("\n2. 選擇您的 Provider 和 Channel (Goldprice)")
    print("\n3. 前往 Messaging API → Webhook settings")
    print("\n4. 啟用 Webhook URL（可以設定為暫時的測試 URL）")
    print("\n5. 讓用戶發送訊息給您的 Bot")
    print("\n6. 在 Webhook 事件中，您會看到類似以下的 JSON:")
    print("""
   {
     "events": [{
       "type": "message",
       "source": {
         "type": "user",
         "userId": "U39ae43e351f819abaef6083d27d3369e"  ← 這就是 USER_ID
       },
       ...
     }]
   }
    """)
    
    print("\n方法 2: 使用 LINE Official Account Manager")
    print("-" * 60)
    print("1. 前往 LINE Official Account Manager")
    print("   https://manager.line.biz/")
    print("\n2. 選擇您的官方帳號")
    print("\n3. 前往設定 → 帳號設定")
    print("\n4. 查看用戶列表（如果有權限）")
    
    print("\n方法 3: 透過 Bot 發送訊息自動獲取")
    print("-" * 60)
    print("1. 確保用戶已加入您的 Bot 為好友")
    print("\n2. 用戶發送任意訊息給 Bot")
    print("\n3. 在 Webhook 事件中查看 userId")
    
    print("\n方法 4: 如果您已經知道 USER_ID 格式")
    print("-" * 60)
    print("USER_ID 格式通常是: U + 32 個十六進位字元")
    print("例如: U39ae43e351f819abaef6083d27d3369e")
    print("\n如果您之前有記錄過，可以直接使用")


def test_user_id(channel_token, user_id):
    """測試 USER_ID 是否有效"""
    print("\n" + "=" * 60)
    print("測試 USER_ID")
    print("=" * 60)
    
    try:
        line_bot_api = LineBotApi(channel_token)
        test_message = "🔍 USER_ID 測試訊息\n\n如果您收到這則訊息，表示 USER_ID 正確！"
        line_bot_api.push_message(user_id, TextSendMessage(text=test_message))
        print(f"✓ USER_ID 有效: {user_id}")
        print("✓ 測試訊息已發送，請檢查您的 LINE")
        return True
    except LineBotApiError as e:
        error_code = e.status_code
        error_message = e.message
        
        if error_code == 400:
            print(f"✗ USER_ID 無效 (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
        elif error_code == 404:
            print(f"✗ USER_ID 不存在或用戶未加入 Bot (HTTP {error_code})")
            print(f"  請確認用戶已加入 Bot 為好友")
        else:
            print(f"✗ 測試失敗 (HTTP {error_code})")
            print(f"  錯誤訊息: {error_message}")
        return False
    except Exception as e:
        print(f"✗ 測試過程發生錯誤: {e}")
        return False


def main():
    """主函數"""
    print("\n" + "📋 LINE User ID 獲取工具" + "\n")
    
    # 檢查 CHANNEL_ACCESS_TOKEN
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    if not channel_token or channel_token.strip() == "":
        print("✗ 錯誤: CHANNEL_ACCESS_TOKEN 環境變數未設定")
        print("\n請先設定:")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        sys.exit(1)
    
    print(f"✓ CHANNEL_ACCESS_TOKEN 已設定\n")
    
    # 顯示說明
    print_instructions()
    
    # 如果命令列有提供 USER_ID，則測試它
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        print(f"\n測試提供的 USER_ID: {user_id}")
        if test_user_id(channel_token, user_id):
            print("\n✅ USER_ID 驗證成功！")
            print(f"\n請在 GitHub Secrets 中設定:")
            print(f"  USER_ID = {user_id}")
        else:
            print("\n✗ USER_ID 驗證失敗，請檢查上述錯誤訊息")
    else:
        print("\n" + "=" * 60)
        print("使用方式")
        print("=" * 60)
        print("\n如果您已經知道 USER_ID，可以執行:")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("  python3 get_user_id.py <您的_USER_ID>")
        print("\n例如:")
        print("  python3 get_user_id.py U39ae43e351f819abaef6083d27d3369e")


if __name__ == "__main__":
    main()

