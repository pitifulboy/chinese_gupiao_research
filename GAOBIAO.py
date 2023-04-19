#  1-n日 涨幅计算top50
from add_share_msg import add_share_msg_to_df
from draw_table import draw_table_by_df
from get_trade_date import get_tradedate_by_enddate_tradedates
from my_time_func import get_today_date, get_my_start_end_date_list
import pandas as pd
from select_sql_tradedata import select_data_by_datelist


# 选定截至日期和交易日统计周期
# 计算周期内，按截止日收盘价算，个股的最大涨幅。
# 计算步骤：1，拉取周期内交易数据。2，
def caculate_ndays_zhangfu(enddate, n_days):
    # 倒推开始日期
    start_date = get_tradedate_by_enddate_tradedates(enddate, n_days)
    # 生成日期list
    date_period = get_my_start_end_date_list(start_date, enddate)
    # 获取周期内的交易数据
    df_date_period = select_data_by_datelist(date_period)

    # 调整数据格式
    df_format_float = df_date_period.astype({'low': 'float64', 'close': 'float64', 'pct_chg': 'float64'}, copy=True)

    # 获取指定日期段中，最早的交易日期
    end_trade_date = df_format_float.trade_date.max()
    # 以最早日期有交易个股为基准，进行计算。不考虑日期段上市的新股
    df_end_trade_date = df_format_float.loc[df_format_float['trade_date'] == end_trade_date]
    # 周期截止日，有交易个股list
    ts_code_list_enddate = df_end_trade_date.ts_code.tolist()

    # 按照最后交易日中个股，逐一筛选周期内最低价，将最低价与最后交易日的收盘价对比，计算周期内最大涨幅。
    data_list = []
    for i in range(0, len(ts_code_list_enddate)):
        # 根据个股代码遍历，获取个股代码
        df_cacul_ts_code = df_format_float.loc[df_format_float['ts_code'] == ts_code_list_enddate[i]]
        # 获取最小，最大index名称，方便切片
        lowest = df_cacul_ts_code.low.min()
        # 最后一个交易额收盘价
        end_trade_date_close = df_cacul_ts_code['close'].tolist()[-1]

        # 涨幅
        pct_chg = '%0.2f' % (end_trade_date_close / lowest * 100 - 100)
        data_list.append([ts_code_list_enddate[i], pct_chg])

    mycolumns = ['ts_code', 'max_zhangfu']
    df_result = pd.DataFrame(data=data_list, columns=mycolumns).astype({'max_zhangfu': 'float'})
    df_result_sorted = df_result.sort_values(by='max_zhangfu', ascending=False)
    # 添加个股信息
    df_full_msg = add_share_msg_to_df(df_result_sorted)

    # 最新一日交易数据

    # 取最后交易日的交易数据，补充最后交易日的涨跌幅。
    df_max_date = df_format_float.loc[df_format_float['trade_date'] == end_trade_date]

    df_add_new_tradedata = pd.merge(left=df_full_msg, right=df_max_date, on='ts_code')
    df_result_final = df_add_new_tradedata.loc[:, ['name', 'ts_code', 'industry', 'max_zhangfu', 'pct_chg']]
    df_result_final.columns = ['名称', '代码', '板块', str(n_days) + '日最大涨幅', '今日涨幅']
    # print(df_result_final.keys())
    # 调整数据格式
    # df_result_final['名称'] = df_result_final['名称'].map(lambda x: x[0:2])
    df_result_final['今日涨幅'] = df_result_final['今日涨幅'].map(lambda x: '%0.2f' % x)
    df_result_final[str(n_days) + '日最大涨幅'] = df_result_final[str(n_days) + '日最大涨幅'].map(lambda x: '%0.2f' % x)

    path = r'D:\00 量化交易\\' + enddate[-4:] + "日" + str(n_days) + '天高标动态.xlsx'
    df_result_final.to_excel(path, sheet_name='1', engine='openpyxl')

    # 绘制表格。需要重置index
    mytable = draw_table_by_df(df_result_final.head(20).reset_index(), enddate[-4:] + "日" + str(n_days) + '天高标动态')

    return mytable


def caculate_gaobiao_7_14():
    # 结束日期选择今天
    enddate = get_today_date()
    caculate_ndays_zhangfu(enddate, 14)
    caculate_ndays_zhangfu(enddate, 7)

# caculate_ndays_zhangfu(get_today_date(), 7)
