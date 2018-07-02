#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import numpy as np


def co2():
    # 讀取世界銀行氣候變化數據集
    file_loc = "ClimateChange.xlsx"
    df_country = pd.read_excel(file_loc, sheetname='Country', index_col=0, na_values=['NA'], parse_cols="B,E")
    dict_country = df_country.to_dict()['Income group']  # create dict{country name: Income group}
    df_data = pd.read_excel(file_loc, sheetname='Data', index_col=0, na_values=['NA'], parse_cols="B,C,G:AB")
    df_data = df_data.loc[df_data['Series code'] == 'EN.ATM.CO2E.KT'].replace(
        {'..': np.nan}).drop('Series code', 1)           # 選擇co2data，並將表中的".."替換成NaN，刪除"Series code" col
    df_data = df_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)  # 填NaN數據
    df_data['total'] = df_data.values[:, 1:].sum(1)      # 以國為單位將排放加總
    df_data = df_data[pd.notnull(df_data['total'])]      # 去除掉 total 為NaN 的國家
    for index, col in df_data.iterrows():
        df_data.loc[index, 'Income group'] = dict_country[index]  # 為每個國家加上 "Income group" value
    income_group = df_data.groupby('Income group')       # 用Income group 為每個國家排序
    df_sum = income_group.sum()['total'].rename('Sum emissions')
    df_high = pd.concat([income_group.idxmax()['total'].rename('Highest emission country'),
                         income_group.max()['total'].rename('Highest emissions')], axis=1)
    df_low = pd.concat([income_group.idxmin()['total'].rename('Lowest emission country'),
                        income_group.min()['total'].rename('Lowest emissions')], axis=1)
    results = pd.concat([df_sum, df_high, df_low], axis=1)
    return results


'''目標
挑戰內容是通過對氣候變化數據集中的 3 個數據表關聯分析，得到 各收入群體（Income group ）二氧化碳 CO2 的排放（Series code: EN.ATM.CO2E.KT）總量，以及各群體排放量最高和最低的國家名稱及相應的排放量。

結果示意圖
挑戰的最後，需要得到如下圖所示的 Dataframe，並將該 Dataframe 作為函數的返回值

其中：

索引列為 5 個收入群體分類名稱。
Sum emissions 表示相應收入群體（Income group）的總排放量
Highest emission country 為相應收入群體裡排放量最高的國家名稱（Country name）。
Highest emissions 為排放量最高的國家對應的排放量數值。
Lowest emission country 為相應收入群體裡排放量最低的國家名稱。
Lowest emissions 為排放量最低的國家對應的排放量數值。
注意：DataFrame 中，請務必使用上述約定的英文名稱作為列名和索引名稱，否則會影響到系統評判結果。'''
