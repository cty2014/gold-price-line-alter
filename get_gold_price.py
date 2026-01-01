import requests
import os
from datetime import datetime
import ssl
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

# 禁用 SSL 警告（如果使用 verify=False）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_gold_price():
    """
    獲取黃金現貨價格（XAU/USD）
    優先使用幣安 API，如果失敗則嘗試其他備用 API
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    # 優先使用幣安 API（最穩定可靠，無需 API Key）
    print("優先使用幣安 API 獲取黃金價格...")
    binance_result = get_gold_price_binance()
    if binance_result:
        return binance_result
    
    # 如果幣安 API 失敗，嘗試 GoldAPI.io（需要 API Key）
    try:
        # 從環境變數獲取 API Key
        api_key = os.getenv("GOLDAPI_KEY")
        
        if not api_key or api_key.strip() == "":
            print("⚠️  警告: GOLDAPI_KEY 環境變數未設定")
            print("   幣安 API 失敗，嘗試其他備用 API...")
            return get_gold_price_fallback()
        
        # GoldAPI.io API
        # 獲取 XAU (黃金) 對 USD (美元) 的即時價格
        api_url = "https://www.goldapi.io/api/XAU/USD"
        
        headers = {
            'x-access-token': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"GoldAPI.io API 請求失敗，狀態碼: {response.status_code}")
            if response.status_code == 401:
                print("   錯誤: API Key 無效或未授權")
            elif response.status_code == 429:
                print("   錯誤: API 請求頻率過高，請稍後再試")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        data = response.json()
        
        # 檢查 API 回應
        if 'error' in data or 'message' in data:
            error_msg = data.get('error') or data.get('message', 'Unknown error')
            print(f"GoldAPI.io API 錯誤: {error_msg}")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        # 解析 API 回應
        # GoldAPI.io 返回格式包含: price, open_price, high_price, low_price 等
        current_price = None
        
        # 獲取當前價格
        if 'price' in data:
            current_price = float(data['price'])
        elif 'rate' in data:
            current_price = float(data['rate'])
        elif 'value' in data:
            current_price = float(data['value'])
        else:
            print("無法從 GoldAPI.io API 獲取當前價格")
            print(f"   API 回應: {str(data)[:200]}")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        if current_price is None or current_price == 0:
            print("無法從 GoldAPI.io API 獲取當前價格")
            print(f"   API 回應: {str(data)[:200]}")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        # GoldAPI.io 提供開盤價、最高價、最低價
        # 優先使用 open_price，如果沒有則使用 prev_close_price
        open_price = data.get('open_price')
        if not open_price:
            open_price = data.get('prev_close_price', current_price)
        open_price = float(open_price) if open_price else current_price
        
        # 獲取最高價和最低價
        day_high = data.get('high_price')
        if not day_high:
            day_high = data.get('high', current_price)
        day_high = float(day_high) if day_high else current_price
        
        day_low = data.get('low_price')
        if not day_low:
            day_low = data.get('low', current_price)
        day_low = float(day_low) if day_low else current_price
        
        print(f"✓ 使用 GoldAPI.io API 獲取數據")
        print(f"  當前價格: ${current_price:.2f}")
        
        return {
            'current_price': current_price,
            'open_price': open_price,
            'day_high': day_high,
            'day_low': day_low
        }
    
    except Exception as e:
        print(f"獲取黃金價格時發生錯誤: {e}")
        print("   嘗試使用備用 API...")
        return get_gold_price_fallback()


def get_gold_price_binance():
    """
    使用幣安 API 獲取黃金價格（PAXG/USDT）
    PAXG (Paxos Gold) 是與黃金掛鉤的穩定幣，1 PAXG = 1 盎司黃金
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        print("嘗試使用幣安 API (Binance)...")
        api_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # 嘗試正常 SSL 連接，最多重試 3 次
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"  重試第 {attempt} 次...")
                
                response = requests.get(api_url, headers=headers, timeout=15, verify=True)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    # 請求頻率過高，等待後重試
                    if attempt < max_retries - 1:
                        import time
                        wait_time = (attempt + 1) * 2
                        print(f"  請求頻率過高，等待 {wait_time} 秒後重試...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"  幣安 API 請求頻率過高，狀態碼: {response.status_code}")
                        return None
                else:
                    print(f"  幣安 API 請求失敗，狀態碼: {response.status_code}")
                    if response.text:
                        print(f"  錯誤訊息: {response.text[:200]}")
                    return None
                    
            except (requests.exceptions.SSLError, ssl.SSLError) as ssl_error:
                # 如果 SSL 錯誤，嘗試使用備用 SSL 設定
                if attempt == 0:
                    print("  SSL 錯誤，嘗試使用備用 SSL 設定...")
                try:
                    response = requests.get(api_url, headers=headers, timeout=15, verify=False)
                    if response.status_code == 200:
                        break
                except Exception as e:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        print(f"  SSL 錯誤且備用設定也失敗: {e}")
                        return None
                        
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"  請求超時，重試中...")
                    continue
                else:
                    print(f"  幣安 API 請求超時")
                    return None
                    
            except requests.exceptions.ConnectionError as conn_error:
                if attempt < max_retries - 1:
                    print(f"  連接錯誤，重試中...")
                    import time
                    time.sleep(2)
                    continue
                else:
                    print(f"  幣安 API 連接失敗: {conn_error}")
                    return None
        else:
            print(f"  幣安 API 請求失敗，已重試 {max_retries} 次")
            return None
        
        # 解析回應
        try:
            data = response.json()
        except ValueError as json_error:
            print(f"  幣安 API 回應格式錯誤，無法解析 JSON: {json_error}")
            print(f"  回應內容: {response.text[:200]}")
            return None
        
        # 幣安 API 返回格式: {"symbol":"PAXGUSDT","price":"2345.67"}
        if 'price' in data:
            try:
                current_price = float(data['price'])
                
                if current_price > 0:
                    print(f"✓ 使用幣安 API 獲取數據成功")
                    print(f"  當前價格: ${current_price:.2f}")
                    
                    # 幣安 API 只提供當前價格，使用當前價格作為開盤價、最高價、最低價的近似值
                    return {
                        'current_price': current_price,
                        'open_price': current_price,  # 使用當前價格作為開盤價
                        'day_high': current_price,    # 使用當前價格作為最高價
                        'day_low': current_price      # 使用當前價格作為最低價
                    }
                else:
                    print(f"  幣安 API 返回的價格無效: {current_price}")
                    return None
            except (ValueError, TypeError) as price_error:
                print(f"  幣安 API 價格轉換失敗: {price_error}")
                print(f"  價格值: {data.get('price', 'N/A')}")
                return None
        else:
            print("  幣安 API 回應格式錯誤，缺少 'price' 欄位")
            print(f"  回應內容: {str(data)[:200]}")
            return None
            
    except Exception as e:
        print(f"  幣安 API 獲取失敗: {e}")
        import traceback
        print(f"  錯誤詳情:")
        traceback.print_exc()
        return None


