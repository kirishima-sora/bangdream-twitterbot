import requests
from bs4 import BeautifulSoup
import csv
# import pandas as pd

url = "https://bang-dream.com/events"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

elems = soup.find_all('ul', attrs={"class": "liveEventList"})
live_events = elems[0].find_all("li")

#live_events配列に各イベント情報がli区切りで入っている
live_event_title = live_events[0].find_all('p', attrs={"class": "liveEventListTitle"})
live_event_data = live_events[0].find_all('div', attrs={"class": "itemInfoColumnData"})

#titleにライブタイトル、dataに開催日時/場所/概要が入っている
print(live_event_title[0])
print(live_event_data[0])
print(live_event_data[1])



""" 
live_event_titles = soup.find_all('p', attrs={"class": "liveEventListTitle"})
live_event_dates = soup.find_all('div', attrs={"class": "itemInfoColumnData"})
live_event_title = live_event_titles[0]
live_event_date = live_event_dates[0]

print(live_event_title)
print(live_event_date)
 """

"""
result = []

for live_news in soup.find_all(class_="liveEventList"):
    result.append([
        live_news.text,
        live_news.get('href')
    ])

print(result)
"""


""" with open("site_source.csv", "w", encoding="Shift_JIS") as file:
    writer = csv.writer(file, lineterminator="\n")

        writer.writerows(row)

print(soup) """
