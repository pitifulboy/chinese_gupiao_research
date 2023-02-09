# 每日涨停，匹配流通股本，总股本，行业数据。
# 每日涨幅top200，匹配流通股本，总股本，行业数据。
from my_time_func import get_today_date
from select_sql_tradedata import select_share_by_date


querydate = get_today_date()
today_trade_df_origin = select_share_by_date(querydate)
print(today_trade_df_origin)

