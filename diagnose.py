#!/usr/bin/env python3
"""
診斷腳本：檢查黃金價格監控系統的設定和狀態
"""

import os
import json
from datetime import datetime
from get_gold_price import get_gold_price
from line_notify import send_line_push

def check_environment():
    """檢查環境變數設定"""
    print("=" * 60)
    print("1. 檢查環境變數設定")
    print("=" * 60)
    
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    print(f"CHANNEL_ACCESS_TOKEN: {'✓ 已設定' if channel_token and channel_token.strip() else '✗ 未設定'}")
    if channel_token:
        print(f"  長度: {len(channel_token)} 字元")
        print(f"  前10字元: {channel_token[:10]}...")
    
    print(f"USER_ID: {'✓ 已設定' if user_id and user_id.strip() else '✗ 未設定'}")
    if user_id:
        print(f"  值: {user_id}")
    
    return channel_token and user_id

def check_time_logic():
    """檢查時間判斷邏輯"""
    print("\n" + "=" * 60)
    print("2. 檢查時間判斷邏輯")
    print("=" * 60)
    
    utc_now = datetime.utcnow()
    taiwan_time = datetime.now()
    current_hour = utc_now.hour
    current_minute = utc_now.minute
    
    print(f"UTC 時間: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"台灣時間: {taiwan_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC 小時: {current_hour}, 分鐘: {current_minute}")
    
    # 檢查是否在每日報告時間窗口
    is_daily_report_time = (current_hour == 9 and current_minute >= 30) or (current_hour == 10 and current_minute < 30)
    
    print(f"\n每日報告時間窗口: UTC 09:30-10:30（台灣時間 17:30-18:30）")
    print(f"是否在時間窗口內: {'✓ 是' if is_daily_report_time else '✗ 否'}")
    
    # 檢查 GitHub Actions 環境
    github_event = os.getenv("GITHUB_EVENT_NAME", "")
    is_manual_trigger = github_event == "workflow_dispatch"
    print(f"GitHub Event: {github_event if github_event else '未設定（本地執行）'}")
    print(f"是否手動觸發: {'✓ 是' if is_manual_trigger else '✗ 否'}")
    
    return is_daily_report_time or is_manual_trigger

def check_last_report():
    """檢查上次報告時間"""
    print("\n" + "=" * 60)
    print("3. 檢查上次報告時間")
    print("=" * 60)
    
    last_report_file = "last_report_time.json"
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    if os.path.exists(last_report_file):
        try:
            with open(last_report_file, 'r', encoding='utf-8') as f:
                last_report_data = json.load(f)
                last_report_date = last_report_data.get('date', '')
                last_report_time = last_report_data.get('time', '')
                print(f"上次報告日期: {last_report_date}")
                print(f"上次報告時間: {last_report_time}")
                print(f"今天日期: {today_date}")
                print(f"今天已發送: {'✓ 是' if last_report_date == today_date else '✗ 否'}")
                return last_report_date == today_date
        except Exception as e:
            print(f"✗ 讀取失敗: {e}")
            return False
    else:
        print("ℹ️  尚未有報告記錄")
        return False

def test_gold_price_api():
    """測試黃金價格 API"""
    print("\n" + "=" * 60)
    print("4. 測試黃金價格 API")
    print("=" * 60)
    
    try:
        price_data = get_gold_price()
        if price_data:
            print("✓ API 連接成功")
            print(f"  當前價格: ${price_data.get('current_price', 0):.2f}")
            print(f"  開盤價格: ${price_data.get('open_price', 0):.2f}")
            print(f"  當天最高: ${price_data.get('day_high', 0):.2f}")
            print(f"  當天最低: ${price_data.get('day_low', 0):.2f}")
            return True
        else:
            print("✗ API 連接失敗")
            return False
    except Exception as e:
        print(f"✗ API 測試失敗: {e}")
        return False

def test_line_notification():
    """測試 LINE 通知"""
    print("\n" + "=" * 60)
    print("5. 測試 LINE 通知")
    print("=" * 60)
    
    test_message = f"🧪 測試訊息\n\n測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n這是一則測試訊息，用於驗證 LINE Bot 設定是否正確。"
    
    print("準備發送測試訊息...")
    print(f"訊息內容:\n{test_message}\n")
    
    try:
        success = send_line_push(test_message)
        if success:
            print("✓ LINE 通知測試成功！請檢查您的 LINE 是否收到訊息。")
            return True
        else:
            print("✗ LINE 通知測試失敗")
            return False
    except Exception as e:
        print(f"✗ LINE 通知測試發生錯誤: {e}")
        return False

def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("黃金價格監控系統診斷工具")
    print("=" * 60 + "\n")
    
    results = {
        '環境變數': check_environment(),
        '時間邏輯': check_time_logic(),
        '上次報告': check_last_report(),
        'API 連接': test_gold_price_api(),
        'LINE 通知': False  # 需要用戶確認
    }
    
    print("\n" + "=" * 60)
    print("診斷結果摘要")
    print("=" * 60)
    
    for key, value in results.items():
        status = "✓ 通過" if value else "✗ 失敗"
        print(f"{key}: {status}")
    
    print("\n" + "=" * 60)
    print("建議操作")
    print("=" * 60)
    
    if not results['環境變數']:
        print("1. ✗ 請檢查環境變數設定（CHANNEL_ACCESS_TOKEN 和 USER_ID）")
        print("   在 GitHub Actions 中，請確認 Secrets 已正確設定")
    
    if not results['時間邏輯']:
        print("2. ℹ️  當前不在每日報告時間窗口內")
        print("   每日報告時間: UTC 09:30-10:30（台灣時間 17:30-18:30）")
        print("   或使用手動觸發（workflow_dispatch）")
    
    if results['上次報告']:
        print("3. ℹ️  今天已經發送過報告，系統會跳過重複發送")
    
    if not results['API 連接']:
        print("4. ✗ 請檢查網路連線和 API 服務狀態")
    
    print("\n5. 是否要測試 LINE 通知？(y/n): ", end="")
    try:
        response = input().strip().lower()
        if response == 'y':
            results['LINE 通知'] = test_line_notification()
    except:
        print("跳過 LINE 通知測試")
    
    print("\n" + "=" * 60)
    print("診斷完成")
    print("=" * 60)

if __name__ == "__main__":
    main()


