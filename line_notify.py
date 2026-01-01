from linebot import LineBotApi
from linebot.models import TextSendMessage
import os


# LINE Bot 設定（必須從環境變數讀取，適合雲端部署）
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")


def send_line_push(message):
    """
    發送文字訊息給指定的 LINE User ID
    
    Args:
        message (str): 要發送的訊息內容
    
    Returns:
        bool: 發送成功返回 True，失敗返回 False
    """
    try:
        # 檢查 token 和 user_id 是否設定
        if not CHANNEL_ACCESS_TOKEN or CHANNEL_ACCESS_TOKEN.strip() == "":
            print("✗ 錯誤: CHANNEL_ACCESS_TOKEN 環境變數未設定")
            print("   請在 GitHub Secrets 中設定 CHANNEL_ACCESS_TOKEN")
            return False
        
        if not USER_ID or USER_ID.strip() == "":
            print("✗ 錯誤: USER_ID 環境變數未設定")
            print("   請在 GitHub Secrets 中設定 USER_ID")
            return False
        
        # 清理和驗證 Token（移除空格、換行符等）
        token_cleaned = CHANNEL_ACCESS_TOKEN.strip()
        # 移除所有空白字符（空格、換行、製表符等）
        token_cleaned = ''.join(token_cleaned.split())
        
        # 驗證 Token 格式（LINE Token 通常是 base64 編碼的字符串）
        if not token_cleaned or len(token_cleaned) < 50:
            print(f"✗ 錯誤: CHANNEL_ACCESS_TOKEN 格式異常（長度: {len(token_cleaned)}）")
            print("   LINE Channel Access Token 通常長度應該超過 50 字元")
            print("   請檢查 GitHub Secrets 中的 CHANNEL_ACCESS_TOKEN 是否正確")
            return False
        
        # 檢查 Token 是否包含無效字符
        import re
        if not re.match(r'^[A-Za-z0-9+/=]+$', token_cleaned):
            print(f"✗ 錯誤: CHANNEL_ACCESS_TOKEN 包含無效字符")
            print("   Token 應該只包含字母、數字和 +/= 字符")
            print("   請檢查 GitHub Secrets 中的 CHANNEL_ACCESS_TOKEN 是否正確")
            return False
        
        # 初始化 LineBotApi（使用清理後的 Token）
        line_bot_api = LineBotApi(token_cleaned)
        
        # 清理和驗證 USER_ID
        user_id_str = str(USER_ID).strip()
        # 移除所有空白字符
        user_id_str = ''.join(user_id_str.split())
        
        if not user_id_str or len(user_id_str) < 10:
            print(f"✗ 錯誤: USER_ID 格式異常（長度: {len(user_id_str)}）")
            print("   LINE User ID 通常長度應該超過 10 字元")
            print("   請檢查 GitHub Secrets 中的 USER_ID 是否正確")
            return False
        
        # 發送文字訊息
        line_bot_api.push_message(user_id_str, TextSendMessage(text=message))
        
        print(f"✓ 訊息已成功發送")
        return True
    
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        
        print(f"\n{'='*60}")
        print(f"✗ LINE 通知發送失敗")
        print(f"{'='*60}")
        print(f"錯誤類型: {error_type}")
        print(f"錯誤訊息: {error_msg}")
        
        # 詳細錯誤診斷
        if "Invalid header value" in error_msg or "invalid header" in error_msg.lower():
            print(f"\n診斷: CHANNEL_ACCESS_TOKEN 格式錯誤（包含無效字符）")
            print(f"Token 長度: {len(CHANNEL_ACCESS_TOKEN) if CHANNEL_ACCESS_TOKEN else 0} 字元")
            print(f"Token 前10字元: {CHANNEL_ACCESS_TOKEN[:10] if CHANNEL_ACCESS_TOKEN else 'N/A'}...")
            print(f"解決方法:")
            print(f"  1. 前往 GitHub Secrets 頁面")
            print(f"  2. 檢查 CHANNEL_ACCESS_TOKEN 的值")
            print(f"  3. 確認 Token 沒有多餘的空格、換行符或特殊字符")
            print(f"  4. 如果 Token 有問題，前往 LINE Developers Console 重新生成")
            print(f"  5. 複製 Token 時，確保只複製 Token 本身，不要包含其他字符")
            print(f"  6. 更新 GitHub Secrets 中的 CHANNEL_ACCESS_TOKEN")
        elif "401" in error_msg or "Authentication failed" in error_msg or "invalid_token" in error_msg:
            print(f"\n診斷: CHANNEL_ACCESS_TOKEN 無效或已過期")
            print(f"解決方法:")
            print(f"  1. 前往 LINE Developers Console: https://developers.line.biz/console/")
            print(f"  2. 選擇您的 Bot")
            print(f"  3. 前往 'Messaging API' 頁面")
            print(f"  4. 檢查 'Channel access token'")
            print(f"  5. 如果過期，點擊 'Issue' 重新生成")
            print(f"  6. 更新 GitHub Secrets 中的 CHANNEL_ACCESS_TOKEN")
        elif "400" in error_msg and ("'to'" in error_msg or "invalid" in error_msg.lower()):
            print(f"\n診斷: USER_ID 無效或用戶未加入 Bot 為好友")
            print(f"當前 USER_ID: {USER_ID}")
            print(f"解決方法:")
            print(f"  1. 確認用戶已加入您的 LINE Bot 為好友")
            print(f"  2. 確認 USER_ID 正確（可在 LINE Developers Console 查看）")
            print(f"  3. 確認 Bot 的 Channel ID 正確")
            print(f"  4. 更新 GitHub Secrets 中的 USER_ID")
        elif "404" in error_msg or "Invalid user" in error_msg:
            print(f"\n診斷: USER_ID 無效或用戶未加入 Bot 為好友")
            print(f"當前 USER_ID: {USER_ID}")
            print(f"解決方法:")
            print(f"  1. 確認用戶已加入您的 LINE Bot 為好友")
            print(f"  2. 確認 USER_ID 正確")
            print(f"  3. 確認 Bot 的 Channel ID 正確")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            print(f"\n診斷: API 請求頻率過高")
            print(f"解決方法: 請稍後再試")
        else:
            print(f"\n診斷: 未知錯誤")
            print(f"請檢查完整的錯誤訊息以獲取更多資訊")
            import traceback
            print(f"\n完整錯誤堆疊:")
            traceback.print_exc()
        
        print(f"{'='*60}\n")
        return False


if __name__ == "__main__":
    # 測試函數
    test_message = "這是一則測試訊息"
    send_line_push(test_message)


