import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt

# 輸入股票代號，唔好再冇啦
stock_symbol = input("輸入股票代號 (e.g. AAPL): ")
ticker = stock_symbol  # 用嚟display

def fetch_news(stock_symbol):
    url = f"https://finviz.com/quote.ashx?t={stock_symbol}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_table = soup.find(id='news-table')
    news_list = []
    for row in news_table.findAll('tr'):
        cols = row.findAll('td')
        if len(cols) > 1:
            news_list.append(cols[1].text.strip())
    return news_list

news = fetch_news(stock_symbol)
print("即時新聞:", news)

def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

sentiments = [sentiment_analysis(item) for item in news]
for i, item in enumerate(news):
    print(f"新聞 {i+1}: {item[:50]}... | 情緒分數: {sentiments[i]:.2f}")

# Bar chart
plt.figure(figsize=(10, 6))
plt.bar(range(len(sentiments)), sentiments)
plt.axhline(y=0, color='black', linestyle='-')
plt.title(f'{ticker} 新聞情緒分析')
plt.xlabel('新聞編號')
plt.ylabel('情緒分數')
plt.tight_layout()
plt.savefig('sentiment_analysis.png')
plt.close()

# Pie chart
labels = ['正面', '中立', '負面']
sizes = [
    sum([s > 0.1 for s in sentiments]),
    sum([abs(s) <= 0.1 for s in sentiments]),
    sum([s < -0.1 for s in sentiments])
]
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('新聞情緒分布')
plt.tight_layout()
plt.savefig('sentiment_pie.png')
plt.close()

# 生成Table內容（用番news同sentiments）
table_rows = []
for i in range(len(news)):
    table_rows.append(f'<tr><td>{news[i][:80]}</td><td>{sentiments[i]:.2f}</td></tr>')
table_content = '\n'.join(table_rows)

# index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(f'''
<!DOCTYPE html>
<html lang="zh-hk">
<head>
    <meta charset="UTF-8">
    <title>AhCry Finance - 股票新聞情緒分析</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 0; }}
        .navbar {{ background: #1a1a2e; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 24px; font-weight: bold; }}
        .container {{ padding: 20px; }}
        h1 {{ color: #1a1a2e; }}
        p {{ font-size: 18px; }}
        img {{ max-width: 100%; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #1a1a2e; color: white; }}
        .footer {{ background: #1a1a2e; color: white; text-align: center; padding: 15px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">AhCry Finance</div>
        <div>AI 財經助手</div>
    </div>
    <div class="container">
        <h1>{ticker} 股票新聞情緒分析</h1>
        <p>用 AI 分析市場情緒，早著先機！</p>
        <img src="sentiment_analysis.png" alt="情緒分析圖">
        <img src="sentiment_pie.png" alt="情緒分布餅圖">
        <p>（溫馨提示：本分析僅供參考，投資有風險，入市需謹慎！）</p>
        <table>
            <thead>
                <tr>
                    <th>新聞標題</th>
                    <th>情緒分數</th>
                </tr>
            </thead>
            <tbody>
                {table_content}
            </tbody>
        </table>
        <p>AhCry Finance - 型到震，你個friend睇到一定以為你係AI股神！</p>
    </div>
    <div class="footer">
        © 2025 AhCrySoLengLui Finance. All rights reserved.
    </div>
</body>
</html>
''')
