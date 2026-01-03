#!/usr/bin/env python3
"""
檢查排程問題：為什麼只在特定時間收到通知
"""

from datetime import datetime, timezone, timedelta

def get_taiwan_time_from_utc(utc_hour, utc_minute):
    """從 UTC 時間轉換為台灣時間"""
    utc_time = datetime(2024, 1, 1, utc_hour, utc_minute, tzinfo=timezone.utc)
    taiwan_tz = timezone(timedelta(hours=8))
    taiwan_time = utc_time.astimezone(taiwan_tz)
    return taiwan_time.hour, taiwan_time.minute

def check_schedule():
    """檢查排程問題"""
    print("=" * 60)
    print("排程問題診斷")
    print("=" * 60)
    print()
    
    print("【當前設定】")
    print("-" * 60)
    print("GitHub Actions Cron: */10 * * * * (每10分鐘執行一次，UTC時間)")
    print("發送條件: 台灣時間整點（分鐘數 0-5）")
    print()
    
    print("【問題分析】")
    print("-" * 60)
    print("GitHub Actions 在 UTC 時間的以下時間點執行：")
    print(":00, :10, :20, :30, :40, :50")
    print()
    print("轉換成台灣時間（UTC+8）：")
    print()
    
    # 檢查一天的執行時間點
    matches = []
    for utc_hour in range(24):
        for utc_minute in [0, 10, 20, 30, 40, 50]:
            taiwan_hour, taiwan_minute = get_taiwan_time_from_utc(utc_hour, utc_minute)
            
            # 檢查是否在整點時段（0-5分鐘）
            will_send = 0 <= taiwan_minute <= 5
            
            status = "✓ 會發送" if will_send else "✗ 不發送"
            print(f"UTC {utc_hour:02d}:{utc_minute:02d} → 台灣 {taiwan_hour:02d}:{taiwan_minute:02d} {status}")
            
            if will_send:
                matches.append((utc_hour, utc_minute, taiwan_hour, taiwan_minute))
    
    print()
    print("=" * 60)
    print("【會發送的時間點】")
    print("=" * 60)
    
    if matches:
        print(f"總共只有 {len(matches)} 個時間點會發送通知（每天）")
        print()
        for utc_h, utc_m, tw_h, tw_m in matches[:10]:  # 只顯示前10個
            print(f"UTC {utc_h:02d}:{utc_m:02d} → 台灣 {tw_h:02d}:{tw_m:02d}")
        if len(matches) > 10:
            print(f"... 還有 {len(matches) - 10} 個時間點")
    else:
        print("沒有找到會發送的時間點！")
    
    print()
    print("=" * 60)
    print("【問題原因】")
    print("=" * 60)
    print("GitHub Actions 每10分鐘執行一次（:00, :10, :20, :30, :40, :50）")
    print("但轉換成台灣時間後，這些時間點對應到：")
    print(":08, :18, :28, :38, :48, :58")
    print()
    print("只有當 UTC 時間的整點（:00）對應到台灣時間的整點時，")
    print("才會在台灣時間的 0-5 分鐘範圍內，因此才會發送。")
    print()
    print("例如：")
    print("- UTC 11:00 → 台灣 19:00 ✓ (會發送)")
    print("- UTC 12:00 → 台灣 20:00 ✓ (會發送)")
    print("- UTC 11:10 → 台灣 19:10 ✗ (不會發送)")
    print()
    
    print("=" * 60)
    print("【解決方案】")
    print("=" * 60)
    print()
    print("方案 1: 修改 cron 時間，讓它在台灣時間整點執行")
    print("  將 cron 改為: '0,10,20,30,40,50 * * * *'")
    print("  但這仍然有問題，因為 UTC 時間的整點對應台灣時間的 :08")
    print()
    print("方案 2: 修改發送邏輯，擴大時間範圍")
    print("  將發送條件改為: 台灣時間分鐘數在 0-10 或 50-59")
    print("  這樣可以涵蓋更多執行時間點")
    print()
    print("方案 3: 修改 cron 為每小時執行一次，在特定分鐘執行")
    print("  例如: '8,18,28,38,48,58 * * * *' (UTC時間)")
    print("  這樣對應台灣時間: :00, :10, :20, :30, :40, :50")
    print()
    print("方案 4: 修改發送邏輯，改為每小時發送一次（不限制整點）")
    print("  記錄上次發送時間，如果距離上次發送超過1小時就發送")

if __name__ == "__main__":
    check_schedule()

