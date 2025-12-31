from datetime import datetime
from get_gold_price import get_gold_price
from line_notify import send_line_push


def format_notification_message(current_price, open_price, change_percent):
    """
    格式化 LINE 通知訊息
    
    Args:
        current_price (float): 當前價格
        open_price (float): 開盤價
        change_percent (float): 價格變化百分比
    
    Returns:
        str: 格式化後的訊息
    """
    # 根據漲跌選擇 Emoji
    emoji = "📈" if change_percent >= 0 else "📉"
    
    # 格式化訊息
    message = f"{emoji} 黃金價格變動通知\n\n"
    message += f"當前價格: ${current_price:.2f}\n"
    message += f"開盤價格: ${open_price:.2f}\n"
    message += f"漲跌幅: {change_percent:+.2f}%\n"
    message += f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
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
        
        # 計算相對於開盤價的漲跌幅
        change_percent = ((current_price - open_price) / open_price) * 100
        abs_change_percent = abs(change_percent)
        
        # 顯示當前狀態
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 當前價格: ${current_price:.2f} | "
              f"開盤價格: ${open_price:.2f} | 漲跌幅: {change_percent:+.2f}%")
        
        # 如果漲跌幅超過閾值，發送 LINE 通知
        if abs_change_percent >= THRESHOLD_PERCENT:
            print(f"⚠️  價格變動超過 {THRESHOLD_PERCENT}%，發送 LINE 通知...")
            
            # 格式化通知訊息
            message = format_notification_message(current_price, open_price, change_percent)
            
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
