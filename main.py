import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# 你揀邊隻股票呀大佬？改下面啦！
ticker = "AAPL"  # 想睇Tesla？改做TSLA啦

# 去Finviz撈新聞
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

# 整理數據，等你可以串人
data = pd.DataFrame({
    'Headline': headlines,
    'Sentiment': sentiments
})

# 畫圖，等你可以晒命
plt.figure(figsize=(10, 6))
plt.bar(range(len(sentiments)), sentiments)
plt.axhline(y=0, color='black', linestyle='-')
plt.title(f'你揀嘅{ticker}新聞情緒分析')  # 你睇，型唔型？
plt.xlabel('新聞編號')
plt.ylabel('情緒分數')
plt.savefig('sentiment_analysis.png')
plt.show()


print("===== 你揀嘅股票新聞情緒分析 =====")
print("睇清楚啦，唔好再問我點解輸錢！")
print(data)
print("\n（溫馨提示：呢個project唔包你發達，只包你型！）")
