import pandas as pd
import numpy as np
import math

def drop_china_data():
    df = pd.read_csv('../DXY-COVID-19-Data/csv/DXYArea.csv')
    df = df[['continentEnglishName','countryName','countryEnglishName','provinceName','provinceEnglishName',
             'province_confirmedCount','province_suspectedCount','province_curedCount','province_deadCount',
             'cityName','cityEnglishName','city_confirmedCount','city_suspectedCount','city_curedCount','city_deadCount',
             'updateTime']]
    df_woc = df[df.countryName != '中国']
    df_china = df[df.countryName == '中国']
    df_with_china = df[df.countryName == df.provinceName]
    df_woc['updateTime'] = df_woc['updateTime'].apply(lambda x:x.split()[0])
    df_china['updateTime'] = df_china['updateTime'].apply(lambda x: x.split()[0])
    df_with_china['updateTime'] = df_with_china['updateTime'].apply(lambda x: x.split()[0])
    df_china.to_csv('csv/data_china.csv')
    df_woc.to_csv('csv/data_without_china.csv')
    df_with_china.to_csv('csv/data_with_china.csv')
    return df_woc, df_china, df_with_china

def data_each_day_without_china(df_woc,date_name):
    # date_name = np.array(list(df_woc['updateTime']))
    # date_name = np.unique(date_name)
    for name in date_name:
        df_woc[df_woc.updateTime == name].drop_duplicates(subset="countryName").drop(columns = ['updateTime']).to_csv('csv/date/'+name+'.csv')


