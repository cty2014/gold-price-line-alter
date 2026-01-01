#!/usr/bin/env python3
"""
快速測試腳本：測試黃金價格獲取和 LINE 通知
"""

import os
import sys
from get_gold_price import get_gold_price
from line_notify import send_line_push
from datetime import datetime

def main():
    print("=" * 60)
    print("快速測試：黃金價格監控系統")
    print("=" * 60)
    
    # 檢查環境變數
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    if not channel_token or not user_id:
        print("\n⚠️  環境變數未設定")
        print("請設定以下環境變數：")
        print("  export CHANNEL_ACCESS_TOKEN='您的_TOKEN'")
        print("  export USER_ID='您的_USER_ID'")
        print("\n或者前往 GitHub Actions 頁面手動觸發 workflow 進行測試")
        return
    
    print(f"\n✓ 環境變數檢查通過")
    
    # 測試獲取黃金價格
    print("\n1. 測試獲取黃金價格...")
    price_data = get_gold_price()
    
    if price_data is None:
        print("✗ 無法獲取黃金價格")
        print("\n發送錯誤通知測試...")
        error_msg = f"⚠️ 測試：黃金價格獲取失敗\n\n"
        error_msg += f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        error_msg += f"這是一個測試訊息，用於驗證錯誤通知功能。"
        success = send_line_push(error_msg)
        if success:
            print("✓ 錯誤通知已發送")
        else:
            print("✗ 錯誤通知發送失敗")
        return
    
    print(f"✓ 價格獲取成功")
    print(f"  當前價格: ${price_data['current_price']:.2f}")
    print(f"  開盤價格: ${price_data['open_price']:.2f}")
    print(f"  當天最高: ${price_data['day_high']:.2f}")
    print(f"  當天最低: ${price_data['day_low']:.2f}")
    
    # 計算波動
    volatility = ((price_data['day_high'] - price_data['day_low']) / price_data['day_high']) * 100
    change = ((price_data['current_price'] - price_data['open_price']) / price_data['open_price']) * 100
    
    print(f"  波動幅度: {volatility:.2f}%")
    print(f"  漲跌幅: {change:+.2f}%")
    
    # 發送測試通知
    print("\n2. 發送測試通知...")
    test_message = f"🧪 測試通知\n\n"
    test_message += f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    test_message += f"當前價格: ${price_data['current_price']:.2f}\n"
    test_message += f"開盤價格: ${price_data['open_price']:.2f}\n"
    test_message += f"當天最高: ${price_data['day_high']:.2f}\n"
    test_message += f"當天最低: ${price_data['day_low']:.2f}\n"
    test_message += f"波動幅度: {volatility:.2f}%\n"
    test_message += f"漲跌幅: {change:+.2f}%\n\n"
    test_message += f"這是一則測試訊息，用於驗證系統功能。"
    
    print(f"\n訊息內容預覽:\n{test_message}\n")
    success = send_line_push(test_message)
    
    if success:
        print("✓ 測試通知已成功發送！請檢查您的 LINE")
    else:
        print("✗ 測試通知發送失敗")
        print("  請檢查:")
        print("  1. CHANNEL_ACCESS_TOKEN 是否正確")
        print("  2. USER_ID 是否正確")
        print("  3. 用戶是否已加入 Bot 為好友")

if __name__ == "__main__":
    main()

