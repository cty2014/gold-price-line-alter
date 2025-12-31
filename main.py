from datetime import datetime
from get_gold_price import get_gold_price
from line_notify import send_line_push


def format_notification_message(current_price, day_high, day_low):
    """
    格式化 LINE 通知訊息（每日黃金價格報告格式）
    
    Args:
        current_price (float): 當前價格
        day_high (float): 當天最高價
        day_low (float): 當天最低價
    
    Returns:
        str: 格式化後的訊息
    """
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # 計算波動幅度
    if day_high > 0:
        volatility = ((day_high - day_low) / day_high) * 100
    else:
        volatility = 0.0
    
    # 格式化訊息（按照用戶要求的格式）
    message = "📊 每日黃金價格報告\n"
    message += f"報告時間: {current_time}\n"
    message += f"日期: {current_date}\n"
    message += f"當前價格: ${current_price:.2f}\n"
    message += "-------------------\n"
    message += f"當天最高: ${day_high:.2f}\n"
    message += f"當天最低: ${day_low:.2f}\n"
    message += f"波動幅度: {volatility:.2f}%"
    
    return message


def main():
    """
    主程式：執行一次價格檢查，如果漲跌幅超過 1% 則發送 LINE 通知
    """
    THRESHOLD_PERCENT = 1.0  # 1% 的變動閾值
    
    print("黃金價格監控系統啟動...")
    print(f"變動閾值: {THRESHOLD_PERCENT}%")
    print("-" * 50)
    
    try:
        # 檢查環境變數是否設定（GitHub Actions）
        import os
        channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
        user_id = os.getenv("USER_ID")
        
        if not channel_token or channel_token.strip() == "":
            print("✗ 錯誤: CHANNEL_ACCESS_TOKEN 環境變數未設定")
            print("   請在 GitHub Secrets 中設定 CHANNEL_ACCESS_TOKEN")
            print("   程式無法繼續執行，請檢查 GitHub Actions Secrets 設定")
            return
        
        if not user_id or user_id.strip() == "":
            print("✗ 錯誤: USER_ID 環境變數未設定")
            print("   請在 GitHub Secrets 中設定 USER_ID")
            print("   程式無法繼續執行，請檢查 GitHub Actions Secrets 設定")
            return
        
        print(f"✓ 環境變數檢查通過")
        print(f"  CHANNEL_ACCESS_TOKEN: {'已設定' if channel_token else '未設定'}")
        print(f"  USER_ID: {'已設定' if user_id else '未設定'}")
        
        # 獲取黃金價格（包含當前價格和開盤價）
        price_data = get_gold_price()
        
        if price_data is None:
            error_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{error_time}] 無法獲取黃金價格")
            print("   這可能是 API 連接問題，請檢查網路連線")
            
            # 即使無法獲取價格，也發送錯誤通知
            error_message = f"⚠️ 黃金價格獲取失敗\n\n"
            error_message += f"報告時間: {error_time}\n"
            error_message += f"錯誤原因: 無法連接到黃金價格 API\n"
            error_message += f"請檢查:\n"
            error_message += f"1. 網路連線是否正常\n"
            error_message += f"2. API 服務是否可用\n"
            error_message += f"3. GitHub Actions 執行環境是否正常"
            
            print(f"\n準備發送錯誤通知到 LINE...")
            success = send_line_push(error_message)
            
            if success:
                print("✓ 錯誤通知已成功發送")
            else:
                print("✗ 錯誤通知發送失敗")
            
            return
        
        current_price = price_data['current_price']
        open_price = price_data['open_price']
        day_high = price_data['day_high']
        day_low = price_data['day_low']
        
        # 計算相對於開盤價的漲跌幅
        change_percent = ((current_price - open_price) / open_price) * 100
        abs_change_percent = abs(change_percent)
        
        # 顯示當前狀態
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 當前價格: ${current_price:.2f} | "
              f"開盤價格: ${open_price:.2f} | 漲跌幅: {change_percent:+.2f}%")
        print(f"當天最高: ${day_high:.2f} | 當天最低: ${day_low:.2f}")
        
        # 發送每日黃金價格報告（每次執行都發送）
        print(f"📊 準備發送每日黃金價格報告...")
        
        # 格式化通知訊息（使用新的報告格式）
        message = format_notification_message(current_price, day_high, day_low)
        
        # 發送 LINE 通知
        print(f"\n準備發送訊息到 LINE...")
        print(f"訊息內容預覽:\n{message}\n")
        success = send_line_push(message)
        
        if success:
            print("✓ LINE 通知已成功發送")
        else:
            print("✗ LINE 通知發送失敗")
            print("   可能的原因:")
            print("   1. CHANNEL_ACCESS_TOKEN 未設定或無效")
            print("   2. USER_ID 未設定或無效")
            print("   3. 用戶未加入 Bot 為好友")
            print("   4. LINE Bot API 連線問題")
            print("   5. Token 已過期或被撤銷")
            raise Exception("LINE 通知發送失敗，請檢查設定")
        
        # 如果漲跌幅超過閾值，額外記錄
        if abs_change_percent >= THRESHOLD_PERCENT:
            print(f"⚠️  價格變動超過 {THRESHOLD_PERCENT}%")
        else:
            print(f"價格變動在正常範圍內（< {THRESHOLD_PERCENT}%）")
        
        print("-" * 50)
        print("程式執行完成")
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
