"""
網頁爬蟲腳本：抓取 i23.uk 網站的文章標題和內容
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_articles(url, num_articles=3):
    """
    抓取網站文章
    
    Args:
        url (str): 目標網址
        num_articles (int): 要抓取的文章數量
        
    Returns:
        list: 包含文章資訊的列表
    """
    
    try:
        print(f"開始抓取：{url}")
        
        # 設置請求頭，模擬瀏覽器訪問
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 發起請求
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        
        # 嘗試尋找文章容器（根據常見的網站結構）
        # 嘗試多種常見的選擇器
        article_containers = soup.find_all(['article', 'div'], class_=['post', 'article', 'entry', 'card'])
        
        if not article_containers:
            # 如果沒有找到，嘗試尋找所有 <article> 標籤
            article_containers = soup.find_all('article')
        
        if not article_containers:
            # 最後嘗試尋找具有標題的 <h> 標籤
            article_containers = soup.find_all(['h1', 'h2', 'h3'])
        
        print(f"找到 {len(article_containers)} 個可能的文章容器")
        
        for i, container in enumerate(article_containers[:num_articles]):
            # 提取標題
            title_elem = container.find(['h1', 'h2', 'h3', 'a'])
            title = title_elem.get_text(strip=True) if title_elem else "無標題"
            
            # 提取內容
            content_elem = container.find(['p', 'div', 'section'])
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            # 如果是在 h 標籤上，嘗試從後續段落抓內容
            if container.name in ['h1', 'h2', 'h3']:
                next_p = container.find_next('p')
                if next_p:
                    content = next_p.get_text(strip=True)
            
            if title and content:
                articles.append({
                    'title': title,
                    'content': content[:500]  # 取前 500 字
                })
                print(f"✓ 成功抓取文章 {len(articles)}: {title[:50]}")
        
        return articles
        
    except requests.RequestException as e:
        print(f"❌ 請求錯誤：{e}")
        return []
    except Exception as e:
        print(f"❌ 解析錯誤：{e}")
        return []


def save_to_txt(articles, filename=None):
    """
    將文章保存為 TXT 檔
    
    Args:
        articles (list): 文章列表
        filename (str): 檔案名稱（可選）
        
    Returns:
        str: 保存的檔案路徑
    """
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"articles_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("網站文章爬蟲結果\n")
            f.write("=" * 80 + "\n\n")
            
            for i, article in enumerate(articles, 1):
                f.write(f"【文章 {i}】\n")
                f.write(f"標題：{article['title']}\n")
                f.write(f"\n內容：\n{article['content']}\n")
                f.write("\n" + "-" * 80 + "\n\n")
        
        print(f"✓ 文件已保存：{filename}")
        return filename
        
    except Exception as e:
        print(f"❌ 保存文件失敗：{e}")
        return None


if __name__ == "__main__":
    # 目標網址
    target_url = "https://www.i23.uk/"
    
    # 抓取文章
    articles = scrape_articles(target_url, num_articles=3)
    
    # 保存結果
    if articles:
        print(f"\n成功抓取 {len(articles)} 篇文章\n")
        save_to_txt(articles, "i23_articles.txt")
    else:
        print("未能成功抓取文章")
