import pandas as pd
import numpy as np


def drop_china_data():
    df = pd.read_csv('csv/DXYArea.csv')
    df = df[['continentEnglishName','countryName','countryEnglishName','province_confirmedCount','province_suspectedCount','province_curedCount','province_deadCount','updateTime']]
    df_woc = df[df.countryName != '中国']
    df_woc['updateTime'] = df_woc['updateTime'].apply(lambda x:x.split()[0])
    df_woc.to_csv('csv/data_without_china.csv')
    return df_woc

def data_each_day(df_woc):
    date_name = np.array(list(df_woc['updateTime']))
    date_name = np.unique(date_name)
    for name in date_name:
        df_woc[df_woc.updateTime == name].drop_duplicates(subset="countryName").drop(columns = ['updateTime']).to_csv('csv/date/'+name+'.csv')


def data_of_each_country(df_woc,date_name):
    data = []
    country_name = np.array(list(df_woc['countryName']))
    country_name = np.unique(country_name)
    tmp_name = np.insert(date_name,0,'Flag')
    tmp_name = np.insert(tmp_name,0,'Name')
    tmp_name = np.insert(tmp_name,0,'Country')

    for name in country_name:
        df_country = df_woc[df_woc.countryName == name].drop_duplicates(subset="updateTime")
        df_country.to_csv('csv/country/'+name+'.csv')

        dic_ =  dict.fromkeys(date_name,0)
        for index, row in df_country.iterrows():
            dic_[row['updateTime']] = row['province_confirmedCount']
        # print(dic_)
        country = df_country.loc[0,2]
        l = [name]+[]+[None] + [dic_[key] for key in dic_]
        data.append(l)
    df_country_data = pd.DataFrame(data,columns= tmp_name)

    df_country_data.to_csv('csv/test.csv')