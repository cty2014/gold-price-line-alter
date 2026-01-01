"""
台灣銀行黃金牌告匯率爬取模組
使用 requests 和 BeautifulSoup 爬取台灣銀行的黃金存摺價格
"""

import requests
from bs4 import BeautifulSoup
import re


def get_bot_gold_price():
    """
    爬取台灣銀行黃金牌告匯率頁面，獲取「本行賣出」的黃金存摺價格（台幣/公克）
    
    Returns:
        dict: 包含價格信息的字典，格式如下：
            {
                'price': float,  # 價格（台幣/公克）
                'unit': str,      # 單位（通常是 '台幣/公克'）
                'source': str     # 數據來源（'台灣銀行'）
            }
            如果獲取失敗則返回 None
    """
    url = 'https://rate.bot.com.tw/gold?Lang=zh-TW'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        print("嘗試爬取台灣銀行黃金牌告匯率...")
        print(f"  目標網址: {url}")
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 檢查回應編碼
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 方法1: 尋找包含「黃金存摺」的表格行
        # 台灣銀行的表格結構可能有多種，我們嘗試多種方法
        
        # 尋找所有表格
        tables = soup.find_all('table')
        
        if not tables:
            print("  錯誤: 無法找到表格")
            return None
        
        print(f"  找到 {len(tables)} 個表格")
        
        # 遍歷所有表格尋找「黃金存摺」相關資料
        for table_idx, table in enumerate(tables):
            rows = table.find_all('tr')
            
            # 首先找到表頭行，確認「本行賣出」的欄位索引
            sell_column_index = None
            
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['th', 'td'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # 尋找包含「本行賣出」的表頭行
                if '本行賣出' in cell_texts:
                    sell_column_index = cell_texts.index('本行賣出')
                    print(f"  在表格 {table_idx + 1} 找到表頭，「本行賣出」位於第 {sell_column_index + 1} 欄")
                    break
            
            # 如果找到表頭，尋找「黃金存摺」的數據行
            if sell_column_index is not None:
                for row_idx, row in enumerate(rows):
                    cells = row.find_all(['td', 'th'])
                    row_text = row.get_text()
                    
                    # 檢查是否包含「黃金存摺」
                    if '黃金存摺' in row_text and len(cells) > sell_column_index:
                        cell_texts = [cell.get_text(strip=True) for cell in cells]
                        
                        # 獲取「本行賣出」欄位的價格
                        price_text = cell_texts[sell_column_index]
                        price = _extract_price(price_text)
                        
                        # 黃金存摺價格通常在 2000-5000 台幣/公克之間
                        if price and 1000 < price < 10000:
                            print(f"  ✓ 成功獲取黃金存摺本行賣出價格: {price} 台幣/公克")
                            return {
                                'price': price,
                                'unit': '台幣/公克',
                                'source': '台灣銀行'
                            }
                        elif price:
                            print(f"  ⚠️  找到價格 {price}，但可能不是正確的欄位，繼續尋找...")
        
        # 如果上述方法都失敗，嘗試使用更通用的方法
        print("  嘗試使用通用方法尋找價格...")
        
        # 尋找所有包含數字的文字，並檢查上下文
        all_text = soup.get_text()
        
        # 使用正則表達式尋找價格模式
        # 台灣銀行的價格格式通常是：數字,數字.數字 或 數字.數字
        price_pattern = r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)'
        matches = re.findall(price_pattern, all_text)
        
        # 尋找「黃金存摺」附近的價格
        gold_index = all_text.find('黃金存摺')
        if gold_index != -1:
            # 在「黃金存摺」附近尋找價格
            nearby_text = all_text[max(0, gold_index - 200):gold_index + 500]
            
            # 尋找「本行賣出」附近的數字
            sell_index = nearby_text.find('本行賣出')
            if sell_index != -1:
                # 在「本行賣出」後尋找價格
                after_sell = nearby_text[sell_index:sell_index + 100]
                price_matches = re.findall(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', after_sell)
                
                for match in price_matches:
                    price = _extract_price(match)
                    if price and price > 100:  # 黃金價格應該大於 100
                        print(f"  ✓ 成功獲取黃金存摺本行賣出價格: {price} 台幣/公克")
                        return {
                            'price': price,
                            'unit': '台幣/公克',
                            'source': '台灣銀行'
                        }
        
        print("  ✗ 無法找到黃金存摺本行賣出價格")
        print(f"  網頁內容預覽（前500字元）: {response.text[:500]}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ HTTP 請求錯誤: {e}")
        return None
    except Exception as e:
        print(f"  ✗ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None


def _extract_price(price_text):
    """
    從文字中提取價格數字
    
    Args:
        price_text (str): 包含價格的文字
        
    Returns:
        float: 提取的價格，如果無法提取則返回 None
    """
    try:
        # 移除逗號和空格
        cleaned = price_text.replace(',', '').replace(' ', '').strip()
        # 提取數字
        match = re.search(r'(\d+\.?\d*)', cleaned)
        if match:
            return float(match.group(1))
    except:
        pass
    return None


if __name__ == "__main__":
    # 測試函數
    print("=" * 60)
    print("測試台灣銀行黃金牌告匯率爬取功能")
    print("=" * 60)
    print()
    
    result = get_bot_gold_price()
    
    if result:
        print()
        print("=" * 60)
        print("✓ 測試成功！")
        print("=" * 60)
        print(f"價格: {result['price']} {result['unit']}")
        print(f"數據來源: {result['source']}")
    else:
        print()
        print("=" * 60)
        print("✗ 測試失敗！無法獲取價格")
        print("=" * 60)

