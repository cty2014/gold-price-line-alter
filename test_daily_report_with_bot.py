#!/usr/bin/env python3
"""
測試包含台灣銀行價格的日報表功能
"""

from main import format_notification_message
from get_gold_price import get_gold_price
from get_bot_gold_price import get_bot_gold_price

def test_daily_report():
    print("=" * 60)
    print("測試包含台灣銀行價格的日報表")
    print("=" * 60)
    print()
    
    # 獲取國際價格
    print("1. 獲取國際價格（CoinGecko/幣安）...")
    price_data = get_gold_price()
    
    if not price_data:
        print("✗ 無法獲取國際價格")
        return
    
    print(f"✓ 國際價格: ${price_data['current_price']:.2f} USD/盎司")
    print()
    
    # 獲取台灣銀行價格
    print("2. 獲取台灣銀行黃金牌告匯率...")
    bot_price_data = get_bot_gold_price()
    
    if bot_price_data:
        print(f"✓ 台灣銀行價格: {bot_price_data['price']:.2f} {bot_price_data.get('unit', '台幣/公克')}")
    else:
        print("⚠️  無法獲取台灣銀行價格")
    print()
    
    # 格式化日報表
    print("3. 格式化日報表...")
    message = format_notification_message(
        price_data['current_price'],
        price_data['day_high'],
        price_data['day_low'],
        bot_price_data
    )
    
    print()
    print("=" * 60)
    print("日報表內容預覽:")
    print("=" * 60)
    print(message)
    print("=" * 60)

if __name__ == "__main__":
    test_daily_report()

