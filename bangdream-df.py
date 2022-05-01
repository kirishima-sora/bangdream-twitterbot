
from cgi import print_arguments
import csv
import pandas as pd


def tweet_create():
    #csv読み込み
    df_old = pd.read_csv("bandre-event-old.csv", encoding="Shift_JIS")
    df_new = pd.read_csv("bandre-event.csv", encoding="Shift_JIS")

    #新情報の行数(shift_num)の確認
    for shift_num in range(10):
        if df_old.iat[0,0] == df_new.iat[shift_num,0]:
            break

    #新情報の行数だけずらすリストの定義
    df_old_comv = df_old.copy()
    df_new_comv = df_new.copy()
    df_new_comv_fake = df_new_comv

    #新情報の行数だけずらす処理
    for drop_num in range(shift_num):
        df_old_comv = df_old_comv.drop(df_old_comv.index[9-drop_num])
        df_new_comv = df_new_comv.drop(df_new_comv.index[0])

    #ずれたインデックスの振り直し
    df_old_comv = df_old_comv.reset_index(drop=True)
    df_new_comv = df_new_comv.reset_index(drop=True)

    #比較結果リストの作成（true,false判定）
    df_comp = (df_old_comv==df_new_comv)
    print(df_comp)
    
    #中間の新情報の番号抜き出しと比較リストの修正
    mid_new_num = []
    mid_shift_num = 0
    for row in range(10 - shift_num):
        row = row - len(mid_new_num)
        if ((df_comp.iat[row,0]==False) and (df_comp.iat[row,1]==False) and (df_comp.iat[row,2]==False)):
            mid_new_num.append(row + len(mid_new_num))
            df_new_comv = df_new_comv.drop(df_new_comv.index[row])
            df_old_comv = df_old_comv.drop(df_old_comv.index[-1])
            df_new_comv = df_new_comv.reset_index(drop=True)
            df_old_comv = df_old_comv.reset_index(drop=True)
            df_comp = (df_old_comv == df_new_comv)
            mid_shift_num += 1

    #更新カテゴリ入れ
    for row in range(10 - shift_num - mid_shift_num):
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

    #頭の新情報のツイート内容作成
    for row in range(shift_num):
        text = "【新情報】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
        tweet_array.append(text.format(title=df_new.iat[row,0], date=df_new.iat[row,2], place=df_new.iat[row,3], URL=df_new.iat[row,1]))
    
    #中間の新情報のツイート内容作成
    for row in mid_new_num:
        text = "【新情報】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
        tweet_array.append(text.format(title=df_new_comv_fake.iat[row,0], date=df_new_comv_fake.iat[row,2], place=df_new_comv_fake.iat[row,3], URL=df_new_comv_fake.iat[row,1]))

    #情報更新のツイート内容作成
    for row in range(10 - shift_num - mid_shift_num):
        if df_comp.iat[row,5] != "None":
            text = "【{info}】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
            tweet_array.append(text.format(info=df_comp.iat[row,5], title=df_new_comv.iat[row,0], date=df_new_comv.iat[row,2], place=df_new_comv.iat[row,3], URL=df_new_comv.iat[row,1]))

    #(テスト用)ツイート内容の確認
    for tweet in enumerate(tweet_array):
        print(tweet[1])


tweet_create()


