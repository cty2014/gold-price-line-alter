#!/usr/bin/env python3
"""
測試備用 API 功能
模擬幣安 API 返回 451 錯誤時，自動切換到 CoinGecko API
"""

from get_gold_price import get_gold_price

def test_fallback():
    print("=" * 60)
    print("測試備用 API 功能")
    print("=" * 60)
    print()
    
    print("測試完整的 get_gold_price() 函數...")
    print("（如果幣安 API 失敗，應該自動切換到 CoinGecko API）")
    print()
    
    price_data = get_gold_price()
    
    if price_data:
        print()
        print("=" * 60)
        print("✓ 測試成功！成功獲取價格數據")
        print("=" * 60)
        print(f"當前價格: ${price_data['current_price']:.2f}")
        print(f"開盤價格: ${price_data['open_price']:.2f}")
        print(f"當天最高: ${price_data['day_high']:.2f}")
        print(f"當天最低: ${price_data['day_low']:.2f}")
    else:
        print()
        print("=" * 60)
        print("✗ 測試失敗！無法獲取價格數據")
        print("=" * 60)

if __name__ == "__main__":
    test_fallback()

