import requests
from bs4 import BeautifulSoup
import threading
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def print_real_time_values():
        url = ("https://finance.yahoo.com/quote/GC=F/?p=GC=F")
        r = requests.get(url)
        # print(r.text)
        r.encoding = "utf-8"
        page = r.text
        web_ = BeautifulSoup(page,"lxml")
        web_ = web_.find('div', class_ = "D(ib) Mend(20px)").text
        print("Gold Real time stock price : ",web_)

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        clear()
        func()

setInterval(print_real_time_values,3)