def get_gold_price_fallback():
    """
    備用 API：嘗試其他免費 API 獲取黃金現貨價格
    當幣安 API 和 GoldAPI.io 都無法使用時的回退方案
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    # 嘗試其他備用 API（幣安 API 已在主函數中優先嘗試）
    # 嘗試多個備用 API
    fallback_apis = [
        ("MetalPrice API", "https://api.metals.live/v1/spot/gold"),
        ("ExchangeRate-API", "https://api.exchangerate-api.com/v4/latest/XAU"),
    ]
    
    for api_name, api_url in fallback_apis:
        try:
            print(f"嘗試使用備用 API ({api_name})...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # 嘗試正常 SSL 連接
            try:
                response = requests.get(api_url, headers=headers, timeout=10, verify=True)
            except (requests.exceptions.SSLError, ssl.SSLError) as ssl_error:
                # 如果 SSL 錯誤，嘗試使用較寬鬆的 SSL 設定（僅作為備用方案）
                print(f"  SSL 錯誤，嘗試使用備用 SSL 設定...")
                response = requests.get(api_url, headers=headers, timeout=10, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                
                # MetalPrice API 格式
                if 'price' in data or 'rate' in data:
                    current_price = float(data.get('price') or data.get('rate', 0))
                    if current_price > 0:
                        open_price = data.get('open', current_price) or current_price
                        day_high = data.get('high', current_price) or current_price
                        day_low = data.get('low', current_price) or current_price
                        
                        print(f"✓ 使用 {api_name} 獲取數據成功")
                        return {
                            'current_price': float(current_price),
                            'open_price': float(open_price),
                            'day_high': float(day_high),
                            'day_low': float(day_low)
                        }
                
                # ExchangeRate-API 格式
                if 'rates' in data:
                    usd_rate = data['rates'].get('USD', None)
                    if usd_rate:
                        # XAU 對 USD 的匯率，需要轉換
                        current_price = float(usd_rate)
                        if current_price > 0:
                            print(f"✓ 使用 {api_name} 獲取數據成功")
                            return {
                                'current_price': float(current_price),
                                'open_price': float(current_price),
                                'day_high': float(current_price),
                                'day_low': float(current_price)
                            }
        except Exception as e:
            print(f"  {api_name} 失敗: {e}")
            continue
    
    # 最後嘗試使用 Yahoo Finance API（通過公開的代理）
    try:
        print("嘗試使用 Yahoo Finance API...")
        # 使用公開的 Yahoo Finance API 代理
        api_url = "https://query1.finance.yahoo.com/v8/finance/chart/XAUUSD=X"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 嘗試正常 SSL 連接
        try:
            response = requests.get(api_url, headers=headers, timeout=10, verify=True)
        except requests.exceptions.SSLError:
            # 如果 SSL 錯誤，嘗試不驗證 SSL 證書
            print("  SSL 錯誤，嘗試使用備用 SSL 設定...")
            response = requests.get(api_url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})
                current_price = meta.get('regularMarketPrice', None)
                
                if current_price:
                    open_price = meta.get('previousClose', current_price) or current_price
                    day_high = meta.get('regularMarketDayHigh', current_price) or current_price
                    day_low = meta.get('regularMarketDayLow', current_price) or current_price
                    
                    print(f"✓ 使用 Yahoo Finance API 獲取數據成功")
                    return {
                        'current_price': float(current_price),
                        'open_price': float(open_price),
                        'day_high': float(day_high),
                        'day_low': float(day_low)
                    }
    except Exception as e:
        print(f"  Yahoo Finance API 失敗: {e}")
    
    print("✗ 所有備用 API 都無法獲取黃金價格")
    return None


if __name__ == "__main__":
    # 測試函數
    price_data = get_gold_price()
    if price_data:
        print(f"當前價格: ${price_data['current_price']:.2f}")
        print(f"開盤價格: ${price_data['open_price']:.2f}")
        change = ((price_data['current_price'] - price_data['open_price']) / price_data['open_price']) * 100
        print(f"漲跌幅: {change:+.2f}%")
    else:
        print("無法獲取黃金價格")
