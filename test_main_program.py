#!/usr/bin/env python3
"""
測試主程序的所有功能
"""

import os
import sys

def test_environment_variables():
    """測試環境變數設定"""
    print("=" * 60)
    print("測試 1: 環境變數設定")
    print("=" * 60)
    
    channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("USER_ID")
    
    if not channel_token:
        print("✗ CHANNEL_ACCESS_TOKEN 未設定")
        return False
    else:
        print(f"✓ CHANNEL_ACCESS_TOKEN: 已設定 (長度: {len(channel_token)})")
    
    if not user_id:
        print("✗ USER_ID 未設定")
        return False
    else:
        print(f"✓ USER_ID: 已設定 ({user_id})")
    
    print()
    return True


def test_gold_price():
    """測試獲取黃金價格"""
    print("=" * 60)
    print("測試 2: 獲取黃金價格")
    print("=" * 60)
    
    try:
        from get_gold_price import get_gold_price
        
        price_data = get_gold_price()
        
        if price_data is None:
            print("✗ 無法獲取黃金價格")
            return False
        
        print(f"✓ 成功獲取黃金價格")
        print(f"  當前價格: ${price_data['current_price']:.2f}")
        print(f"  開盤價格: ${price_data['open_price']:.2f}")
        print(f"  當日最高: ${price_data['day_high']:.2f}")
        print(f"  當日最低: ${price_data['day_low']:.2f}")
        
        change = ((price_data['current_price'] - price_data['open_price']) / price_data['open_price']) * 100
        print(f"  漲跌幅: {change:+.2f}%")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ 獲取黃金價格時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


def test_line_notification():
    """測試 LINE 通知功能"""
    print("=" * 60)
    print("測試 3: LINE 通知功能")
    print("=" * 60)
    
    try:
        from line_notify import send_line_push
        
        test_message = "🧪 主程序測試\n\n這是一則測試訊息，用於驗證 LINE Bot 通知功能是否正常運作。\n\n如果您收到這則訊息，表示所有設定都正確！"
        
        print("發送測試訊息...")
        success = send_line_push(test_message)
        
        if success:
            print("✓ LINE 通知發送成功")
            print("  請檢查您的 LINE 是否收到測試訊息")
        else:
            print("✗ LINE 通知發送失敗")
        
        print()
        return success
        
    except Exception as e:
        print(f"✗ LINE 通知測試時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


def test_main_program_logic():
    """測試主程序邏輯（不發送實際通知）"""
    print("=" * 60)
    print("測試 4: 主程序邏輯")
    print("=" * 60)
    
    try:
        from main import format_notification_message, get_taiwan_time
        
        # 測試時間函數
        taiwan_time = get_taiwan_time()
        print(f"✓ 台灣時間獲取成功: {taiwan_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 測試訊息格式化
        test_price = 2345.67
        test_high = 2350.00
        test_low = 2340.00
        
        message = format_notification_message(test_price, test_high, test_low)
        print(f"✓ 訊息格式化成功")
        print(f"  訊息長度: {len(message)} 字元")
        print(f"  訊息預覽:")
        print("  " + "\n  ".join(message.split("\n")[:5]))
        print("  ...")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ 主程序邏輯測試時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


def main():
    """主測試函數"""
    print("\n" + "🧪 主程序完整測試" + "\n")
    
    results = []
    
    # 測試 1: 環境變數
    results.append(("環境變數設定", test_environment_variables()))
    
    # 測試 2: 獲取黃金價格
    results.append(("獲取黃金價格", test_gold_price()))
    
    # 測試 3: LINE 通知
    results.append(("LINE 通知功能", test_line_notification()))
    
    # 測試 4: 主程序邏輯
    results.append(("主程序邏輯", test_main_program_logic()))
    
    # 顯示測試結果摘要
    print("=" * 60)
    print("測試結果摘要")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print()
    print(f"總計: {passed}/{len(results)} 項測試通過")
    
    if failed > 0:
        print(f"⚠️  有 {failed} 項測試失敗，請檢查上述錯誤訊息")
        sys.exit(1)
    else:
        print("✅ 所有測試通過！程序運作正常")
        sys.exit(0)


if __name__ == "__main__":
    main()

