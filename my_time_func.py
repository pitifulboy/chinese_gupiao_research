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
def get_today_date(type_str):
    # 今天
    today_1 = pd.Timestamp.now()

    today_tushare_format = today_1.strftime('%Y%m%d')
    today_tushare_baostock = today_1.strftime('%Y-%m-%d')

    if type_str == 'tushare':
        date_str = today_tushare_format
    elif type_str == 'baostock':
        date_str = today_tushare_baostock

    return date_str
