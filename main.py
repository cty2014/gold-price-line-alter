from datetime import datetime
import os
import json
from get_gold_price import get_gold_price
from line_notify import send_line_push


def format_notification_message(current_price, day_high, day_low):
    """
    格式化 LINE 通知訊息（每日黃金價格報告格式）
    
    Args:
        current_price (float): 當前價格
        day_high (float): 當天最高價
        day_low (float): 當天最低價
    
    Returns:
        str: 格式化後的訊息
    """
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # 計算波動幅度
    if day_high > 0:
        volatility = ((day_high - day_low) / day_high) * 100
    else:
        volatility = 0.0
    
    # 格式化訊息（按照用戶要求的格式）
    message = "📊 每日黃金價格報告\n"
    message += f"報告時間: {current_time}\n"
    message += f"日期: {current_date}\n"
    message += f"當前價格: ${current_price:.2f}\n"
    message += "-------------------\n"
    message += f"當天最高: ${day_high:.2f}\n"
    message += f"當天最低: ${day_low:.2f}\n"
    message += f"波動幅度: {volatility:.2f}%"
    
    return message


def main():
    """
    主程式：每5分鐘發送一次日報表，或當價格波動超過5%時觸發警報通知
    """
    VOLATILITY_THRESHOLD = 5.0  # 5% 的波動閾值（當天最高價與最低價的波動）
    
    print("黃金價格監控系統啟動...")
    print(f"波動觸發閾值: {VOLATILITY_THRESHOLD}%")
    print("-" * 50)
    
    try:
        # 檢查環境變數是否設定（GitHub Actions）
        channel_token = os.getenv("CHANNEL_ACCESS_TOKEN")
        user_id = os.getenv("USER_ID")
        
        if not channel_token or channel_token.strip() == "":
            print("✗ 錯誤: CHANNEL_ACCESS_TOKEN 環境變數未設定")
            print("   請在 GitHub Secrets 中設定 CHANNEL_ACCESS_TOKEN")
            print("   程式無法繼續執行，請檢查 GitHub Actions Secrets 設定")
            return
        
        if not user_id or user_id.strip() == "":
            print("✗ 錯誤: USER_ID 環境變數未設定")
            print("   請在 GitHub Secrets 中設定 USER_ID")
            print("   程式無法繼續執行，請檢查 GitHub Actions Secrets 設定")
            return
        
        print(f"✓ 環境變數檢查通過")
        print(f"  CHANNEL_ACCESS_TOKEN: {'已設定' if channel_token else '未設定'}")
        print(f"  USER_ID: {'已設定' if user_id else '未設定'}")
        
        # 獲取黃金價格（包含當前價格和開盤價）
        price_data = get_gold_price()
        
        if price_data is None:
            error_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            taiwan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{error_time}] 無法獲取黃金價格")
            print("   這可能是 API 連接問題，請檢查網路連線")
            
            # 即使無法獲取價格，也發送錯誤通知（強制發送）
            error_message = f"⚠️ 黃金價格獲取失敗\n\n"
            error_message += f"報告時間: {taiwan_time}\n"
            error_message += f"UTC 時間: {error_time}\n"
            error_message += f"錯誤原因: 無法連接到黃金價格 API\n\n"
            error_message += f"已嘗試的 API:\n"
            error_message += f"1. GoldAPI.io (需要 API Key)\n"
            error_message += f"2. 多個備用 API\n\n"
            error_message += f"請檢查:\n"
            error_message += f"1. 網路連線是否正常\n"
            error_message += f"2. API 服務是否可用\n"
            error_message += f"3. GitHub Actions 執行環境是否正常\n"
            error_message += f"4. 是否設定了 GOLDAPI_KEY"
            
            print(f"\n準備發送錯誤通知到 LINE...")
            print(f"錯誤訊息內容:\n{error_message}\n")
            success = send_line_push(error_message)
            
            if success:
                print("✓ 錯誤通知已成功發送")
            else:
                print("✗ 錯誤通知發送失敗")
                print("   可能的原因:")
                print("   1. CHANNEL_ACCESS_TOKEN 未設定或無效")
                print("   2. USER_ID 未設定或無效")
                print("   3. LINE Bot API 連線問題")
            
            # 即使發送失敗也繼續執行，不要 return，讓後續邏輯知道發生了錯誤
            # 但由於 price_data 是 None，後續邏輯會因為 KeyError 而失敗
            # 所以我們應該 return，但確保錯誤通知已發送
            return
        
        current_price = price_data['current_price']
        open_price = price_data['open_price']
        day_high = price_data['day_high']
        day_low = price_data['day_low']
        
        # 計算當天的價格波動幅度（最高價與最低價的波動）
        if day_high > 0:
            volatility_percent = ((day_high - day_low) / day_high) * 100
        else:
            volatility_percent = 0.0
        
        # 計算相對於開盤價的漲跌幅
        change_percent = ((current_price - open_price) / open_price) * 100
        
        # 顯示當前狀態
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{current_time}] 當前價格: ${current_price:.2f} | "
              f"開盤價格: ${open_price:.2f} | 漲跌幅: {change_percent:+.2f}%")
        print(f"當天最高: ${day_high:.2f} | 當天最低: ${day_low:.2f} | 波動幅度: {volatility_percent:.2f}%")
        
        # 判斷是否應該發送報告
        # 現在改為每5分鐘發送一次日報表
        utc_now = datetime.utcnow()
        taiwan_time = datetime.now()
        
        # 輸出當前時間信息（用於調試）
        print(f"⏰ 當前時間資訊:")
        print(f"   UTC 時間: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   台灣時間: {taiwan_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 檢查是否為手動觸發（透過環境變數判斷）
        # GitHub Actions 手動觸發時會設定 GITHUB_EVENT_NAME
        github_event = os.getenv("GITHUB_EVENT_NAME", "")
        is_manual_trigger = github_event == "workflow_dispatch"
        print(f"   GitHub Event: {github_event}")
        print(f"   是否手動觸發: {is_manual_trigger}")
        
        # 每5分鐘執行一次，每次都發送日報表（無條件發送）
        # 移除時間窗口限制和重複發送檢查
        should_send_daily = True
        print(f"   📊 每5分鐘發送日報表模式：啟用")
        
        # 檢查波動是否超過5%（用於警報通知）
        should_send_alert = False
        if volatility_percent >= VOLATILITY_THRESHOLD:
            should_send_alert = True
            print(f"⚠️  價格波動超過 {VOLATILITY_THRESHOLD}% ({volatility_percent:.2f}%)，觸發警報")
        
        # 決定是否發送通知
        # 每日報告時間：無條件發送（不論波動是否超過5%）
        # 其他時間：只有波動超過5%時才發送警報
        should_send = should_send_daily or should_send_alert
        
        if is_manual_trigger:
            print(f"📊 手動觸發執行，發送報告")
        elif should_send_daily:
            print(f"📊 定期執行（每5分鐘），發送日報表")
        
        if should_send:
            if should_send_daily and should_send_alert:
                print(f"📊 準備發送每日黃金價格報告（價格波動超過 {VOLATILITY_THRESHOLD}%）...")
            elif should_send_daily:
                if is_manual_trigger:
                    print(f"📊 準備發送每日黃金價格報告（手動觸發）...")
                else:
                    print(f"📊 準備發送每日黃金價格報告...")
            else:
                print(f"⚠️  價格波動超過 {VOLATILITY_THRESHOLD}%，發送警報通知...")
            
            print(f"   發送條件:")
            if should_send_daily:
                print(f"   - 日報表: 是（每5分鐘發送一次）")
            if should_send_alert:
                print(f"   - 波動警報: 是（波動 {volatility_percent:.2f}% >= {VOLATILITY_THRESHOLD}%）")
            else:
                print(f"   - 波動警報: 否（波動 {volatility_percent:.2f}% < {VOLATILITY_THRESHOLD}%）")
            
            # 格式化通知訊息
            if should_send_alert:
                message = format_notification_message(current_price, day_high, day_low)
                message = f"⚠️ 價格波動警報\n\n" + message
            else:
                message = format_notification_message(current_price, day_high, day_low)
            
            # 發送 LINE 通知
            print(f"\n準備發送訊息到 LINE...")
            print(f"訊息內容預覽:\n{message}\n")
            
            try:
                success = send_line_push(message)
                
                if success:
                    print("✓ LINE 通知已成功發送")
                    # 記錄本次報告的發送時間（用於追蹤）
                    if should_send_daily:
                        try:
                            last_report_file = "last_report_time.json"
                            report_data = {
                                'date': utc_now.strftime('%Y-%m-%d'),
                                'time': utc_now.strftime('%Y-%m-%d %H:%M:%S'),
                                'taiwan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            with open(last_report_file, 'w', encoding='utf-8') as f:
                                json.dump(report_data, f, ensure_ascii=False, indent=2)
                            print(f"✓ 已記錄報告發送時間")
                        except Exception as e:
                            print(f"⚠️  記錄報告時間時發生錯誤: {e}")
                else:
                    print("✗ LINE 通知發送失敗")
                    print("   可能的原因:")
                    print("   1. CHANNEL_ACCESS_TOKEN 未設定或無效")
                    print("   2. USER_ID 未設定或無效")
                    print("   3. 用戶未加入 Bot 為好友")
                    print("   4. LINE Bot API 連線問題")
                    print("   5. Token 已過期或被撤銷")
                    # 不拋出異常，讓程式繼續執行，但記錄錯誤
                    print("   警告: 通知發送失敗，但程式繼續執行")
            except Exception as e:
                print(f"✗ 發送 LINE 通知時發生異常: {e}")
                import traceback
                traceback.print_exc()
                print("   警告: 通知發送失敗，但程式繼續執行")
        else:
            taiwan_time = datetime.now()
            print(f"✓ 價格波動在正常範圍內（{volatility_percent:.2f}% < {VOLATILITY_THRESHOLD}%），僅發送日報表")
            print(f"   當前 UTC 時間: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   當前台灣時間: {taiwan_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   是否手動觸發: {is_manual_trigger}")
            print("   不發送通知")
        
        print("-" * 50)
        print("程式執行完成")
    
    except Exception as e:
        error_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{'='*60}")
        print(f"[{error_time}] 發生錯誤: {e}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        
        # 嘗試發送錯誤通知
        try:
            error_message = f"❌ 系統錯誤\n\n"
            error_message += f"錯誤時間: {error_time}\n"
            error_message += f"錯誤訊息: {str(e)}\n\n"
            error_message += f"請檢查 GitHub Actions 執行日誌以獲取詳細資訊。"
            send_line_push(error_message)
        except:
            print("無法發送錯誤通知")
        
        raise


if __name__ == "__main__":
    main()
