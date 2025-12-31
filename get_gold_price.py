import requests


def get_gold_price():
    """
    使用鉅亨網 API 獲取黃金現貨價格和開盤價
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        # 鉅亨網 API URL
        api_url = "https://ws.cnyes.com/ws/api/v1/quote/quotes/XAUUSD"
        
        # 發送請求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"API 請求失敗，狀態碼: {response.status_code}")
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
                print("無法從 API 獲取當前價格")
                return None
            
            if open_price is None:
                print("無法從 API 獲取開盤價，使用當前價格作為開盤價")
                open_price = current_price
            
            return {
                'current_price': float(current_price),
                'open_price': float(open_price)
            }
        else:
            print("API 回應格式錯誤")
            return None
    
    except Exception as e:
        print(f"獲取黃金價格時發生錯誤: {e}")
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