def data_of_each_country(df_woc,date_name,china_confirmedCount , china_curedCount , china_deadCount):
    data_province_confirmedCount, data_province_deadCount , data_province_curedCount,data_province_confirmedCount_perMillion= [] ,[] ,[],[]
    country_name = np.array(list(df_woc['countryName']))
    country_name_ = df_woc[['countryName','countryEnglishName']].drop_duplicates()

    # for index , row in country_name_.iterrows():
    #     print(row['countryName'],row['countryEnglishName'])
    country_name = np.unique(country_name)

    tmp_name = np.insert(date_name,0,'Flag')
    tmp_name = np.insert(tmp_name, 0, 'Population')
    tmp_name = np.insert(tmp_name,0,'Name')
    tmp_name = np.insert(tmp_name, 0, 'English Name')

    # for name in country_name:
    dic_name,dic_flag = {},{}
    flag = pd.read_csv('csv/flag.csv')
    for index, row in flag.iterrows():
        flag_, country_name,countryEnglishName = row['Flag'], row['Name'],row['countryEnglishName']
        dic_name[country_name] = countryEnglishName
        dic_flag[country_name] = flag_

    dic_population = {}
    population = pd.read_csv('csv/population.csv')
    for index, row in population.iterrows():
        population_, country_name = row['Population'], row['Country']
        dic_population[country_name] = population_
    # print(dic_population)

    days = len(date_name)
    for index, row in country_name_.iterrows():
        name,English_name = row['countryName'],row['countryEnglishName']
        df_country = df_woc[df_woc.countryName == name].drop_duplicates(subset="updateTime")
        # print (df_country)
        df_country.to_csv('csv/country/'+name+'.csv')

        dic_province_confirmedCount , dic_province_deadCount, dic_province_curedCount =  dict.fromkeys(date_name,0),dict.fromkeys(date_name,0),dict.fromkeys(date_name,0)
        for index, row in df_country.iterrows():
            dic_province_confirmedCount[row['updateTime']] = row['province_confirmedCount']


        for index, row in df_country.iterrows():
            dic_province_deadCount[row['updateTime']] = row['province_deadCount']


        for index, row in df_country.iterrows():
            dic_province_curedCount[row['updateTime']] = row['province_curedCount']

        country_flag = None
        if name in dic_flag:
            country_flag = dic_flag[name]
        if type(English_name) != type('a'):
            if name in dic_name:
                English_name = dic_name[name]

        country_population = None
        if English_name in dic_population:
            country_population = int(dic_population[English_name].replace(',', ''))

        if country_population == None:
            millions = 1
        elif country_population < 1000000:
            millions = 1
        else:
            millions = country_population/1000000
        # print (millions)
        data_province_confirmedCount.append([English_name]+[name]+[country_population] +[country_flag]+ [dic_province_confirmedCount[key] for key in dic_province_confirmedCount])
        data_province_deadCount.append([English_name] + [name] +[country_population]+ [country_flag] + [dic_province_deadCount[key] for key in dic_province_deadCount])
        data_province_curedCount.append([English_name] + [name] +[country_population]+ [country_flag] + [dic_province_curedCount[key] for key in dic_province_curedCount])
        data_province_confirmedCount_perMillion.append([English_name]+[name]+[country_population] +[country_flag]+ [(dic_province_confirmedCount[key]/millions) for key in dic_province_confirmedCount])


    data_province_confirmedCount.append(['China'] + ['中国'] + [1439323776]+['https://www.countryflags.io/cn/flat/64.png'] +list(china_confirmedCount[len(china_confirmedCount)-days:]))
    data_province_deadCount.append(['China'] + ['中国'] + [1439323776]+['https://www.countryflags.io/cn/flat/64.png'] +list(china_deadCount[len(china_deadCount)-days:]))
    data_province_curedCount.append(['China'] + ['中国'] + [1439323776]+['https://www.countryflags.io/cn/flat/64.png'] +list(china_curedCount[len(china_curedCount)-days:]))
    data_province_confirmedCount_perMillion.append(['China'] + ['中国'] + [1439323776]+['https://www.countryflags.io/cn/flat/64.png'] +list(china_confirmedCount[len(china_confirmedCount)-days:]/1439323776*1000000))

    df_total_confirmed_case = pd.DataFrame(data_province_confirmedCount,columns= tmp_name)
    df_total_confirmed_case.to_csv('csv/total_confirmed_case.csv')

    df_total_deadCount = pd.DataFrame(data_province_deadCount, columns=tmp_name)
    df_total_deadCount.to_csv('csv/total_deadCount.csv')

    df_total_cured = pd.DataFrame(data_province_curedCount, columns=tmp_name)
    df_total_cured.to_csv('csv/total_curedCount.csv')

    df_total_confirmed_perMillion = pd.DataFrame(data_province_confirmedCount_perMillion, columns=tmp_name)
    df_total_confirmed_perMillion.to_csv('csv/total_confirmed_case_perMillion.csv')


def data_each_day_china(df_china,date_name):
    for name in date_name:
        df_china[df_china.updateTime == name].drop_duplicates(subset="provinceName").drop(columns = ['cityName','cityEnglishName','city_confirmedCount','city_suspectedCount','city_curedCount','city_deadCount',
             'updateTime']).to_csv('csv/data_china/'+name+'.csv')

def data_china(date_name):
    df = pd.read_csv('csv/china.csv')
    total_confirmedCount = list(df['total_confirmedCount'])
    total_confirmedCount.reverse()

    total_curedCount = list(df['total_curedCount'])
    total_curedCount.reverse()

    total_deadCount = list(df['deadCount'])
    total_deadCount.reverse()

    return np.asarray(total_confirmedCount),np.asarray(total_curedCount),np.asarray(total_deadCount)


if __name__ == "__main__":
    df_woc, df_china ,df_with_china= drop_china_data()

    date_name = np.array(list(df_woc['updateTime']))
    date_name = np.unique(date_name)

    data_each_day_without_china(df_woc,date_name)
    data_each_day_without_china(df_with_china,date_name)
    data_each_day_china(df_china, date_name)
    china_confirmedCount , china_curedCount , china_deadCount= data_china(date_name)
    data_of_each_country(df_woc,date_name,china_confirmedCount , china_curedCount , china_deadCount)


