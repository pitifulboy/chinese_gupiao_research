# 查询龙虎榜最近20个交易日龙虎榜的透视表
# 筛选透视表：筛选出活跃席位，频次>交易日数，且小于5倍交易日数，筛选出盈利能力强的席位，最大涨幅>平均涨幅。根据席位查询个股。
# 周期选7天，5个交易日。

from LHB_make_money_research import lhb_analysis, lhb_povit_df
from get_trade_date import get_trade_datelist, get_tradedate_by_enddate_tradedates
from my_time_func import get_today_date

# TODO: 代码优化
from update_longhubang import update_longhubang_auto

update_longhubang_auto()

# 龙虎榜更新较晚，且需要计算次日收益，因此截至日期应往前2个交易日。
today_date = get_today_date()
enddate = get_tradedate_by_enddate_tradedates(today_date, 1)

startdate = get_tradedate_by_enddate_tradedates(enddate, 6)
print(startdate)

'''start_date = '20230101'
# 本次分析龙虎榜后一个交易日收益情况，获取指定日期后一个交易日
end_date = '20230107
'''

my_datelist = get_trade_datelist(startdate, enddate)
# 交易日数量
num = len(my_datelist)
# 龙虎榜数据
df = lhb_analysis(my_datelist)
# 龙虎榜透视
df_povit = lhb_povit_df(my_datelist, df)

# 筛选营业部，根据筛选后的营业部，匹配参与的个股。
df2 = df_povit.loc[
    (df_povit['exalter'] > num) & (df_povit['exalter'] < 5 * num) & (df_povit["次日最大涨幅"] > df_povit["次日最大涨幅"].mean())]
print(df2)
# 导出筛选后的席位——盈利 信息。
path2 = r'D:\00 量化交易\\' + my_datelist[0] + '-' + my_datelist[-1] + '盈利强席位' + '.xlsx'
df2.to_excel(path2, sheet_name='协同明细', engine='openpyxl')

# 获取盈利能力强的席位
exalter_list = df2.index.tolist()
print(exalter_list)
exalter_df = df[df['exalter'].isin(exalter_list)]
print(exalter_df)

path3 = r'D:\00 量化交易\\' + my_datelist[0] + '-' + my_datelist[-1] + '盈利强席位参与明细' + '.xlsx'
exalter_df.to_excel(path3, sheet_name='协同明细', engine='openpyxl')
