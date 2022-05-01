
from cgi import print_arguments
from cmath import inf
import csv
import pandas as pd


def tweet_create():
    #csv読み込み
    df_old = pd.read_csv("bandre-event-old.csv", encoding="Shift_JIS")
    df_new = pd.read_csv("bandre-event.csv", encoding="Shift_JIS")

    #新情報を抜き出すリストの定義
    df_old_comv = df_old.copy()
    df_new_comv = df_new.copy()

    #最初の比較結果リストの作成（true,false判定）
    df_comp = (df_old_comv==df_new_comv)

    #新情報の番号抽出・新情報の抜出後の比較リスト作成（true,false判定）
    new_num_list = []
    shift_num = 0
    for row in range(10):
        row = row - len(new_num_list)
        if ((df_comp.iat[row,0]==False) and (df_comp.iat[row,1]==False) and (df_comp.iat[row,2]==False)):
            new_num_list.append(row + len(new_num_list))
            df_new_comv = df_new_comv.drop(df_new_comv.index[row])
            df_old_comv = df_old_comv.drop(df_old_comv.index[-1])
            df_new_comv = df_new_comv.reset_index(drop=True)
            df_old_comv = df_old_comv.reset_index(drop=True)
            df_comp = (df_old_comv == df_new_comv)
            shift_num += 1

    #更新カテゴリ入れ
    for row in range(10 - shift_num):
        info = "None"
        if df_comp.iat[row, 2] == False:
            info = "ライブ日程決定"
        elif df_comp.iat[row, 3] == False:
            info = "ライブ開催場所決定"
        elif df_comp.iat[row, 0] == False:
            info = "ライブタイトル決定"
        elif (df_comp.iat[row, 0] == False) or (df_comp.iat[row, 2] == False) or (df_comp.iat[row, 3] == False) or (df_comp.iat[row, 4] == False):
            info = "ライブ情報更新"
        df_comp.iat[row, 5] = info

    #ツイート内容を入れる配列を作成
    tweet_array = []

    #新情報のツイート内容作成
    for row in new_num_list:
        text = "【新情報】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
        tweet_array.append(text.format(title=df_new.iat[row,0], date=df_new.iat[row,2], place=df_new.iat[row,3], URL=df_new.iat[row,1]))
    #情報更新のツイート内容作成
    for row in range(10 - shift_num):
        if df_comp.iat[row,5] != "None":
            text = "【{info}】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
            tweet_array.append(text.format(info=df_comp.iat[row,5], title=df_new_comv.iat[row,0], date=df_new_comv.iat[row,2], place=df_new_comv.iat[row,3], URL=df_new_comv.iat[row,1]))

    #(テスト用)ツイート内容の確認
    for tweet in enumerate(tweet_array):
        print(tweet[1])


tweet_create()


