import requests
import os
from datetime import datetime


def get_gold_price():
    """
    使用 Alpha Vantage API 獲取黃金現貨價格（XAU/USD）
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        # 從環境變數獲取 API Key
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        
        if not api_key or api_key.strip() == "":
            print("⚠️  警告: ALPHA_VANTAGE_API_KEY 環境變數未設定")
            print("   嘗試使用備用 API (鉅亨網)...")
            return get_gold_price_fallback()
        
        # Alpha Vantage CURRENCY_EXCHANGE_RATE API
        # 獲取 XAU (黃金) 對 USD (美元) 的即時匯率
        api_url = "https://www.alphavantage.co/query"
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': 'XAU',
            'to_currency': 'USD',
            'apikey': api_key
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"Alpha Vantage API 請求失敗，狀態碼: {response.status_code}")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        data = response.json()
        
        # 檢查 API 回應
        if 'Error Message' in data:
            error_msg = data['Error Message']
            print(f"Alpha Vantage API 錯誤: {error_msg}")
            # 如果是無效的 API 調用，可能是 XAU 不被支援，嘗試使用備用 API
            if 'Invalid API call' in error_msg or 'does not exist' in error_msg:
                print("   注意: Alpha Vantage 可能不支援 XAU/USD，使用備用 API...")
            else:
                print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        if 'Note' in data:
            print(f"Alpha Vantage API 限制: {data['Note']}")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
        
        # 解析 API 回應
        if 'Realtime Currency Exchange Rate' in data:
            exchange_data = data['Realtime Currency Exchange Rate']
            current_price = float(exchange_data.get('5. Exchange Rate', 0))
            
            if current_price == 0:
                print("無法從 Alpha Vantage API 獲取當前價格")
                print("   嘗試使用備用 API...")
                return get_gold_price_fallback()
            
            # Alpha Vantage 的 CURRENCY_EXCHANGE_RATE API 只提供即時匯率
            # 沒有開盤價、最高價、最低價等數據
            # 使用當前價格作為近似值
            open_price = current_price
            day_high = current_price
            day_low = current_price
            
            print(f"✓ 使用 Alpha Vantage API 獲取數據")
            print(f"  當前價格: ${current_price:.2f}")
            
            return {
                'current_price': current_price,
                'open_price': open_price,
                'day_high': day_high,
                'day_low': day_low
            }
        else:
            print("Alpha Vantage API 回應格式錯誤")
            print(f"   回應內容: {str(data)[:200]}")
            print("   嘗試使用備用 API...")
            return get_gold_price_fallback()
    
    except Exception as e:
        print(f"獲取黃金價格時發生錯誤: {e}")
        print("   嘗試使用備用 API...")
        return get_gold_price_fallback()


def get_gold_price_fallback():
    """
    備用 API：使用鉅亨網 API 獲取黃金現貨價格
    當 Alpha Vantage API 無法使用時的回退方案
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        print("使用備用 API (鉅亨網) 獲取黃金價格...")
        # 鉅亨網 API URL
        api_url = "https://ws.cnyes.com/ws/api/v1/quote/quotes/XAUUSD"
        
        # 發送請求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"備用 API 請求失敗，狀態碼: {response.status_code}")
            return None
        
        data = response.json()
        
        # 解析 API 回應
        if 'data' in data and len(data['data']) > 0:
            quote_data = data['data'][0]
            
            # 獲取當前價格（最新價）
            current_price = quote_data.get('close', None) or quote_data.get('last', None)
            
            # 獲取開盤價
            open_price = quote_data.get('open', None)
            
            # 如果沒有開盤價，嘗試使用昨日收盤價
            if open_price is None:
                open_price = quote_data.get('previousClose', None) or quote_data.get('yesterdayClose', None)
            
            if current_price is None:
                print("無法從備用 API 獲取當前價格")
                return None
            
            if open_price is None:
                print("無法從備用 API 獲取開盤價，使用當前價格作為開盤價")
                open_price = current_price
            
            # 獲取當天最高價和最低價
            day_high = quote_data.get('high', None) or quote_data.get('dayHigh', None)
            day_low = quote_data.get('low', None) or quote_data.get('dayLow', None)
            
            # 如果沒有最高最低價，使用當前價格作為近似值
            if day_high is None:
                day_high = current_price
            if day_low is None:
                day_low = current_price
            
            return {
                'current_price': float(current_price),
                'open_price': float(open_price),
                'day_high': float(day_high),
                'day_low': float(day_low)
            }
        else:
            print("備用 API 回應格式錯誤")
            return None
    
    except Exception as e:
        print(f"備用 API 獲取失敗: {e}")
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
