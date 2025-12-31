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
        # 獲取黃金價格（包含當前價格和開盤價）
        price_data = get_gold_price()
        
        if price_data is None:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 無法獲取黃金價格")
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
        
        # 如果漲跌幅超過閾值，發送 LINE 通知
        if abs_change_percent >= THRESHOLD_PERCENT:
            print(f"⚠️  價格變動超過 {THRESHOLD_PERCENT}%，發送 LINE 通知...")
            
            # 格式化通知訊息（使用新的報告格式）
            message = format_notification_message(current_price, day_high, day_low)
            
            # 發送 LINE 通知
            success = send_line_push(message)
            
            if success:
                print("✓ LINE 通知已成功發送")
            else:
                print("✗ LINE 通知發送失敗")
        else:
            print(f"價格變動在正常範圍內（< {THRESHOLD_PERCENT}%）")
        
        print("-" * 50)
        print("程式執行完成")
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
