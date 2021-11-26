import requests
from bs4 import BeautifulSoup
import threading
from os import system, name
from sentiment import *

stocks = ["AAPL", "GOOG", "AMZN", "FB", "TSLA", "NFLX", "GC=F"]

def clear():
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
def real_time(stock_name):
            url = ("https://finance.yahoo.com/quote/"+stock_name+"/?p="+stock_name)
            r = requests.get(url)
            # print(r.text)
            r.encoding = "utf-8"
            page = r.text
            web_ = BeautifulSoup(page,"lxml")
            web_ = web_.find('div', class_ = "D(ib) Mend(20px)").text
            # web_ = web_.find("span").text
            return web_
def print_real_time_values(func):
        for i in stocks:
            print("Company : {}   Real time stock : {}".format(i,func(i)))

def setInterval(func1,func2,time):
        e = threading.Event()
        while not e.wait(time):
            clear()
            func1(func2)

setInterval(print_real_time_values,real_time,10)
sentiment()