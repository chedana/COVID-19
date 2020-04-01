import pandas as pd
import numpy as np


def drop_china_data():
    df = pd.read_csv('../DXY-COVID-19-Data/csv/DXYArea.csv')
    df = df[['continentEnglishName','countryName','countryEnglishName','provinceName','provinceEnglishName',
             'province_confirmedCount','province_suspectedCount','province_curedCount','province_deadCount',
             'cityName','cityEnglishName','city_confirmedCount','city_suspectedCount','city_curedCount','city_deadCount',
             'updateTime']]
    df_woc = df[df.countryName != '中国']
    df_china = df[df.countryName == '中国']
    df_woc['updateTime'] = df_woc['updateTime'].apply(lambda x:x.split()[0])
    df_china['updateTime'] = df_china['updateTime'].apply(lambda x: x.split()[0])
    df_china.to_csv('csv/data_china.csv')
    df_woc.to_csv('csv/data_without_china.csv')
    return df_woc, df_china

def data_each_day_without_china(df_woc,date_name):
    # date_name = np.array(list(df_woc['updateTime']))
    # date_name = np.unique(date_name)
    for name in date_name:
        df_woc[df_woc.updateTime == name].drop_duplicates(subset="countryName").drop(columns = ['updateTime']).to_csv('csv/date/'+name+'.csv')


def data_of_each_country(df_woc,date_name):
    data = []
    country_name = np.array(list(df_woc['countryName']))
    country_name_ = df_woc[['countryName','countryEnglishName']].drop_duplicates()

    # for index , row in country_name_.iterrows():
    #     print(row['countryName'],row['countryEnglishName'])
    country_name = np.unique(country_name)
    tmp_name = np.insert(date_name,0,'Flag')
    tmp_name = np.insert(tmp_name,0,'Name')
    tmp_name = np.insert(tmp_name, 0, 'English Name')

    # for name in country_name:
    for index, row in country_name_.iterrows():
        name,English_name = row['countryName'],row['countryEnglishName']
        df_country = df_woc[df_woc.countryName == name].drop_duplicates(subset="updateTime")
        # print (df_country)
        df_country.to_csv('csv/country/'+name+'.csv')

        dic_ =  dict.fromkeys(date_name,0)
        for index, row in df_country.iterrows():
            dic_[row['updateTime']] = row['province_confirmedCount']
        # print(dic_)

        flag = pd.read_csv('csv/flag.csv')
        country_flag = None
        for index, row in flag.iterrows():
            flag, country_name = row['Flag'],row['Name']
            if name == country_name :
                country_flag = flag
        l = [English_name]+[name] +[country_flag]+ [dic_[key] for key in dic_]
        data.append(l)

    df_country_data = pd.DataFrame(data,columns= tmp_name)
    df_country_data.to_csv('csv/test.csv')

def data_each_day_china(df_china,date_name):
    for name in date_name:
        df_china[df_china.updateTime == name].drop_duplicates(subset="provinceName").drop(columns = ['cityName','cityEnglishName','city_confirmedCount','city_suspectedCount','city_curedCount','city_deadCount',
             'updateTime']).to_csv('csv/date_china/'+name+'.csv')

if __name__ == "__main__":
    df_woc, df_china = drop_china_data()

    date_name = np.array(list(df_woc['updateTime']))
    date_name = np.unique(date_name)

    data_each_day_without_china(df_woc,date_name)
    data_each_day_china(df_china, date_name)
    data_of_each_country(df_woc,date_name)