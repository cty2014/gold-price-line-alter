#!/usr/bin/env python3
"""
測試幣安 API 連接
"""

import requests
import json

def test_binance_api():
    """測試幣安 API"""
    print("=" * 60)
    print("測試幣安 API 連接")
    print("=" * 60)
    print()
    
    api_url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
    
    print(f"API URL: {api_url}")
    print()
    
    try:
        # 測試 1: 基本請求（無 headers）
        print("測試 1: 基本請求（無 headers）...")
        response = requests.get(api_url, timeout=10)
        print(f"  狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ 成功！價格: ${float(data['price']):.2f}")
        else:
            print(f"  ✗ 失敗: {response.text[:200]}")
    except Exception as e:
        print(f"  ✗ 錯誤: {e}")
    
    print()
    
    try:
        # 測試 2: 帶 headers 的請求
        print("測試 2: 帶 headers 的請求...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        print(f"  狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ 成功！價格: ${float(data['price']):.2f}")
        else:
            print(f"  ✗ 失敗: {response.text[:200]}")
    except Exception as e:
        print(f"  ✗ 錯誤: {e}")
    
    print()
    
    try:
        # 測試 3: 檢查網路連接
        print("測試 3: 檢查網路連接...")
        test_url = "https://www.binance.com"
        response = requests.get(test_url, timeout=5)
        print(f"  幣安網站連接: {'✓ 正常' if response.status_code == 200 else '✗ 異常'}")
    except Exception as e:
        print(f"  ✗ 網路連接問題: {e}")
    
    print()
    print("=" * 60)
    print("測試完成")
    print("=" * 60)

if __name__ == "__main__":
    test_binance_api()

