
import csv
import pandas as pd

#csv読み込み
df_old = pd.read_csv("bangdream-sc-old.csv", encoding="Shift_JIS")
df_new = pd.read_csv("bangdream-sc.csv", encoding="Shift_JIS")

#新情報がどこまでかを確認
for shift_num in range(10):
    if df_old.iat[0,0] == df_new.iat[shift_num,0]:
        break

#新情報分だけずらすリストの定義
df_old_comv = df_old.copy()
df_new_comv = df_new.copy()

#新情報分だけずらす処理
for drop_num in range(shift_num):
    df_old_comv = df_old_comv.drop(df_old_comv.index[9-drop_num])
    df_new_comv = df_new_comv.drop(df_new_comv.index[0])

#ずれたインデックスの振り直し
df_old_comv = df_old_comv.reset_index(drop=True)
df_new_comv = df_new_comv.reset_index(drop=True)

#比較結果リストの作成（true,false埋め）
df_comp = (df_old_comv==df_new_comv)
print(df_comp)

#更新カテゴリ入れ
for row in range(10-shift_num):
    category = "更新なし"
    if ((df_comp.iat[row, 2] == False) and (df_comp.iat[row, 3] == False)) or (df_comp.iat[row, 0] == False) or (df_comp.iat[row, 4] == False):
        category = "情報更新"
    elif df_comp.iat[row, 2] == False:
        category = "日程情報更新"
    elif df_comp.iat[row, 3] == False:
        category = "場所情報更新"
    df_comp.iat[row, 5] = category
print(df_comp)

#ツイート内容の配列を作成
tweet_array = []

#新情報のツイート内容作成
for row in range(shift_num):
    text = "【新情報】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
    tweet_array.append(text.format(title=df_new.iat[row,0], date=df_new.iat[row,2], place=df_new.iat[row,3], URL=df_new.iat[row,1]))

#情報更新のツイート内容作成
for row in range(10-shift_num):
    if df_comp.iat[row,5] != "更新なし":
        text = "【{category}】\n{title}\n開催日時:{date}\n場所:{place}\n{URL}"
        tweet_array.append(text.format(category=df_comp.iat[row,5], title=df_new_comv.iat[row,0], date=df_new_comv.iat[row,2], place=df_new_comv.iat[row,3], URL=df_new_comv.iat[row,1]))

for tweet in enumerate(tweet_array):
    print(tweet[1])



