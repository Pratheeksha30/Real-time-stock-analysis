import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
from urllib.request import urlopen
from urllib.request import Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentiment import *

import nltk
nltk.download('vader_lexicon')

global conn 
global c

conn=sqlite3.connect('cust_data.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS cdata(
            usid text,
            s_nm text,
            s_no integer,
            s_p integer
          )   """)
usid=input("Enter the USER ID: ")
d=dict()
n=int(input("Enter the number of companies you have invested in: "))
for i in range(n):
  k = input("\nEnter company {} code: ".format(i+1))
  v = float(input("Price : "))
  m = int(input("No.of shares bought : "))
  print()
  d[k] = [v,m]

for x,y in d.items():
  c.execute("INSERT INTO cdata (usid, s_nm, s_no, s_p) VALUES ('{}', '{}', '{}', '{}')".format(usid,x,y[1],y[0]))
  y.append(y[0]/y[1])
  print(x, y)
conn.commit()

def sentiment():
    n = 5 #the # of article headlines displayed per ticker
    tickers = []
    for k in d.keys():
      tickers.append(k)

    # Get Data
    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    for ticker in tickers:
        url = finviz_url + ticker
        req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
        resp = urlopen(req)     
        html = BeautifulSoup(resp, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table

    try:
        for ticker in tickers:
            df = news_tables[ticker]
            df_tr = df.findAll('tr')
        
            print ('\n')
            print ('Recent News Headlines for {}: '.format(ticker))
            
            for i, table_row in enumerate(df_tr):
                a_text = table_row.a.text
                td_text = table_row.td.text
                td_text = td_text.strip()
                print(a_text,'(',td_text,')')
                if i == n-1:
                    break
    except KeyError:
        pass

    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text() 
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]
                
            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]
            
            parsed_news.append([ticker, date, time, text])

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    # View Data 
    news['Date'] = pd.to_datetime(news.Date).dt.date

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    values = []
    for ticker in tickers: 
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')
        dataframe = dataframe.drop(columns = ['Headline'])
        print ('\n')
        print (dataframe.head())
        
        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)
        
    df = pd.DataFrame(list(zip(tickers, values)), columns =['Ticker', 'Mean Sentiment']) 
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    print ('\n')
    print (df)

def real_time(stock_name):
        url = ("https://finance.yahoo.com/quote/"+stock_name+"/?p="+stock_name)
        r = requests.get(url)
        # print(r.text)
        r.encoding = "utf-8"
        page = r.text
        web_ = BeautifulSoup(page,"lxml")
        web_ = web_.find('div', class_ = "D(ib) Mend(20px)")
        web_ = web_.find("span").text
        return web_

real_values = dict()
for k in d.keys():
  real_values[k]=real_time(k)

for x,y in d.items():
  print("{} :\nStock purchased at : {}\tStock currently at : {}".format(x,y[2],real_values[x]))

sentiment()



