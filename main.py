from datetime import datetime
import os
import json
from get_gold_price import get_gold_price
from get_bot_gold_price import get_bot_gold_price
from line_notify import send_line_push


def format_notification_message(current_price, day_high, day_low, bot_price=None):
    """
    格式化 LINE 通知訊息（每日黃金價格報告格式）
    
    Args:
        current_price (float): 當前價格（USD/盎司）
        day_high (float): 當天最高價（USD/盎司）
        day_low (float): 當天最低價（USD/盎司）
        bot_price (dict, optional): 台灣銀行價格，格式為 {'price': float, 'unit': str}
    
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
    message += "\n【國際價格（USD/盎司）】\n"
    message += f"當前價格: ${current_price:.2f}\n"
    message += "-------------------\n"
    message += f"當天最高: ${day_high:.2f}\n"
    message += f"當天最低: ${day_low:.2f}\n"
    message += f"波動幅度: {volatility:.2f}%\n"
    
    # 添加台灣銀行價格
    if bot_price and 'price' in bot_price:
        message += "\n【台灣銀行黃金牌告匯率】\n"
        message += f"本行賣出: {bot_price['price']:.2f} {bot_price.get('unit', '台幣/公克')}\n"
    else:
        message += "\n【台灣銀行黃金牌告匯率】\n"
        message += "本行賣出: 無法取得\n"
    
    return message


def main():
    """
    主程式：每小時監測一次數據
    - 價格超過5%時寄送通知
    - 如果沒有超過，每天早上10點和凌晨1:30發送日報表
    """
    PRICE_CHANGE_THRESHOLD = 5.0  # 5% 的價格變化閾值
    
    print("黃金價格監控系統啟動...")
    print(f"價格變化觸發閾值: {PRICE_CHANGE_THRESHOLD}%")
    print("日報表發送時間: 每天早上10:00 和 凌晨01:30 (台灣時間)")
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
            error_message += f"1. 幣安 API (Binance)\n\n"
            error_message += f"請檢查:\n"
            error_message += f"1. 網路連線是否正常\n"
            error_message += f"2. 幣安 API 服務是否可用\n"
            error_message += f"3. GitHub Actions 執行環境是否正常"
            
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
        
        # 獲取台灣銀行黃金牌告匯率
        print("\n嘗試獲取台灣銀行黃金牌告匯率...")
        bot_price_data = None
        try:
            bot_price_data = get_bot_gold_price()
            if bot_price_data:
                print(f"✓ 成功獲取台灣銀行價格: {bot_price_data['price']:.2f} {bot_price_data.get('unit', '台幣/公克')}")
            else:
                print("⚠️  無法獲取台灣銀行價格，將在報告中標註")
        except Exception as e:
            print(f"⚠️  獲取台灣銀行價格時發生錯誤: {e}")
            bot_price_data = None
        
        # 讀取上次價格
        last_price_file = "last_price.json"
        last_price = None
        
        try:
            if os.path.exists(last_price_file):
                with open(last_price_file, 'r', encoding='utf-8') as f:
                    last_data = json.load(f)
                    last_price = last_data.get('last_price')
                    if last_price:
                        print(f"✓ 讀取上次價格: ${last_price:.2f}")
        except Exception as e:
            print(f"⚠️  讀取上次價格時發生錯誤: {e}")
        
        # 計算價格變化百分比（相對於上次價格）
        price_change_percent = None
        if last_price and last_price > 0:
            price_change_percent = abs((current_price - last_price) / last_price) * 100
            change_direction = "上漲" if current_price > last_price else "下跌"
            print(f"  價格變化: {change_direction} {price_change_percent:.2f}% (相對於上次價格 ${last_price:.2f})")
        else:
            print("  這是首次執行，無法計算價格變化")
        
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
        utc_now = datetime.utcnow()
        taiwan_time = datetime.now()
        taiwan_hour = taiwan_time.hour
        taiwan_minute = taiwan_time.minute
        
        # 輸出當前時間信息（用於調試）
        print(f"\n⏰ 當前時間資訊:")
        print(f"   UTC 時間: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   台灣時間: {taiwan_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   台灣時間: {taiwan_hour:02d}:{taiwan_minute:02d}")
        
        # 檢查是否為手動觸發（透過環境變數判斷）
        github_event = os.getenv("GITHUB_EVENT_NAME", "")
        is_manual_trigger = github_event == "workflow_dispatch"
        print(f"   GitHub Event: {github_event}")
        print(f"   是否手動觸發: {is_manual_trigger}")
        
        # 檢查是否為日報表發送時間（早上10:00 或 凌晨01:30）
        # 允許5分鐘的誤差範圍（考慮 GitHub Actions 的延遲）
        is_daily_report_time = False
        
        # 早上10:00 (10:00-10:05)
        if taiwan_hour == 10 and 0 <= taiwan_minute <= 5:
            is_daily_report_time = True
            print(f"   ✓ 檢測到日報表發送時間: 早上10:00")
        
        # 凌晨01:30 (01:30-01:35)
        if taiwan_hour == 1 and 30 <= taiwan_minute <= 35:
            is_daily_report_time = True
            print(f"   ✓ 檢測到日報表發送時間: 凌晨01:30")
        
        if not is_daily_report_time and not is_manual_trigger:
            print(f"   ✗ 非日報表發送時間")
        
        # 檢查價格變化是否超過5%
        should_send_alert = False
        if price_change_percent and price_change_percent >= PRICE_CHANGE_THRESHOLD:
            should_send_alert = True
            print(f"\n⚠️  價格變化超過 {PRICE_CHANGE_THRESHOLD}% ({price_change_percent:.2f}%)，觸發警報通知")
        
        # 決定是否發送通知
        # 1. 價格變化超過5%：立即發送警報
        # 2. 日報表時間（早上10點或凌晨1:30）：發送日報表
        # 3. 手動觸發：發送日報表
        should_send = should_send_alert or is_daily_report_time or is_manual_trigger
        
        if should_send:
            if should_send_alert:
                print(f"\n⚠️  準備發送價格變化警報通知...")
                print(f"   發送原因: 價格變化 {price_change_percent:.2f}% >= {PRICE_CHANGE_THRESHOLD}%")
            elif is_daily_report_time:
                print(f"\n📊 準備發送每日黃金價格報告...")
                print(f"   發送原因: 日報表發送時間（{taiwan_hour:02d}:{taiwan_minute:02d}）")
            elif is_manual_trigger:
                print(f"\n📊 準備發送每日黃金價格報告（手動觸發）...")
            
            # 格式化通知訊息
            if should_send_alert:
                message = format_notification_message(current_price, day_high, day_low, bot_price_data)
                # 添加價格變化信息
                if price_change_percent:
                    change_direction = "上漲" if current_price > last_price else "下跌"
                    message = f"⚠️ 價格變化警報\n\n" + message
                    message += f"\n\n【價格變化】\n"
                    message += f"相對於上次價格: {change_direction} {price_change_percent:.2f}%\n"
                    message += f"上次價格: ${last_price:.2f}\n"
                    message += f"當前價格: ${current_price:.2f}"
            else:
                message = format_notification_message(current_price, day_high, day_low, bot_price_data)
            
            # 發送 LINE 通知
            print(f"\n準備發送訊息到 LINE...")
            print(f"訊息內容預覽:\n{message}\n")
            
            try:
                success = send_line_push(message)
                
                if success:
                    print("✓ LINE 通知已成功發送")
                    
                    # 保存當前價格到 last_price.json
                    try:
                        price_data_to_save = {
                            'last_price': current_price,
                            'timestamp': utc_now.strftime('%Y-%m-%d %H:%M:%S'),
                            'taiwan_time': taiwan_time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        with open(last_price_file, 'w', encoding='utf-8') as f:
                            json.dump(price_data_to_save, f, ensure_ascii=False, indent=2)
                        print(f"✓ 已保存當前價格到 {last_price_file}")
                    except Exception as e:
                        print(f"⚠️  保存價格時發生錯誤: {e}")
                    
                    # 記錄本次報告的發送時間（用於追蹤）
                    if is_daily_report_time or is_manual_trigger:
                        try:
                            last_report_file = "last_report_time.json"
                            report_data = {
                                'date': utc_now.strftime('%Y-%m-%d'),
                                'time': utc_now.strftime('%Y-%m-%d %H:%M:%S'),
                                'taiwan_time': taiwan_time.strftime('%Y-%m-%d %H:%M:%S')
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
            # 價格變化未超過5%，且非日報表時間，不發送通知
            print(f"\n✓ 價格變化在正常範圍內")
            if price_change_percent:
                print(f"   價格變化: {price_change_percent:.2f}% < {PRICE_CHANGE_THRESHOLD}%")
            print(f"   當前時間: {taiwan_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   非日報表發送時間，不發送通知")
            
            # 即使不發送通知，也保存當前價格
            try:
                price_data_to_save = {
                    'last_price': current_price,
                    'timestamp': utc_now.strftime('%Y-%m-%d %H:%M:%S'),
                    'taiwan_time': taiwan_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                with open(last_price_file, 'w', encoding='utf-8') as f:
                    json.dump(price_data_to_save, f, ensure_ascii=False, indent=2)
                print(f"✓ 已保存當前價格到 {last_price_file}")
            except Exception as e:
                print(f"⚠️  保存價格時發生錯誤: {e}")
        
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
