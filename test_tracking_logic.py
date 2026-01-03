#!/usr/bin/env python3
"""
測試追蹤邏輯，確保最高/最低價正確更新
"""

import json
import os
from datetime import datetime, timezone, timedelta

def test_tracking():
    """測試追蹤邏輯"""
    print("=" * 60)
    print("測試價格追蹤邏輯")
    print("=" * 60)
    print()
    
    # 模擬多次執行
    daily_price_file = "daily_price.json"
    current_date = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
    
    # 初始化
    tracked_day_high = None
    tracked_day_low = None
    
    # 模擬價格序列（包含相同價格）
    price_sequence = [
        4359.16,  # 第1次
        4359.16,  # 第2次（相同）
        4359.20,  # 第3次（上漲）
        4359.16,  # 第4次（回到原價）
        4359.10,  # 第5次（下跌）
        4359.16,  # 第6次（回到原價）
        4359.25,  # 第7次（上漲）
    ]
    
    print("【模擬價格序列】")
    print("-" * 60)
    print("價格:", [f"${p:.2f}" for p in price_sequence])
    print()
    
    print("【追蹤過程】")
    print("-" * 60)
    
    for i, current_price in enumerate(price_sequence, 1):
        print(f"\n第 {i} 次執行:")
        print(f"  當前價格: ${current_price:.2f}")
        
        # 讀取歷史記錄（模擬）
        if i == 1:
            # 第一次執行，沒有歷史記錄
            print(f"  歷史記錄: 無（首次執行）")
        else:
            print(f"  歷史記錄: 最高 ${tracked_day_high:.2f}, 最低 ${tracked_day_low:.2f}")
        
        # 更新邏輯（與 main.py 相同）
        old_high = tracked_day_high
        old_low = tracked_day_low
        
        if tracked_day_high is None or current_price > tracked_day_high:
            tracked_day_high = current_price
            if old_high is not None:
                print(f"  ✓ 更新最高價: ${old_high:.2f} → ${tracked_day_high:.2f}")
            else:
                print(f"  ✓ 設定最高價: ${tracked_day_high:.2f}")
        
        if tracked_day_low is None or current_price < tracked_day_low:
            tracked_day_low = current_price
            if old_low is not None:
                print(f"  ✓ 更新最低價: ${old_low:.2f} → ${tracked_day_low:.2f}")
            else:
                print(f"  ✓ 設定最低價: ${tracked_day_low:.2f}")
        
        if tracked_day_high == tracked_day_low == current_price:
            if i == 1:
                print(f"  ℹ️  首次執行，最高=最低=當前價格（正常）")
            else:
                print(f"  ⚠️  最高=最低=當前價格（可能價格沒有變化）")
        elif tracked_day_high == tracked_day_low:
            print(f"  ⚠️  最高=最低（但不等於當前價格，這不應該發生）")
        else:
            print(f"  ✓ 最高和最低不同（正常）")
        
        print(f"  更新後: 最高 ${tracked_day_high:.2f}, 最低 ${tracked_day_low:.2f}")
    
    print()
    print("=" * 60)
    print("【最終結果】")
    print("=" * 60)
    print(f"最高價: ${tracked_day_high:.2f}")
    print(f"最低價: ${tracked_day_low:.2f}")
    print(f"價格範圍: ${tracked_day_high - tracked_day_low:.2f}")
    
    expected_high = max(price_sequence)
    expected_low = min(price_sequence)
    
    if tracked_day_high == expected_high and tracked_day_low == expected_low:
        print(f"\n✓ 追蹤邏輯正確！")
        print(f"  預期最高: ${expected_high:.2f}, 實際最高: ${tracked_day_high:.2f}")
        print(f"  預期最低: ${expected_low:.2f}, 實際最低: ${tracked_day_low:.2f}")
    else:
        print(f"\n✗ 追蹤邏輯有問題！")
        print(f"  預期最高: ${expected_high:.2f}, 實際最高: ${tracked_day_high:.2f}")
        print(f"  預期最低: ${expected_low:.2f}, 實際最低: ${tracked_day_low:.2f}")
    
    # 檢查是否最高=最低
    if tracked_day_high == tracked_day_low:
        print(f"\n⚠️  警告：最高價和最低價相同")
        print(f"  這表示：")
        print(f"  1. 所有價格都相同（正常情況）")
        print(f"  2. 或追蹤邏輯有問題（異常情況）")
        print(f"  3. 或日期檢查導致重置（異常情況）")

if __name__ == "__main__":
    test_tracking()

