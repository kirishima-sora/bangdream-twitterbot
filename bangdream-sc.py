import requests
from bs4 import BeautifulSoup
import csv
import urllib
# import pandas as pd

url = "https://bang-dream.com/events"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

elems = soup.find_all('ul', attrs={"class": "liveEventList"})
events = elems[0].find_all("li")

#全て合わさったリストの定義
event_list = []

#eventリストの作成
for event in enumerate(events):
    title = event[1].find('p', attrs={"class": "liveEventListTitle"}).text
    short_url = event[1].find('a').get("href")
    long_url = urllib.parse.urljoin(url, short_url)
    columns = event[1].find_all('div', attrs={"class": "itemInfoColumnTitle"})
    datas = event[1].find_all('div', attrs={"class": "itemInfoColumnData"})
    date = place = overview = None
    for i, column in enumerate(columns):
        if column.get_text() == "開催日時":
            date = datas[i].get_text()
        elif column.get_text() == "場所":
            place = datas[i].get_text()
        elif column.get_text() == "概要":
            overview = datas[i].get_text()
    event_list.append([title, long_url, date, place, overview])

#CSV書き込み
with open("bangdream-sc.csv", "w", encoding="Shift_JIS") as file:
    writer = csv.writer(file, lineterminator="\n")
    writer.writerows(event_list)


""" 
#events配列に各イベント情報がli区切りで入っている
event_title = events[0].find_all('p', attrs={"class": "liveEventListTitle"})
event_url = events[0].find_all('a')
event_column = events[0].find_all('div', attrs={"class": "itemInfoColumnTitle"})
event_data = events[0].find_all('div', attrs={"class": "itemInfoColumnData"})

#titleにライブタイトル、dataに開催日時/場所/概要、urlにはリンクが入っている
print(event_title[0])
print(event_column[0])
print(event_data[0])
print(event_column[1])
print(event_data[1])
print(event_url[0]).attrs['href']
 """


