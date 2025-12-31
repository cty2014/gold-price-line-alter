import requests
import os
from datetime import datetime


def get_gold_price():
    """
    使用 GoldAPI.io 獲取黃金現貨價格（XAU/USD）
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        # 從環境變數獲取 API Key
        api_key = os.getenv("GOLDAPI_KEY")
        
        if not api_key or api_key.strip() == "":
            print("⚠️  警告: GOLDAPI_KEY 環境變數未設定")
            print("   嘗試使用備用 API (鉅亨網)...")
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
