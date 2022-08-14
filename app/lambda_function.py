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
    #スクレイピング
    url_sc = "https://bang-dream.com/events"
    response = requests.get(url_sc)
    soup = BeautifulSoup(response.text, "html.parser")
    elems = soup.find_all('ul', attrs={"class": "liveEventList"})
    #イベントごとにliで区切られているため、li箇所の抜き出し
    events = elems[0].find_all("li")

    #イベント一覧リストの定義
    event_list = []
    event_list.append(["タイトル", "URL", "日付", "場所", "概要", "カテゴリ"])

    #イベント一覧リストの作成
    for event_unit in enumerate(events):
        title = event_unit[1].find('p', attrs={"class": "liveEventListTitle"}).text
        short_url = event_unit[1].find('a').get("href")
        long_url = urllib.parse.urljoin(url_sc, short_url)
        columns = event_unit[1].find_all('div', attrs={"class": "itemInfoColumnTitle"})
        #情報分類の抽出（開催日時・場所・概要）
        event_data = event_unit[1].find_all('div', attrs={"class": "itemInfoColumnData"})
        date = place = overview = update_category = "None"
        #情報分類を元にライブ情報の抽出
        for i, column in enumerate(columns):
            if column.get_text() == "開催日時":
                date = event_data[i].get_text()
            elif column.get_text() == "場所":
                place = event_data[i].get_text()
            elif column.get_text() == "概要":
                overview = event_data[i].get_text()
        event_list.append([title, long_url, date, place, overview, update_category])

    #S3バケット処理の準備
    s3 = boto3.resource('s3')
    bucket_name = "bangdream-eventlist"
    s3_filename_old = "bandre-event-old.csv"

    #S3バケット内の最新のCSVを読み込み
    df_old_object = s3.Object(bucket_name, s3_filename_old)
    body_in = df_old_object.get()['Body'].read().decode("cp932")
    buffer_in = io.StringIO(body_in)
    df_old = pd.read_csv(buffer_in, lineterminator='\n')

    #スクレイピングした情報のデータフレーム化
    df_new = pd.DataFrame(event_list[1:], columns=event_list[0])

    #新情報を抜き出すためのリストの定義
    df_old_comv = df_old.copy()
    df_new_comv = df_new.copy()
    #比較結果リストの作成（True,False判定）
    df_comp = (df_old_comv==df_new_comv)

    #新情報の番号抽出・新情報の抜出後の比較リスト作成（True,False判定）
    #新情報が何番目の行かをリスト化
    new_line_num_list = []
    new_quantity = 0
    for row in range(10):
        row = row - len(new_line_num_list)
        #タイトル・URL・日付が全て異なっている場合は新情報とみなす
        if ((~(df_comp.iat[row, 0])) and (~(df_comp.iat[row, 1])) and (~(df_comp.iat[row, 2]))):
            #新情報の行番号をリストに保存
            new_line_num_list.append(row + len(new_line_num_list))
            df_new_comv = df_new_comv.drop(df_new_comv.index[row])
            df_old_comv = df_old_comv.drop(df_old_comv.index[-1])
            df_new_comv = df_new_comv.reset_index(drop=True)
            df_old_comv = df_old_comv.reset_index(drop=True)
            df_comp = (df_old_comv == df_new_comv)
            new_quantity += 1

    #更新カテゴリ入れ
    for row in range(10 - new_quantity):
        update_category = "None"
        if ~(df_comp.iat[row, 2]):
            update_category = "ライブ日程決定"
        elif ~(df_comp.iat[row, 3]):
            update_category = "ライブ開催場所決定"
        elif ~(df_comp.iat[row, 0]):
            update_category = "ライブタイトル決定"
        elif (~(df_comp.iat[row, 0])) or (~(df_comp.iat[row, 2])) or (~(df_comp.iat[row, 3])) or (~(df_comp.iat[row, 4])):
            update_category = "ライブ情報更新"
        df_comp.iat[row, 5] = update_category

    #ツイート内容を入れる配列を作成
    tweet_array = []

    #新情報のツイート内容作成
    for row in new_line_num_list:
        text = "【新情報】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
        tweet_array.append(text.format(title=df_new.iat[row,0], date=df_new.iat[row,2], place=df_new.iat[row,3], URL=df_new.iat[row,1]))
    #情報更新のツイート内容作成
    for row in range(10 - new_quantity):
        if df_comp.iat[row,5] != "None":
            text = "【{update_category}】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
            tweet_array.append(text.format(update_category=df_comp.iat[row,5], title=df_new_comv.iat[row,0], date=df_new_comv.iat[row,2], place=df_new_comv.iat[row,3], URL=df_new_comv.iat[row,1]))


    #更新があれば自動ツイートとcsvリネーム処理を実行
    if (new_quantity != 0) or (~(df_old_comv.equals(df_new_comv))):
        twitter_consumer_key = os.environ['CONSUMER_KEY']
        twitter_consumer_secret = os.environ['CONSUMER_KEY_SECRET']
        twitter_access_token = os.environ['ACCESS_TOKEN_KEY']
        twitter_access_token_secret = os.environ['ACCESS_TOKEN_KEY_SECRET']

        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        api = tweepy.API(auth)

        #更新情報のツイート
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

        #実行前の最新ファイルを過去フォルダへ移動
        old_csv = "bandre-event-old-{day}-{hour}.csv"
        old_csv_form = old_csv.format(day=today, hour=hour_zero)
        old_copy_to = 'oldlist-csv/' + old_csv_form
        s3.Object(bucket_name, old_copy_to).copy_from(CopySource={'Bucket': bucket_name, 'Key': s3_filename_old})
        s3.Object(bucket_name, s3_filename_old).delete()

        #実行後の最新ファイルを次回比較のためにS3にアップロード
        #一時利用ファイルパス
        tmp_path = "/tmp/data.csv"
        #CSV書き込み
        with open(tmp_path, "w", encoding="cp932") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerows(event_list)
        bucket = s3.Bucket(bucket_name)
        bucket.upload_file(tmp_path, s3_filename_old)
        #tmpファイルの削除
        os.remove(tmp_path)


