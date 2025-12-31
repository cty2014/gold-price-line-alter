import yfinance as yf
import json
import os


# 儲存上一次價格的檔案路徑
PRICE_HISTORY_FILE = "last_price.json"


def get_gold_price():
    """
    獲取黃金現貨價格 (XAUUSD=X)
    
    Returns:
        float: 當前黃金價格，如果獲取失敗則返回 None
    """
    try:
        # 創建黃金現貨 ticker 對象
        gold = yf.Ticker("XAUUSD=X")
        
        # 獲取最新價格資訊
        info = gold.info
        
        # 嘗試從 info 中獲取當前價格
        # 通常會使用 'regularMarketPrice' 或 'previousClose'
        current_price = info.get('regularMarketPrice') or info.get('previousClose')
        
        if current_price is None:
            # 如果 info 中沒有價格，嘗試從歷史數據獲取最新價格
            hist = gold.history(period="1d", interval="1m")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
            else:
                return None
        
        return float(current_price)
    
    except Exception as e:
        print(f"獲取黃金價格時發生錯誤: {e}")
        return None


def load_last_price():
    """
    從檔案中載入上一次的價格
    
    Returns:
        float: 上一次的價格，如果檔案不存在則返回 None
    """
    try:
        if os.path.exists(PRICE_HISTORY_FILE):
            with open(PRICE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return float(data.get('last_price'))
        return None
    except Exception as e:
        print(f"讀取上一次價格時發生錯誤: {e}")
        return None


def save_price(price):
    """
    將當前價格儲存到檔案中
    
    Args:
        price (float): 要儲存的價格
    """
    try:
        with open(PRICE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({'last_price': price}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"儲存價格時發生錯誤: {e}")


def check_price_change(current_price, threshold_percent=5.0):
    """
    檢查當前價格與上一次價格的變化是否超過閾值
    
    Args:
        current_price (float): 當前價格
        threshold_percent (float): 價格變化閾值百分比（預設為 5.0，表示 5%）
    
    Returns:
        tuple: (alert: bool, change_percent: float, last_price: float)
            - alert: 是否需要觸發警示（True 表示變化超過閾值）
            - change_percent: 價格變化百分比（正數表示上漲，負數表示下跌）
            - last_price: 上一次的價格（如果沒有記錄則為 None）
    """
    last_price = load_last_price()
    
    # 如果沒有上一次的價格記錄，儲存當前價格並返回不觸發警示
    if last_price is None:
        save_price(current_price)
        return False, 0.0, None
    
    # 計算價格變化百分比
    change_percent = ((current_price - last_price) / last_price) * 100
    
    # 計算絕對變化百分比（無論漲跌）
    abs_change_percent = abs(change_percent)
    
    # 如果變化超過閾值，觸發警示
    alert = abs_change_percent >= threshold_percent
    
    # 更新儲存的價格
    save_price(current_price)
    
    return alert, change_percent, last_price


if __name__ == "__main__":
    # 測試函數
    price = get_gold_price()
    if price:
        print(f"當前黃金現貨價格: ${price:.2f}")
        
        # 檢查價格變化（設定閾值為 5%）
        alert, change_percent, last_price = check_price_change(price, threshold_percent=5.0)
        
        if last_price is not None:
            print(f"上一次價格: ${last_price:.2f}")
            print(f"價格變化: {change_percent:+.2f}%")
            
            if alert:
                print(f"⚠️  警示：價格變化超過 5%！")
            else:
                print(f"價格變化在正常範圍內（< 5%）")
        else:
            print("這是第一次檢查，已記錄當前價格")
    else:
        print("無法獲取黃金價格")

