import time
from datetime import datetime
from get_gold_price import get_gold_price, load_last_price, save_price, check_price_change
from line_notify import send_line_push


def format_notification_message(current_price, change_percent, last_price):
    """
    格式化 LINE 通知訊息
    
    Args:
        current_price (float): 當前價格
        change_percent (float): 價格變化百分比
        last_price (float): 上一次價格
    
    Returns:
        str: 格式化後的訊息
    """
    # 根據漲跌選擇 Emoji
    emoji = "📈" if change_percent >= 0 else "📉"
    
    # 格式化訊息
    message = f"{emoji} 黃金價格變動通知\n\n"
    message += f"當前價格: ${current_price:.2f}\n"
    message += f"上次價格: ${last_price:.2f}\n"
    message += f"漲跌幅: {change_percent:+.2f}%\n"
    message += f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return message


def main_loop():
    """
    主迴圈：每 10 分鐘檢查一次黃金價格，如果變動超過 2% 則發送 LINE 通知
    """
    CHECK_INTERVAL = 600  # 10 分鐘 = 600 秒
    THRESHOLD_PERCENT = 2.0  # 2% 的變動閾值
    
    print("黃金價格監控系統啟動...")
    print(f"檢查間隔: {CHECK_INTERVAL // 60} 分鐘")
    print(f"變動閾值: {THRESHOLD_PERCENT}%")
    print("-" * 50)
    
    while True:
        try:
            # 獲取當前黃金價格
            current_price = get_gold_price()
            
            if current_price is None:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 無法獲取黃金價格，跳過本次檢查")
                time.sleep(CHECK_INTERVAL)
                continue
            
            # 載入上一次的價格
            last_price = load_last_price()
            
            # 如果是第一次檢查，記錄價格但不發送通知
            if last_price is None:
                save_price(current_price)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 首次檢查，已記錄當前價格: ${current_price:.2f}")
                time.sleep(CHECK_INTERVAL)
                continue
            
            # 計算價格變化百分比
            change_percent = ((current_price - last_price) / last_price) * 100
            abs_change_percent = abs(change_percent)
            
            # 顯示當前狀態
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 當前價格: ${current_price:.2f} | "
                  f"上次價格: ${last_price:.2f} | 變化: {change_percent:+.2f}%")
            
            # 如果變化超過閾值，發送 LINE 通知
            if abs_change_percent >= THRESHOLD_PERCENT:
                print(f"⚠️  價格變動超過 {THRESHOLD_PERCENT}%，發送 LINE 通知...")
                
                # 格式化通知訊息
                message = format_notification_message(current_price, change_percent, last_price)
                
                # 發送 LINE 通知
                success = send_line_push(message)
                
                if success:
                    print("✓ LINE 通知已成功發送")
                else:
                    print("✗ LINE 通知發送失敗")
                
                # 更新儲存的價格
                save_price(current_price)
            else:
                # 即使沒有觸發通知，也要更新價格記錄
                save_price(current_price)
                print(f"價格變動在正常範圍內（< {THRESHOLD_PERCENT}%）")
            
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n程式已停止")
            break
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 發生錯誤: {e}")
            print("-" * 50)
        
        # 等待 5 分鐘後再次檢查
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main_loop()

