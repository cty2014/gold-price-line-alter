from linebot import LineBotApi
from linebot.models import TextSendMessage
import os


# LINE Bot 設定（優先使用環境變數，適合雲端部署）
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN", "g+KcmhaZeUrdd+rwZnCNMTDWwJzT7Vwnkkksl0UFcDdiF3dGr41zPZy6YR7OXLqEf167GuCIgEaj0qVtmwrRa5LMSaNVwp2j4vQMKTRAW+qi2nyo+6ECsOhFwhzhzahTLrjnXCxCFVZ3qbp9qpwt3QdB04t89/1O/w1cDnyilFU=")
USER_ID = os.getenv("USER_ID", "U39ae43e351f819abaef6083d27d3369e")


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
        if CHANNEL_ACCESS_TOKEN == "YOUR_CHANNEL_ACCESS_TOKEN" or not CHANNEL_ACCESS_TOKEN:
            print("錯誤: CHANNEL_ACCESS_TOKEN 未設定或無效")
            return False
        
        if USER_ID == "YOUR_USER_ID" or not USER_ID:
            print("錯誤: USER_ID 未設定或無效")
            return False
        
        # 初始化 LineBotApi
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        
        # 發送文字訊息
        # 確保 USER_ID 是字符串格式
        user_id_str = str(USER_ID).strip()
        line_bot_api.push_message(user_id_str, TextSendMessage(text=message))
        
        print(f"✓ 訊息已成功發送")
        return True
    
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Authentication failed" in error_msg or "invalid_token" in error_msg:
            print(f"✗ LINE 認證失敗: CHANNEL_ACCESS_TOKEN 無效或已過期")
            print(f"  請檢查 LINE Developers Console 並更新 CHANNEL_ACCESS_TOKEN")
        elif "400" in error_msg and ("'to'" in error_msg or "invalid" in error_msg.lower()):
            print(f"✗ LINE 發送失敗: USER_ID 無效或用戶未加入 Bot 為好友")
            print(f"  請確認 USER_ID ({USER_ID}) 正確，且用戶已加入您的 LINE Bot")
            print(f"  提示: USER_ID 應該是字符串格式，且用戶必須先加入 Bot 為好友")
        elif "404" in error_msg or "Invalid user" in error_msg:
            print(f"✗ LINE 發送失敗: USER_ID 無效或用戶未加入 Bot 為好友")
            print(f"  請確認 USER_ID 正確，且用戶已加入您的 LINE Bot")
        else:
            print(f"✗ 發送 LINE 訊息時發生錯誤: {e}")
        return False


if __name__ == "__main__":
    # 測試函數
    test_message = "這是一則測試訊息"
    send_line_push(test_message)

