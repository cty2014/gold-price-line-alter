#!/usr/bin/env python3
"""
檢查 GoldAPI.io API Key 設定狀態
"""

import os
import requests

def check_goldapi_key():
    """檢查 GoldAPI.io API Key 設定"""
    print("=" * 60)
    print("檢查 GoldAPI.io API Key 設定")
    print("=" * 60)
    print()
    
    # 檢查環境變數
    api_key = os.getenv("GOLDAPI_KEY")
    
    if not api_key or api_key.strip() == "":
        print("✗ GOLDAPI_KEY 環境變數未設定")
        print()
        print("設定方法:")
        print("1. 前往 GitHub 倉庫的 Settings → Secrets and variables → Actions")
        print("2. 點擊 'New repository secret'")
        print("3. Name: GOLDAPI_KEY")
        print("4. Secret: 您的 GoldAPI.io API Key")
        print("5. 點擊 'Add secret'")
        print()
        print("獲取 API Key:")
        print("1. 前往 https://www.goldapi.io/")
        print("2. 註冊帳號並登入")
        print("3. 在控制台中獲取您的 API Key")
        return False
    
    # 顯示 API Key 信息（隱藏大部分內容）
    api_key_cleaned = api_key.strip()
    api_key_length = len(api_key_cleaned)
    api_key_preview = api_key_cleaned[:10] + "..." + api_key_cleaned[-5:] if api_key_length > 15 else api_key_cleaned[:10] + "..."
    
    print(f"✓ GOLDAPI_KEY 環境變數已設定")
    print(f"  API Key 長度: {api_key_length} 字元")
    print(f"  API Key 預覽: {api_key_preview}")
    print()
    
    # 測試 API Key 是否有效
    print("測試 API Key 是否有效...")
    try:
        api_url = "https://www.goldapi.io/api/XAU/USD"
        headers = {
            'x-access-token': api_key_cleaned,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 檢查是否有錯誤訊息
            if 'error' in data or 'message' in data:
                error_msg = data.get('error') or data.get('message', 'Unknown error')
                print(f"✗ API Key 無效或 API 返回錯誤")
                print(f"  錯誤訊息: {error_msg}")
                return False
            
            # 檢查是否有價格數據
            if 'price' in data or 'rate' in data:
                price = float(data.get('price') or data.get('rate', 0))
                print(f"✓ API Key 有效！")
                print(f"  成功獲取黃金價格: ${price:.2f}")
                print()
                print("API 回應數據:")
                print(f"  - 當前價格: ${price:.2f}")
                if 'open_price' in data:
                    print(f"  - 開盤價格: ${data['open_price']:.2f}")
                if 'high_price' in data:
                    print(f"  - 當天最高: ${data['high_price']:.2f}")
                if 'low_price' in data:
                    print(f"  - 當天最低: ${data['low_price']:.2f}")
                return True
            else:
                print(f"✗ API 回應格式異常")
                print(f"  API 回應: {str(data)[:200]}")
                return False
                
        elif response.status_code == 401:
            print(f"✗ API Key 無效或未授權")
            print(f"  狀態碼: 401 Unauthorized")
            print()
            print("可能的原因:")
            print("1. API Key 錯誤")
            print("2. API Key 已過期")
            print("3. API Key 未啟用")
            print()
            print("解決方法:")
            print("1. 前往 https://www.goldapi.io/")
            print("2. 檢查 API Key 是否正確")
            print("3. 如果過期，重新生成 API Key")
            print("4. 更新 GitHub Secrets 中的 GOLDAPI_KEY")
            return False
            
        elif response.status_code == 429:
            print(f"⚠️  API 請求頻率過高")
            print(f"  狀態碼: 429 Too Many Requests")
            print()
            print("請稍後再試")
            return False
            
        else:
            print(f"✗ API 請求失敗")
            print(f"  狀態碼: {response.status_code}")
            print(f"  回應: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"✗ API 請求超時")
        print("  請檢查網路連線")
        return False
    except requests.exceptions.RequestException as e:
        print(f"✗ API 請求失敗: {e}")
        return False
    except Exception as e:
        print(f"✗ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_goldapi_key()
    print()
    print("=" * 60)
    if success:
        print("✓ GoldAPI.io 設定成功！")
    else:
        print("✗ GoldAPI.io 設定失敗或未設定")
    print("=" * 60)

