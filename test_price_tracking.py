#!/usr/bin/env python3
"""
測試價格追蹤邏輯
"""

import json
import os
from datetime import datetime, timezone, timedelta

def get_taiwan_time():
    """獲取台灣時間"""
    taiwan_tz = timezone(timedelta(hours=8))
    return datetime.now(taiwan_tz)

def test_price_tracking():
    """測試價格追蹤邏輯"""
    print("=" * 60)
    print("價格追蹤邏輯測試")
    print("=" * 60)
    print()
    
    # 模擬多次價格更新
    daily_price_file = "daily_price.json"
    current_date = get_taiwan_time().strftime('%Y-%m-%d')
    
    # 測試價格序列
    test_prices = [4358.81, 4360.50, 4355.20, 4362.30, 4350.00, 4365.00]
    
    print("【模擬價格追蹤】")
    print("-" * 60)
    
    # 初始化
    tracked_day_high = None
    tracked_day_low = None
    
    # 如果文件存在，讀取現有數據
    if os.path.exists(daily_price_file):
        try:
            with open(daily_price_file, 'r', encoding='utf-8') as f:
                daily_data = json.load(f)
                if daily_data.get('date') == current_date:
                    tracked_day_high = daily_data.get('day_high')
                    tracked_day_low = daily_data.get('day_low')
                    print(f"✓ 讀取現有記錄: 最高 ${tracked_day_high:.2f}, 最低 ${tracked_day_low:.2f}")
        except Exception as e:
            print(f"⚠️  讀取文件時發生錯誤: {e}")
    
    print()
    print("【模擬價格更新】")
    print("-" * 60)
    
    for i, current_price in enumerate(test_prices, 1):
        print(f"\n第 {i} 次更新:")
        print(f"  當前價格: ${current_price:.2f}")
        high_str = f"${tracked_day_high:.2f}" if tracked_day_high else "N/A"
        low_str = f"${tracked_day_low:.2f}" if tracked_day_low else "N/A"
        print(f"  更新前 - 最高: {high_str}, 最低: {low_str}")
        
        # 更新邏輯（與 main.py 相同）
        if tracked_day_high is None or current_price > tracked_day_high:
            tracked_day_high = current_price
            print(f"  ✓ 更新最高價: ${tracked_day_high:.2f}")
        
        if tracked_day_low is None or current_price < tracked_day_low:
            tracked_day_low = current_price
            print(f"  ✓ 更新最低價: ${tracked_day_low:.2f}")
        
        print(f"  更新後 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
    
    print()
    print("=" * 60)
    print("【測試結果】")
    print("=" * 60)
    print(f"最終最高價: ${tracked_day_high:.2f}")
    print(f"最終最低價: ${tracked_day_low:.2f}")
    print(f"價格範圍: ${tracked_day_high - tracked_day_low:.2f}")
    
    if tracked_day_high == tracked_day_low:
        print("\n⚠️  警告: 最高價和最低價相同！")
        print("   這表示追蹤邏輯可能有問題，或者所有價格都相同")
    else:
        print("\n✓ 追蹤邏輯正常，最高價和最低價不同")

if __name__ == "__main__":
    test_price_tracking()

