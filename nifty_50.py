import requests
from bs4 import BeautifulSoup
# from urllib.request import urlopen,  Request
tables = []
for i in range(30):
    url = ("https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9")
    r = requests.get(url)
    r.encoding = "utf-8"
    page = r.text
    web_ = BeautifulSoup(page,"lxml")
    table = web_.find('table',class_ = "tbldata14 bdrtpg").text
    tables.append(table)


strings = ["\n\n\n\n\nAdd to Watchlist\nAdd to Portfolio\n\n\n\n\n","\n\n\n\n","\n\n\n"]
new_set = [x.replace(strings[0], '').replace(strings[1], '\n').replace(strings[2], '\n') for x in tables]

lst =new_set[0].split("\n")
lst = lst[1:len(lst)-2]

new_lst = []
new_lst.append(' '.join(lst[0:6]))
for i in range(1,int(len(lst)/5)):
    new_lst.append('\t'.join(lst[(5*(i))+1:(5*(i+1))+1]))
for i in new_lst:
    print(i)

