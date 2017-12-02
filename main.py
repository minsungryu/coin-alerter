#-*- coding: utf-8 -*-
import os
import sys
import threading
from time import sleep
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
from playsound import playsound

reload(sys)  
sys.setdefaultencoding('utf8')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printout(str):
    sys.stdout.write(str)
    sys.stdout.flush()

def alert():
    playsound('./Alarm.wav')

def initialize():
    chrome = webdriver.Chrome('./chromedriver')
    chrome.get('https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC')
    return chrome    

def checkIsOnMarket(browser, interval):
    soup = BeautifulSoup(browser.page_source, 'lxml')

    coin_table = soup.select('#root > div > div > div.mainB > section.ty02 > article > span.tabB > div > div > div > div > table > tbody')
    rows = coin_table[0].find_all('tr')
    
    find = False
    printout("[")
    printout(str(datetime.now()))
    printout("] ")
    for row in rows:
        cols = row.find_all('td')
        coin_name = cols[2].text
        coin_tran = cols[5].text
        if coin_tran == u"0백만":
            find = True
            global alert_thread
            if not alert_thread.is_alive():
                try:
                    alert_thread.start()
                except RuntimeError:
                    alert_thread = threading.Thread(target=alert)
                    alert_thread.start()
            printout(coin_name)
            printout(" => ")
            printout(coin_tran)

    if find is False:
        printout(u"신규 상장 발견되지 않음")

    find = False
    sleep(interval)
    print ""
    # clear()
    # browser.refresh()
 
chrome = initialize()
sleep(5)
alert_thread = threading.Thread(target=alert)
try:
    while True:
        checkIsOnMarket(chrome, 0.5)
finally:
    # pass
    chrome.close()
    chrome.quit()