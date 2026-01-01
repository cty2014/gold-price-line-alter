import requests
import os
import sys
from datetime import datetime
import ssl
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

# 禁用 SSL 警告（如果使用 verify=False）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_gold_price():
    """
    獲取黃金現貨價格（XAU/USD）
    優先使用 CoinGecko API 獲取 PAXG/USD 價格
    如果 CoinGecko API 失敗，則使用幣安 API 作為備用
    PAXG (Paxos Gold) 是與黃金掛鉤的穩定幣，1 PAXG = 1 盎司黃金
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    # 優先使用 CoinGecko API（無地理位置限制）
    result = get_gold_price_coingecko()
    
    # 如果 CoinGecko API 失敗，使用幣安 API 作為備用
    if result is None:
        print("CoinGecko API 失敗，嘗試使用幣安 API 作為備用...")
        result = get_gold_price_binance()
    
    return result


def get_gold_price_binance():
    """
    使用幣安 API 獲取黃金價格（PAXG/USDT）
    PAXG (Paxos Gold) 是與黃金掛鉤的穩定幣，1 PAXG = 1 盎司黃金
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        # 檢測是否在 GitHub Actions 環境中
        is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
        if is_github_actions:
            print("🔍 檢測到 GitHub Actions 環境")
            print(f"  Runner OS: {os.getenv('RUNNER_OS', 'Unknown')}")
            print(f"  Python 版本: {sys.version.split()[0]}")
            # 測試網路連接
            try:
                import socket
                socket.setdefaulttimeout(5)
                socket.create_connection(("api.binance.com", 443), timeout=5)
                print("  ✓ 網路連接到 api.binance.com 正常")
            except Exception as net_test_error:
                print(f"  ⚠️  網路連接測試失敗: {net_test_error}")
        
        print("嘗試使用幣安 API (Binance)...")
        api_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        print(f"  API URL: {api_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # 在 GitHub Actions 環境中，增加超時時間
        timeout = 30 if is_github_actions else 15
        print(f"  請求超時設定: {timeout} 秒")
        
        # 嘗試正常 SSL 連接，最多重試 5 次（GitHub Actions 環境中增加重試次數）
        max_retries = 5 if is_github_actions else 3
        print(f"  最大重試次數: {max_retries}")
        response = None
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"  重試第 {attempt} 次...")
                
                response = requests.get(api_url, headers=headers, timeout=timeout, verify=True)
                
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
                        if response.text:
                            print(f"  錯誤訊息: {response.text[:200]}")
                        return None
                elif response.status_code == 451:
                    # 451 錯誤表示地理位置限制，不需要重試，直接返回 None 讓備用 API 處理
                    print(f"  幣安 API 返回 451 錯誤（地理位置限制）")
                    if response.text:
                        print(f"  錯誤訊息: {response.text[:200]}")
                    print("  將嘗試使用備用 API...")
                    return None
                else:
                    print(f"  幣安 API 請求失敗，狀態碼: {response.status_code}")
                    if response.text:
                        print(f"  錯誤訊息: {response.text[:200]}")
                    # 非 429/451 錯誤時，如果不是最後一次重試，繼續重試
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(2)
                        continue
                    else:
                        return None
                    
            except (requests.exceptions.SSLError, ssl.SSLError) as ssl_error:
                # 如果 SSL 錯誤，嘗試使用備用 SSL 設定
                if attempt == 0:
                    print(f"  SSL 錯誤: {ssl_error}，嘗試使用備用 SSL 設定...")
                try:
                    response = requests.get(api_url, headers=headers, timeout=timeout, verify=False)
                    if response.status_code == 200:
                        print("  ✓ 使用備用 SSL 設定成功")
                        break
                    else:
                        print(f"  備用 SSL 設定請求失敗，狀態碼: {response.status_code}")
                        if attempt < max_retries - 1:
                            import time
                            time.sleep(2)
                            continue
                        else:
                            return None
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"  備用 SSL 設定也失敗: {e}，重試中...")
                        import time
                        time.sleep(2)
                        continue
                    else:
                        print(f"  SSL 錯誤且備用設定也失敗: {e}")
                        return None
                        
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"  請求超時，重試中...")
                    import time
                    time.sleep(2)
                    continue
                else:
                    print(f"  幣安 API 請求超時，已重試 {max_retries} 次")
                    return None
                    
            except requests.exceptions.ConnectionError as conn_error:
                if attempt < max_retries - 1:
                    print(f"  連接錯誤: {conn_error}，重試中...")
                    import time
                    time.sleep(2)
                    continue
                else:
                    print(f"  幣安 API 連接失敗: {conn_error}")
                    return None
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  發生錯誤: {e}，重試中...")
                    import time
                    time.sleep(2)
                    continue
                else:
                    print(f"  幣安 API 請求發生未預期錯誤: {e}")
                    import traceback
                    traceback.print_exc()
                    return None
        
        # 檢查 response 是否存在
        if response is None:
            print(f"  幣安 API 請求失敗，無法獲取回應")
            return None
        
        if response.status_code != 200:
            print(f"  幣安 API 請求失敗，狀態碼: {response.status_code}")
            if response.text:
                print(f"  錯誤訊息: {response.text[:200]}")
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


