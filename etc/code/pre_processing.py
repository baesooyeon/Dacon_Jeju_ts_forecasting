# 주차 계산
from datetime import datetime
def pre_process(train) :
    train.rename(columns={'supply(kg)':'supply', 'price(원/kg)':'price'},inplace=True)
    week_num =[]
    for i in range(len(train['timestamp'])) :
        week=datetime.strptime(train['timestamp'][i], "%Y-%m-%d").isocalendar()[1]
        week_num.append(week)

    #파생변수 생성
    train['year']=train['timestamp'].str.split('-').str[0]
    train['month']=train['timestamp'].str.split('-').str[1]
    train['week']=week_num
    train['day']=train['timestamp'].str.split('-').str[2]
    train['year']=train['year'].astype('int64')

    train['year'].dtype

    week_list=[]
    for i in range(len(train['year'])) :
        if train['year'][i] == 2019 :
            week_list.append(int(train['week'][i]))
        elif train['year'][i] == 2020 :
            week_list.append(int(train['week'][i])+52)
        elif train['year'][i] == 2021 :
            week_list.append(int(train['week'][i])+52+53)
        elif train['year'][i] == 2022 :
            week_list.append(int(train['week'][i])+52+53+53)
        elif train['year'][i] == 2023 :
            week_list.append(int(train['week'][i])+52+53+53+52)


    train['week_num']= week_list

    #수동으로 값 바꾸기
    train.loc[train['timestamp']=='2019-12-30','week_num']=52
    train.loc[train['timestamp']=='2019-12-31','week_num']=52

    year_month=[]
    for i in range(len(train)) :
        year_month.append(train['timestamp'][i][:7])

    train['year_month']=year_month  

    season_list=[]
    for i in range(len(train)) :
        if train['month'][i] in ['03','04','05'] :
            season  = '봄'
        elif train['month'][i] in ['06','07','08'] :
            season  = '여름'
        elif train['month'][i] in ['09','10','11'] :
            season  = '가을'
        elif train['month'][i] in ['01','02','12'] :
            season  = '가을'
        season_list.append(season)
        
        
    train['season'] = season_list

    train=train.sort_values(by='timestamp',ignore_index=True)
    train['timestamp']=pd.to_datetime(train['timestamp'])
    train['day']=train['day'].astype('int64')
    train['month']=train['month'].astype('int64')

    return train
    
        