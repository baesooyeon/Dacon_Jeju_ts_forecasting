import datetime
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
import holidays
from sklearn.preprocessing import LabelEncoder

def pre_all(train, test):
    print(f"전처리 전 train 크기 : {train.shape}")
    print(f"전처리 전 test 크기 : {test.shape}")
    print("=================전처리 중=================")

    # 합쳐서 전처리하기
    train["timestamp"] = pd.to_datetime(train["timestamp"])
    test["timestamp"] = pd.to_datetime(test["timestamp"])
    df = pd.concat([train,test]).reset_index(drop = True)

    df.rename(columns={'supply(kg)':'supply', 'price(원/kg)':'price'},inplace=True)

    #년/월/일 추가
    df['year']=df['timestamp'].dt.year
    df['month']=df['timestamp'].dt.month
    df['day']=df['timestamp'].dt.day

    #요일 추가
    df['week_day']=df['timestamp'].dt.weekday

    # 년-월 변수 추가 : year-month의 형태
    le = LabelEncoder()
    df["year_month"] = df["timestamp"].map(lambda x :str(x.year) + "-"+str(x.month))

    # 라벨 인코딩
    df["year_month"] = le.fit_transform(df["year_month"])

    # 주차 변수 추가
    df["week"] = df["timestamp"].map(lambda x: datetime.datetime(x.year, x.month, x.day).isocalendar()[1])

    # 주차 누적값
    week_list=[]
    for i in range(len(df['year'])) :
        if df['year'][i] == 2019 :
            week_list.append(int(df['week'][i]))
        elif df['year'][i] == 2020 :
            week_list.append(int(df['week'][i])+52)
        elif df['year'][i] == 2021 :
            week_list.append(int(df['week'][i])+52+53)
        elif df['year'][i] == 2022 :
            week_list.append(int(df['week'][i])+52+53+53)
        elif df['year'][i] == 2023 :
            week_list.append(int(df['week'][i])+52+53+53+52)
    df['week_num']= week_list

    #수동으로 값 바꾸기
    df.loc[df['timestamp']=='2019-12-30','week_num']=52
    df.loc[df['timestamp']=='2019-12-31','week_num']=52


    # 계절 추가
    def make_season(x):
        if x in [12,1,2]:
            return 0
        elif x in [3,4,5]:
            return 1
        elif x in [6,7,8]:
            return 2
        elif x in [9,10,11]:
            return 3
        
    df["season"] =df["month"].map(lambda  x:make_season(x))

    # 공휴일 변수 추가
    def make_holi(x):
        kr_holi = holidays.KR()

        if x in kr_holi:
            return 1
        else:
            return 0
        
    df["holiday"] = df["timestamp"].map(lambda x : make_holi(x))
    
    # # 더미 변수 처리
    # df = pd.get_dummies(df, columns = ["corporation", "location"], drop_first=True)

    # train, test 분리하기
    train = df[~df["price"].isnull()].sort_values("timestamp").reset_index(drop = True)
    test = df[df["price"].isnull()].sort_values("timestamp").reset_index(drop=True)

    # # # train, test 분리하기
    # train = df[df["timestamp"]<"2023-03-04"]
    # test = df[df["timestamp"]>="2023-03-04"]

    print(f"전처리 후 train 크기 : {train.shape}")
    print(f"전처리 후 test 크기 : {test.shape}")

    return train, test