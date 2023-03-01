# 涨停个股中市值低于100的。
from add_share_shizhi import add_shizhi_info_by_df
from select_sql_tradedata import select_share_by_date

day_or_days = '20230210'
today_trade_df_origin = select_share_by_date(day_or_days)
df_zt = add_shizhi_info_by_df(today_trade_df_origin, '涨停')

# 涨停个股，市值低于100亿的个股

df_zt_below_100yi = df_zt.loc[df_zt['总值（亿）'] < 100]

print(df_zt_below_100yi)
