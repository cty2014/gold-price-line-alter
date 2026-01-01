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
    使用幣安 API 獲取 PAXG/USDT 價格
    PAXG (Paxos Gold) 是與黃金掛鉤的穩定幣，1 PAXG = 1 盎司黃金
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    # 只使用幣安 API
    return get_gold_price_binance()


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
