# 获取后一天
import pandas as pd
from datetime import datetime, timedelta


# 获取n天后日期，tushare格式
def get_days_after_tushare(datestr, n):
    date_datetime = pd.to_datetime(datestr, format='%Y%m%d')
    date_dayafter = date_datetime + timedelta(n)
    date_dayafter_formate = date_dayafter.strftime('%Y%m%d')

    return date_dayafter_formate


# 获取今天的日期
def get_today_date():
    # 今天
    today_1 = pd.Timestamp.now()
    today_tushare_format = today_1.strftime('%Y%m%d')
    date_str = today_tushare_format

    return date_str


# 指定其实结束日期，生成日期list
def get_my_start_end_date_list(startdate, enddate):
    t = pd.period_range(start=startdate, end=enddate)
    new_list = []
    for i in range(0, len(t)):
        new_list.append(t[i].strftime('%Y%m%d'))

    return new_list