def get_gold_price_coingecko():
    """
    使用 CoinGecko API 獲取黃金價格（PAXG/USD）
    CoinGecko 是免費的加密貨幣和商品價格 API，沒有地理位置限制
    PAXG (Paxos Gold) 是與黃金掛鉤的穩定幣，1 PAXG = 1 盎司黃金
    
    Returns:
        dict: 包含 current_price (當前價格) 和 open_price (開盤價) 的字典
              如果獲取失敗則返回 None
    """
    try:
        print("嘗試使用 CoinGecko API...")
        # CoinGecko API: 獲取 PAXG 價格（以 USD 計價）
        # PAXG 的 CoinGecko ID 是 "pax-gold"
        api_url = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        print(f"  API URL: {api_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # CoinGecko 免費 API 有速率限制，但通常比幣安更寬鬆
        timeout = 30
        max_retries = 3
        print(f"  請求超時設定: {timeout} 秒")
        print(f"  最大重試次數: {max_retries}")
        
        response = None
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"  重試第 {attempt} 次...")
                    import time
                    time.sleep(2)
                
                response = requests.get(api_url, headers=headers, timeout=timeout, verify=True)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    # 請求頻率過高，等待後重試
                    if attempt < max_retries - 1:
                        import time
                        wait_time = (attempt + 1) * 3
                        print(f"  請求頻率過高，等待 {wait_time} 秒後重試...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"  CoinGecko API 請求頻率過高，狀態碼: {response.status_code}")
                        return None
                else:
                    print(f"  CoinGecko API 請求失敗，狀態碼: {response.status_code}")
                    if response.text:
                        print(f"  錯誤訊息: {response.text[:200]}")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return None
                        
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"  請求超時，重試中...")
                    continue
                else:
                    print(f"  CoinGecko API 請求超時，已重試 {max_retries} 次")
                    return None
                    
            except requests.exceptions.ConnectionError as conn_error:
                if attempt < max_retries - 1:
                    print(f"  連接錯誤: {conn_error}，重試中...")
                    continue
                else:
                    print(f"  CoinGecko API 連接失敗: {conn_error}")
                    return None
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  發生錯誤: {e}，重試中...")
                    continue
                else:
                    print(f"  CoinGecko API 請求發生錯誤: {e}")
                    return None
        
        # 檢查 response 是否存在
        if response is None or response.status_code != 200:
            print(f"  CoinGecko API 請求失敗")
            return None
        
        # 解析回應
        try:
            data = response.json()
        except ValueError as json_error:
            print(f"  CoinGecko API 回應格式錯誤，無法解析 JSON: {json_error}")
            print(f"  回應內容: {response.text[:200]}")
            return None
        
        # CoinGecko API 返回格式: {"pax-gold":{"usd":2345.67,"usd_24h_change":0.5}}
        if 'pax-gold' in data and 'usd' in data['pax-gold']:
            try:
                current_price = float(data['pax-gold']['usd'])
                
                if current_price > 0:
                    print(f"✓ 使用 CoinGecko API 獲取數據成功")
                    print(f"  當前價格: ${current_price:.2f}")
                    
                    # CoinGecko 提供 24 小時變化，可以用來估算開盤價
                    # 如果沒有變化數據，使用當前價格作為開盤價
                    if 'usd_24h_change' in data['pax-gold']:
                        change_percent = float(data['pax-gold']['usd_24h_change'])
                        open_price = current_price / (1 + change_percent / 100)
                    else:
                        open_price = current_price
                    
                    # 使用當前價格作為最高價和最低價的近似值
                    return {
                        'current_price': current_price,
                        'open_price': open_price,
                        'day_high': current_price,
                        'day_low': current_price
                    }
                else:
                    print(f"  CoinGecko API 返回的價格無效: {current_price}")
                    return None
            except (ValueError, TypeError, KeyError) as price_error:
                print(f"  CoinGecko API 價格轉換失敗: {price_error}")
                print(f"  回應數據: {str(data)[:200]}")
                return None
        else:
            print("  CoinGecko API 回應格式錯誤，缺少 'pax-gold.usd' 欄位")
            print(f"  回應內容: {str(data)[:200]}")
            return None
            
    except Exception as e:
        print(f"  CoinGecko API 獲取失敗: {e}")
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
