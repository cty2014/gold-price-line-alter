#!/usr/bin/env python3
"""
診斷九點未收到報告的問題
"""

from datetime import datetime, timezone, timedelta

def get_taiwan_time():
    taiwan_tz = timezone(timedelta(hours=8))
    return datetime.now(taiwan_tz)

def analyze_schedule():
    """分析排程問題"""
    print("=" * 60)
    print("九點未收到報告問題診斷")
    print("=" * 60)
    print()
    
    print("【問題分析】")
    print("-" * 60)
    print("台灣時間 09:00 對應的 GitHub Actions 執行時間點：")
    print()
    
    # GitHub Actions 執行時間點（UTC）
    utc_times = []
    for hour in range(24):
        for minute in [0, 10, 20, 30, 40, 50]:
            utc_time = datetime(2026, 1, 3, hour, minute, 0, tzinfo=timezone.utc)
            taiwan_time = utc_time.astimezone(timezone(timedelta(hours=8)))
            
            if taiwan_time.hour == 9:
                utc_times.append((utc_time, taiwan_time))
                print(f"UTC {utc_time.strftime('%H:%M')} → 台灣 {taiwan_time.strftime('%H:%M')}")
    
    print()
    print("【可能的原因】")
    print("-" * 60)
    print()
    
    print("1. GitHub Actions 執行時間問題")
    print("   - GitHub Actions 在 UTC 01:00 執行時，台灣時間是 09:08")
    print("   - 如果上次發送是 08:00，距離是 68 分鐘，應該會發送")
    print("   - 但 GitHub Actions 可能延遲或失敗")
    print()
    
    print("2. 時間間隔檢查問題")
    print("   - 如果上次發送時間記錄在 08:10 或更晚")
    print("   - 距離 09:08 可能不到 55 分鐘")
    print("   - 因此不會發送")
    print()
    
    print("3. 時間範圍問題")
    print("   - 當前設定：0-10 分鐘")
    print("   - UTC 01:00 → 台灣 09:08 ✓ (在範圍內)")
    print("   - UTC 01:10 → 台灣 09:18 ✗ (不在範圍內)")
    print()
    
    print("【解決方案】")
    print("-" * 60)
    print()
    print("方案 1: 擴大時間範圍到 0-15 分鐘")
    print("   - 這樣可以涵蓋 UTC :10 對應台灣 :18 的情況")
    print()
    print("方案 2: 降低時間間隔要求到 50 分鐘")
    print("   - 這樣即使上次發送在 08:10，09:08 時也會發送")
    print()
    print("方案 3: 改為每小時固定時間發送")
    print("   - 在 UTC :08 執行（對應台灣 :00）")
    print("   - 但這會影響價格變化警報的及時性")
    print()
    
    # 模擬不同情況
    print("【模擬情況】")
    print("-" * 60)
    print()
    
    scenarios = [
        ("上次發送 08:00", datetime(2026, 1, 3, 8, 0, 0, tzinfo=timezone(timedelta(hours=8)))),
        ("上次發送 08:10", datetime(2026, 1, 3, 8, 10, 0, tzinfo=timezone(timedelta(hours=8)))),
        ("上次發送 08:20", datetime(2026, 1, 3, 8, 20, 0, tzinfo=timezone(timedelta(hours=8)))),
    ]
    
    current_time = datetime(2026, 1, 3, 9, 8, 0, tzinfo=timezone(timedelta(hours=8)))
    
    for desc, last_time in scenarios:
        time_diff = current_time - last_time
        minutes_diff = time_diff.total_seconds() / 60
        
        will_send = minutes_diff >= 55
        status = "✓ 會發送" if will_send else "✗ 不會發送"
        
        print(f"{desc}:")
        print(f"  距離: {int(minutes_diff)} 分鐘")
        print(f"  結果: {status}")
        print()

if __name__ == "__main__":
    analyze_schedule()

