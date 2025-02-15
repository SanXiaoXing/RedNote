"""
抖音热搜实时爬虫
版本：v1.1
依赖：requests
"""

import requests
import json
from datetime import datetime

def fetch_douyin_hot_search():
    """
    获取抖音实时热搜榜
    返回结构：
    [
        {
            "rank": 排名,
            "title": 热搜词,
            "hot_value": 热度值,
            "word_cover": 封面图URL,
            "sentence_id": 句子ID,
            "event_time": 时间戳
        },
        ...
    ]
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.douyin.com/discover"
    }
    
    # 抖音网页版热搜API（需自行更新Cookie）
    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = json.loads(response.text)
        hot_list = data.get('data').get('word_list')[:10]  # 取前十条
        
        formatted_data = []
        for index, item in enumerate(hot_list, 1):
            formatted_item = {
                "rank": index,
                "title": item.get('word'),
                "hot_value": item.get('hot_value'),
                "word_cover": item.get('word_cover').get('url_list')[0] if item.get('word_cover') else None,
                "sentence_id": item.get('sentence_id'),
                "event_time": datetime.fromtimestamp(item.get('event_time')).strftime('%Y-%m-%d %H:%M:%S')
            }
            formatted_data.append(formatted_item)
            
        return formatted_data
        
    except Exception as e:
        print(f"数据获取失败: {str(e)}")
        return None

def display_hot_search(data):
    """控制台格式化输出"""
    if not data:
        return
    
    print("\n🔥 抖音实时热搜TOP10\n" + "="*40)
    for item in data:
        print(f"{item['rank']:>2}. {item['title']}")
        print(f"   🔥 热度：{item['hot_value']} | 时间：{item['event_time']}")
        print("-"*40)

if __name__ == "__main__":
    hot_data = fetch_douyin_hot_search()
    display_hot_search(hot_data)