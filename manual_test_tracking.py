#!/usr/bin/env python3
"""
手動測試價格追蹤邏輯
模擬不同的價格變化情況，驗證追蹤是否正確
"""

import json
import os
import shutil
from datetime import datetime, timezone, timedelta

def get_taiwan_time():
    """獲取台灣時間"""
    taiwan_tz = timezone(timedelta(hours=8))
    return datetime.now(taiwan_tz)

def backup_file(filename):
    """備份文件"""
    if os.path.exists(filename):
        backup_name = f"{filename}.backup"
        shutil.copy2(filename, backup_name)
        print(f"✓ 已備份 {filename} -> {backup_name}")
        return backup_name
    return None

def restore_file(filename, backup_name):
    """還原文件"""
    if backup_name and os.path.exists(backup_name):
        shutil.copy2(backup_name, filename)
        print(f"✓ 已還原 {filename} <- {backup_name}")

def test_price_tracking():
    """測試價格追蹤邏輯"""
    print("=" * 60)
    print("手動測試價格追蹤邏輯")
    print("=" * 60)
    print()
    
    # 備份原始文件
    daily_price_file = "daily_price.json"
    last_price_file = "last_price.json"
    
    daily_backup = backup_file(daily_price_file)
    last_backup = backup_file(last_price_file)
    
    try:
        # 測試場景 1: 首次執行（沒有歷史記錄）
        print("\n" + "=" * 60)
        print("測試場景 1: 首次執行（沒有歷史記錄）")
        print("=" * 60)
        
        # 刪除現有文件
        if os.path.exists(daily_price_file):
            os.remove(daily_price_file)
        if os.path.exists(last_price_file):
            os.remove(last_price_file)
        
        # 模擬首次執行
        current_price = 4358.81
        current_date = get_taiwan_time().strftime('%Y-%m-%d')
        
        tracked_day_high = None
        tracked_day_low = None
        
        # 讀取歷史記錄（應該不存在）
        if os.path.exists(daily_price_file):
            with open(daily_price_file, 'r', encoding='utf-8') as f:
                daily_data = json.load(f)
                if daily_data.get('date') == current_date:
                    tracked_day_high = daily_data.get('day_high')
                    tracked_day_low = daily_data.get('day_low')
        
        # 更新邏輯
        if tracked_day_high is None or current_price > tracked_day_high:
            tracked_day_high = current_price
        if tracked_day_low is None or current_price < tracked_day_low:
            tracked_day_low = current_price
        
        # 保存記錄
        daily_data_to_save = {
            'date': current_date,
            'day_high': tracked_day_high,
            'day_low': tracked_day_low,
            'last_update': get_taiwan_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(daily_price_file, 'w', encoding='utf-8') as f:
            json.dump(daily_data_to_save, f, ensure_ascii=False, indent=2)
        
        print(f"當前價格: ${current_price:.2f}")
        print(f"最高價: ${tracked_day_high:.2f}")
        print(f"最低價: ${tracked_day_low:.2f}")
        print(f"結果: {'✓ 正確（首次執行，最高=最低=當前價格）' if tracked_day_high == tracked_day_low == current_price else '✗ 錯誤'}")
        
        # 測試場景 2: 價格上漲
        print("\n" + "=" * 60)
        print("測試場景 2: 價格上漲")
        print("=" * 60)
        
        # 讀取現有記錄
        with open(daily_price_file, 'r', encoding='utf-8') as f:
            daily_data = json.load(f)
            tracked_day_high = daily_data.get('day_high')
            tracked_day_low = daily_data.get('day_low')
        
        print(f"更新前 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
        
        # 模擬價格上漲
        current_price = 4365.50
        
        # 更新邏輯
        if tracked_day_high is None or current_price > tracked_day_high:
            tracked_day_high = current_price
            print(f"✓ 更新最高價: ${tracked_day_high:.2f}")
        if tracked_day_low is None or current_price < tracked_day_low:
            tracked_day_low = current_price
            print(f"✓ 更新最低價: ${tracked_day_low:.2f}")
        
        # 保存記錄
        daily_data_to_save = {
            'date': current_date,
            'day_high': tracked_day_high,
            'day_low': tracked_day_low,
            'last_update': get_taiwan_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(daily_price_file, 'w', encoding='utf-8') as f:
            json.dump(daily_data_to_save, f, ensure_ascii=False, indent=2)
        
        print(f"當前價格: ${current_price:.2f}")
        print(f"更新後 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
        print(f"結果: {'✓ 正確（最高價已更新）' if tracked_day_high == current_price else '✗ 錯誤'}")
        
        # 測試場景 3: 價格下跌
        print("\n" + "=" * 60)
        print("測試場景 3: 價格下跌")
        print("=" * 60)
        
        # 讀取現有記錄
        with open(daily_price_file, 'r', encoding='utf-8') as f:
            daily_data = json.load(f)
            tracked_day_high = daily_data.get('day_high')
            tracked_day_low = daily_data.get('day_low')
        
        print(f"更新前 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
        
        # 模擬價格下跌
        current_price = 4350.20
        
        # 更新邏輯
        if tracked_day_high is None or current_price > tracked_day_high:
            tracked_day_high = current_price
            print(f"✓ 更新最高價: ${tracked_day_high:.2f}")
        if tracked_day_low is None or current_price < tracked_day_low:
            tracked_day_low = current_price
            print(f"✓ 更新最低價: ${tracked_day_low:.2f}")
        
        # 保存記錄
        daily_data_to_save = {
            'date': current_date,
            'day_high': tracked_day_high,
            'day_low': tracked_day_low,
            'last_update': get_taiwan_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(daily_price_file, 'w', encoding='utf-8') as f:
            json.dump(daily_data_to_save, f, ensure_ascii=False, indent=2)
        
        print(f"當前價格: ${current_price:.2f}")
        print(f"更新後 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
        print(f"結果: {'✓ 正確（最低價已更新）' if tracked_day_low == current_price else '✗ 錯誤'}")
        
        # 測試場景 4: 價格在中間範圍
        print("\n" + "=" * 60)
        print("測試場景 4: 價格在中間範圍（不更新最高/最低）")
        print("=" * 60)
        
        # 讀取現有記錄
        with open(daily_price_file, 'r', encoding='utf-8') as f:
            daily_data = json.load(f)
            tracked_day_high = daily_data.get('day_high')
            tracked_day_low = daily_data.get('day_low')
        
        print(f"更新前 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
        
        # 模擬價格在中間範圍
        current_price = 4358.00
        old_high = tracked_day_high
        old_low = tracked_day_low
        
        # 更新邏輯
        if tracked_day_high is None or current_price > tracked_day_high:
            tracked_day_high = current_price
        if tracked_day_low is None or current_price < tracked_day_low:
            tracked_day_low = current_price
        
        print(f"當前價格: ${current_price:.2f}")
        print(f"更新後 - 最高: ${tracked_day_high:.2f}, 最低: ${tracked_day_low:.2f}")
        print(f"結果: {'✓ 正確（最高/最低價未改變）' if tracked_day_high == old_high and tracked_day_low == old_low else '✗ 錯誤'}")
        
        # 測試場景 5: 多次價格變化
        print("\n" + "=" * 60)
        print("測試場景 5: 多次價格變化（完整追蹤）")
        print("=" * 60)
        
        # 重置為初始狀態
        tracked_day_high = None
        tracked_day_low = None
        
        # 模擬多次價格變化
        price_sequence = [4358.81, 4360.50, 4355.20, 4362.30, 4350.00, 4365.00, 4352.50]
        
        print("價格序列:", [f"${p:.2f}" for p in price_sequence])
        print()
        
        for i, price in enumerate(price_sequence, 1):
            # 更新邏輯
            if tracked_day_high is None or price > tracked_day_high:
                tracked_day_high = price
                print(f"第 {i} 次: ${price:.2f} → ✓ 更新最高價: ${tracked_day_high:.2f}")
            elif tracked_day_low is None or price < tracked_day_low:
                tracked_day_low = price
                print(f"第 {i} 次: ${price:.2f} → ✓ 更新最低價: ${tracked_day_low:.2f}")
            else:
                print(f"第 {i} 次: ${price:.2f} → ⏸ 無變化")
        
        print()
        print(f"最終最高價: ${tracked_day_high:.2f}")
        print(f"最終最低價: ${tracked_day_low:.2f}")
        print(f"價格範圍: ${tracked_day_high - tracked_day_low:.2f}")
        print(f"波動幅度: {((tracked_day_high - tracked_day_low) / tracked_day_high * 100):.2f}%")
        
        expected_high = max(price_sequence)
        expected_low = min(price_sequence)
        
        if tracked_day_high == expected_high and tracked_day_low == expected_low:
            print(f"結果: ✓ 正確（最高價和最低價都正確追蹤）")
        else:
            print(f"結果: ✗ 錯誤")
            print(f"  預期最高: ${expected_high:.2f}, 實際最高: ${tracked_day_high:.2f}")
            print(f"  預期最低: ${expected_low:.2f}, 實際最低: ${tracked_day_low:.2f}")
        
        # 顯示最終記錄
        print("\n" + "=" * 60)
        print("最終記錄內容")
        print("=" * 60)
        with open(daily_price_file, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
            print(json.dumps(final_data, indent=2, ensure_ascii=False))
        
    finally:
        # 還原原始文件
        print("\n" + "=" * 60)
        print("還原原始文件")
        print("=" * 60)
        restore_file(daily_price_file, daily_backup)
        restore_file(last_price_file, last_backup)
        
        # 清理備份文件
        if daily_backup and os.path.exists(daily_backup):
            os.remove(daily_backup)
        if last_backup and os.path.exists(last_backup):
            os.remove(last_backup)
        
        print("\n✓ 測試完成，原始文件已還原")

if __name__ == "__main__":
    test_price_tracking()

