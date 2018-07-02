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
        {'..': np.nan}).drop('Series code', 1)  # 選擇co2data，並將表中的".."替換成NaN，刪除"Series code" col
    df_data = df_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)  # 填NaN數據
    df_data.dropna(how='all', inplace=True)
    df_data['total'] = df_data.values[:, 1:].sum(1)  # 以國為單位將排放加總
    #df_data = df_data[pd.notnull(df_data['total'])]  # 去除掉 total 為NaN 的國家
    for index, col in df_data.iterrows():
        df_data.loc[index, 'Income group'] = dict_country[index]  # 為每個國家加上 "Income group" value
    income_group = df_data.groupby('Income group')  # 用Income group 為每個國家排序
    df_sum = income_group.sum()['total'].rename('Sum emissions')
    df_high = pd.concat([income_group.idxmax()['total'].rename('Highest emission country'),
                         income_group.max()['total'].rename('Highest emissions')], axis=1)
    df_low = pd.concat([income_group.idxmin()['total'].rename('Lowest emission country'),
                        income_group.min()['total'].rename('Lowest emissions')], axis=1)
    results = pd.concat([df_sum, df_high, df_low], axis=1)
    return results


if __name__ == '__main__':
    co2()
