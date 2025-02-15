"""
抖音热搜自动归档脚本
版本：v2.0
功能：获取热搜+自动生成日期目录+保存MD文件
"""

import os
import json
import requests
from datetime import datetime

def ensure_directory(date_str):
    """创建当日存储目录"""
    dir_path = os.path.join(os.getcwd(), date_str)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"已创建目录：{dir_path}")
    return dir_path

def generate_md_content(data, date_str):
    """生成Markdown文档内容"""
    md_header = f"""# 🎬 抖音热搜每日播报 | {date_str} 

> 数据更新于：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    md_body = "## 🔥 今日热搜TOP10\n\n"
    for item in data:
        md_body += f"### {item['rank']}. {item['title']}\n"
        md_body += f"- **热度值**：`{item['hot_value']}`\n"
        md_body += f"- **上榜时间**：{item['event_time']}\n"
        md_body += f"- [查看详情](https://www.douyin.com/hot/{item['sentence_id']})\n\n"
    
    md_footer = """---
**数据说明**：
1. 榜单数据每小时更新一次
2. 热度值基于搜索量与话题讨论度计算
"""
    return md_header + md_body + md_footer

def save_to_md(data, date_str):
    """保存为Markdown文件"""
    try:
        dir_path = ensure_directory(date_str)
        filename = f"{date_str}.md"
        file_path = os.path.join(dir_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            md_content = generate_md_content(data, date_str)
            f.write(md_content)
            
        print(f"文件已保存至：{file_path}")
        return True
    except Exception as e:
        print(f"文件保存失败: {str(e)}")
        return False

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

if __name__ == "__main__":
    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 获取热搜数据
    hot_data = fetch_douyin_hot_search()
    
    if hot_data:
        # 保存MD文件
        save_result = save_to_md(hot_data, current_date)
        
        # 控制台输出
        print("\n" + "="*40)
        print(f"📅 数据日期：{current_date}")
        print(f"📊 收录条目：{len(hot_data)}条")
        print("="*40)