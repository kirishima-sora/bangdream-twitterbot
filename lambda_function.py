from copy import copy
from unicodedata import category
import requests
from bs4 import BeautifulSoup
import csv
import urllib
import pandas as pd
from cgitb import text
import time
import os
import datetime
import boto3
import tweepy
import io

#lambdaで最初に実行される関数
def lambda_handler(event, context):
    #スクレイピング先ページの取得
    url_sc = "https://bang-dream.com/events"
    response = requests.get(url_sc)
    soup = BeautifulSoup(response.text, "html.parser")

    #スクレイピング
    elems = soup.find_all('ul', attrs={"class": "liveEventList"})
    events = elems[0].find_all("li")

    #イベント一覧リストの定義
    event_list = []
    event_list.append(["タイトル", "URL", "日付", "場所", "概要", "カテゴリ"])

    #イベント一覧リストの作成
    for event_unit in enumerate(events):
        title = event_unit[1].find('p', attrs={"class": "liveEventListTitle"}).text
        short_url_sc = event_unit[1].find('a').get("href")
        long_url_sc = urllib.parse.urljoin(url_sc, short_url_sc)
        columns = event_unit[1].find_all('div', attrs={"class": "itemInfoColumnTitle"})
        datas = event_unit[1].find_all('div', attrs={"class": "itemInfoColumnData"})
        date = place = overview = info = "None"
        for i, column in enumerate(columns):
            if column.get_text() == "開催日時":
                date = datas[i].get_text()
            elif column.get_text() == "場所":
                place = datas[i].get_text()
            elif column.get_text() == "概要":
                overview = datas[i].get_text()
        event_list.append([title, long_url_sc, date, place, overview, info])

    #S3バケット内でのファイル生成準備
    s3 = boto3.resource('s3')
    bucket_name = "bangdream-eventlist"
    bucket = s3.Bucket(bucket_name)
    s3_filename_new = 'bandre-event.csv'
    s3_filename_old = 'bandre-event-old.csv'

    #lambda実行時の一時ファイルパス
    tmp_path = "/tmp/data.csv"

    #CSV書き込み
    with open(tmp_path, "w", encoding="Shift_JIS") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerows(event_list)

    #S3バケットへのファイルアップロード
    bucket.upload_file(tmp_path, s3_filename_new)

    #tmpファイルの削除
    os.remove(tmp_path)

    #s3バケットからcsv読み込み
    df_old_bucket = s3.Object(bucket_name, s3_filename_old)
    body_in = df_old_bucket.get()['Body'].read().decode("Shift_JIS")
    buffer_in = io.StringIO(body_in)
    df_old = pd.read_csv(buffer_in, lineterminator='\n')
    #newも同様
    df_new_bucket = s3.Object(bucket_name, s3_filename_new)
    body_in = df_new_bucket.get()['Body'].read().decode("Shift_JIS")
    buffer_in = io.StringIO(body_in)
    df_new = pd.read_csv(buffer_in, lineterminator='\n')

    #新情報の行数(shift_num)の確認
    for shift_num in range(10):
        if df_old.iat[0,0] == df_new.iat[shift_num,0]:
            break

    #新情報の行数だけずらすリストの定義
    df_old_comv = df_old.copy()
    df_new_comv = df_new.copy()

    #新情報の行数だけずらす処理
    for drop_num in range(shift_num):
        df_old_comv = df_old_comv.drop(df_old_comv.index[9-drop_num])
        df_new_comv = df_new_comv.drop(df_new_comv.index[0])

    #ずれたインデックスの振り直し
    df_old_comv = df_old_comv.reset_index(drop=True)
    df_new_comv = df_new_comv.reset_index(drop=True)

    #比較結果リストの作成（true,false判定）
    df_comp = (df_old_comv==df_new_comv)

    #更新カテゴリ入れ
    for row in range(10-shift_num):
        info = "None"
        if ((df_comp.iat[row, 2] == False) and (df_comp.iat[row, 3] == False)) or (df_comp.iat[row, 0] == False) or (df_comp.iat[row, 4] == False):
            info = "情報更新"
        elif df_comp.iat[row, 2] == False:
            info = "日程情報更新"
        elif df_comp.iat[row, 3] == False:
            info = "場所情報更新"
        df_comp.iat[row, 5] = info

    #ツイート内容を入れる配列を作成
    tweet_array = []

    #新情報のツイート内容作成
    for row in range(shift_num):
        text = "【新情報】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
        tweet_array.append(text.format(title=df_new.iat[row,0], date=df_new.iat[row,2], place=df_new.iat[row,3], URL=df_new.iat[row,1]))

    #情報更新のツイート内容作成
    for row in range(10-shift_num):
        if df_comp.iat[row,5] != "None":
            text = "【{info}】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
            tweet_array.append(text.format(info=df_comp.iat[row,5], title=df_new_comv.iat[row,0], date=df_new_comv.iat[row,2], place=df_new_comv.iat[row,3], URL=df_new_comv.iat[row,1]))


    #更新があれば自動ツイートとcsvリネーム処理を実行
    if (shift_num != 0) or (df_old_comv.equals(df_new_comv) == False):
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_KEY_SECRET']
        access_token = os.environ['ACCESS_TOKEN_KEY']
        access_token_secret = os.environ['ACCESS_TOKEN_KEY_SECRET']

        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        #情報のツイート
        for tweet in enumerate(tweet_array):
            # ツイートを投稿
            api.update_status(tweet[1])

        #csv更新処理
        #現在の日時と日付の文字列変換
        dt_now = datetime.datetime.now()
        d_today = datetime.date.today()
        now_hour = str(dt_now.hour)
        hour_zero = now_hour.zfill(2)
        today = str(d_today)

        #古いファイルの名前作成
        old_csv = "bandre-event-old-{day}-{hour}.csv"
        old_csv_form = old_csv.format(day=today, hour=hour_zero)

        #古いファイルを過去ファイルに移動
        old_copy_to = 'oldlist-csv/' + old_csv_form
        s3.Object(bucket_name, old_copy_to).copy_from(CopySource={'Bucket': bucket_name, 'Key': s3_filename_old})
        s3.Object(bucket_name, s3_filename_old).delete()

        #最新ファイルを1つ前の古いファイルに移動
        s3.Object(bucket_name, s3_filename_old).copy_from(CopySource={'Bucket': bucket_name, 'Key': s3_filename_new})
        s3.Object(bucket_name, s3_filename_new).delete()

    #更新がなければ自動ツイートとcsvリネームは省略する(スクレイピングで作成したファイルは削除する)
    else:
        s3.Object(bucket_name, s3_filename_new).delete()


