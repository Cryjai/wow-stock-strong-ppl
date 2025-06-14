import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd

# 你揀邊隻股票呀大佬？改下面啦！
ticker = "AAPL"  # 想睇Tesla？改做TSLA啦，不過小心比Musk玩謝你！

# 去Finviz撈新聞，扮晒pro
url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
headers = {'User-Agent': 'Mozilla/5.0'}  # 扮browser，唔係會俾人ban
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 搵晒啲新聞標題，等你可以扮股神
news = soup.find_all('a', class_='tab-link-news')
headlines = [n.text for n in news]

# 情緒分析，睇下啲新聞係咪唱好你
sentiments = []
for headline in headlines:
    blob = TextBlob(headline)
    sentiments.append(blob.sentiment.polarity)

data = pd.DataFrame({
    'Headline': headlines,
    'Sentiment': sentiments
})

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.bar(range(len(sentiments)), sentiments)
plt.axhline(y=0, color='black', linestyle='-')
plt.title(f'你揀嘅{ticker}新聞情緒分析')
plt.xlabel('新聞編號')
plt.ylabel('情緒分數')
plt.savefig('sentiment_analysis.png')
plt.close()  # 唔好彈個圖出嚟，直接save

table_rows = []
for _, row in data.iterrows():
    table_rows.append(f'<tr><td>{row["Headline"]}</td><td>{row["Sentiment"]}</td></tr>')
table_content = '\n'.join(table_rows)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(f'''
<!DOCTYPE html>
<html lang="zh-hk">
<head>
    <meta charset="UTF-8">
    <title>股票新聞情緒分析（串爆版）</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #ff5500; }}
        p {{ font-size: 18px; }}
        img {{ max-width: 100%; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>股票新聞情緒分析（串爆版）</h1>
    <p>睇清楚啦，唔好再問我點解輸錢！</p>
    <img src="sentiment_analysis.png" alt="情緒分析圖">
    <p>（溫馨提示：呢個project唔包你發達，只包你型！）</p>
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
    <p>GitHub Pages 型到震，你個friend睇到一定以為你係AI股神！</p>
</body>
</html>
    ''')

# 輸出結果，串爆你friend
print("===== 你揀嘅股票新聞情緒分析 =====")
print("睇清楚啦，唔好再問我點解輸錢！")
print(data)
print("\n（溫馨提示：呢個project唔包你發達，只包你型！）")



print("===== 你揀嘅股票新聞情緒分析 =====")
print("睇清楚啦，唔好再問我點解輸錢！")
print(data)
print("\n（溫馨提示：呢個project唔包你發達，只包你型！）")
