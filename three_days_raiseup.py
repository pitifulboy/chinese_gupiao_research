# 获取数据库中，最近3个交易日数据，分析最近三日情况。
from get_trade_date import get_tradedate_by_enddate_tradedates
from my_time_func import get_my_start_end_date_list
from select_sql_tradedata import select_data_by_datelist
from selet_sql_maxdate import get_dailytrade_maxdate

# 更新交易数据
# update_trade_data()

maxdate = get_dailytrade_maxdate()
print(maxdate)
# n个交易日前的交易日
start_tradedate = get_tradedate_by_enddate_tradedates(maxdate, 2)
print(start_tradedate)

datelist = get_my_start_end_date_list(start_tradedate, maxdate)
df = select_data_by_datelist(datelist)
print(df)
