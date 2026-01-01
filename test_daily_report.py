#!/usr/bin/env python3
"""
測試每日報告邏輯
強制發送一次報告來測試功能
"""

import os
import sys
from datetime import datetime
from get_gold_price import get_gold_price
from line_notify import send_line_push

def format_notification_message(current_price, day_high, day_low):
    """格式化通知訊息"""
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    if day_high > 0:
        volatility = ((day_high - day_low) / day_high) * 100
    else:
        volatility = 0.0
    
    message = "📊 每日黃金價格報告（測試）\n"
    message += f"報告時間: {current_time}\n"
    message += f"日期: {current_date}\n"
    message += f"當前價格: ${current_price:.2f}\n"
    message += "-------------------\n"
    message += f"當天最高: ${day_high:.2f}\n"
    message += f"當天最低: ${day_low:.2f}\n"
    message += f"波動幅度: {volatility:.2f}%"
    
    return message

def main():
    print("測試每日報告功能...")
    print("-" * 50)
    
    # 檢查環境變數
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    if not channel_token or not user_id:
        print("錯誤: 請設定環境變數")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("  export USER_ID='您的_USER_ID'")
        sys.exit(1)
    
    # 獲取價格
    print("獲取黃金價格...")
    price_data = get_gold_price()
    
    if price_data is None:
        print("✗ 無法獲取黃金價格")
        sys.exit(1)
    
    current_price = price_data['current_price']
    day_high = price_data['day_high']
    day_low = price_data['day_low']
    
    print(f"✓ 價格獲取成功")
    print(f"  當前價格: ${current_price:.2f}")
    print(f"  當天最高: ${day_high:.2f}")
    print(f"  當天最低: ${day_low:.2f}")
    
    # 發送測試報告
    print("\n準備發送測試報告...")
    message = format_notification_message(current_price, day_high, day_low)
    
    success = send_line_push(message)
    
    if success:
        print("✓ 測試報告已成功發送")
    else:
        print("✗ 測試報告發送失敗")
        sys.exit(1)

if __name__ == "__main__":
    main()



