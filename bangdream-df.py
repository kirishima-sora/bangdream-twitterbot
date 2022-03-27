
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

#新情報以外の差分の確認
df_comp = df_new_comv.compare(df_old_comv)
print(df_comp)

diff_col = df_comp.columns.droplevel(1).unique()
print(diff_col)




""" 
df_comp = df_old.compare(df_new)
print(df_comp)
print(df_new.iat[0,2])
"""

""" 
df1 = pd.DataFrame(
    dict(
        a=[2, 4, 6],
        b=[1, 2, 3],
        c=[3, 6, 9],
    )
)
df2 = pd.DataFrame(
    dict(
        a=[2, 40, 6],
        b=[10, 2, 3],
        c=[3, 6, 9],
    )
)

df_comp = df1.compare(df2)
print(df_comp)

 """
