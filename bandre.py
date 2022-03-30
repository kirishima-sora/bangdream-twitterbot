import requests
from bs4 import BeautifulSoup
import csv
import urllib
import pandas as pd
from cgitb import text
from selenium import webdriver
import time

#スクレイピング先ページの取得
url_sc = "https://bang-dream.com/events"
response = requests.get(url_sc)
soup = BeautifulSoup(response.text, "html.parser")

#スクレイピング
elems = soup.find_all('ul', attrs={"class": "liveEventList"})
events = elems[0].find_all("li")

#イベント一覧リストの定義
event_list = []

#イベント一覧リストの作成
for event in enumerate(events):
    title = event[1].find('p', attrs={"class": "liveEventListTitle"}).text
    short_url_sc = event[1].find('a').get("href")
    long_url_sc = urllib.parse.urljoin(url_sc, short_url_sc)
    columns = event[1].find_all('div', attrs={"class": "itemInfoColumnTitle"})
    datas = event[1].find_all('div', attrs={"class": "itemInfoColumnData"})
    date = place = overview = None
    for i, column in enumerate(columns):
        try:
            if column.get_text() == "開催日時":
                date = datas[i].get_text()
            elif column.get_text() == "場所":
                place = datas[i].get_text()
            elif column.get_text() == "概要":
                overview = datas[i].get_text()
        except:
            print("colum data Error")
    event_list.append([title, long_url_sc, date, place, overview])

#CSV書き込み
with open("bangdream-sc.csv", "w", encoding="Shift_JIS") as file:
    writer = csv.writer(file, lineterminator="\n")
    writer.writerows(event_list)
