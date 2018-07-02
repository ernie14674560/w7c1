#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import numpy as np


def co2():
    # 讀取世界銀行氣候變化數據集
    file_loc = "ClimateChange.xlsx"
    df_country = pd.read_excel(file_loc, sheetname='Country', index_col=0, na_values=['NA'], parse_cols="B,E")
    dict_country = df_country.to_dict()['Income group']
    df_data = pd.read_excel(file_loc, sheetname='Data', index_col=0, na_values=['NA'], parse_cols="B,C,G:AB")
    df_data = df_data.loc[df_data['Series code'] == 'EN.ATM.CO2E.KT'].replace(
        {'..': np.nan})  # 選擇co2data，並將表中的".."替換成NaN
    df_data = df_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)  # 填NaN數據

    '''
    補充代碼：
    1. 查看數據文件結構。
    2. 將國家和所在的收入群體類別產生關聯。
    3. 處理 DataFrame 中的不必要數據和缺失數據。
    3. 尤其是注意這裡的缺失值並不是 NaN 的形式。
    4. 將最終返回的 DataFrame 處理成挑戰要求的格式 。
    '''

    # 必須返回最終得到的 DataFrame
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
