import numpy as np
from add_share_msg import add_share_msg_to_df
from get_trade_date import get_trade_datelist, get_trade_date_n_days_after
import pandas as pd
from select_sql_lhb import select_days_longhubang
from select_sql_tradedata import select_data_by_shareslist_datelist


def lhb_analysis(my_datelist):
    # 获取指定周期内，龙虎榜数据
    lhb_data = select_days_longhubang(my_datelist)
    # 本次分析龙虎榜后一个交易日收益情况，获取指定日期后一个交易日
    print(my_datelist[-1])
    next_tradedate = get_trade_date_n_days_after(my_datelist[-1], 1)
    print(next_tradedate)

    my_tradedate_datelist = get_trade_datelist(my_datelist[0], next_tradedate)

    # 股票list去重
    lhb_sharelist = list(set(lhb_data['ts_code'].tolist()))
    # 根据日期和代码，获取所需的全部交易数据
    tradedata = select_data_by_shareslist_datelist(lhb_sharelist, my_tradedate_datelist)

    # 在龙虎榜数据中，增加上榜日后一个交易日。字段
    lhb_data['next_trade_date'] = lhb_data['trade_date'].apply(
        lambda x: my_tradedate_datelist[my_tradedate_datelist.index(x) + 1])

    # 根据龙虎榜中的 代码+日期，匹配龙虎榜当日交易数据。
    lhb_and_tradedata = pd.merge(lhb_data, tradedata, on=['trade_date', 'ts_code'])
    # 根据龙虎榜中的 代码+日期，匹配龙虎榜次日交易数据。
    lhb_and_tradedata = pd.merge(lhb_and_tradedata, tradedata, left_on=['next_trade_date', 'ts_code'],
                                 right_on=['trade_date', 'ts_code'])
    # 根据龙虎榜中的 代码，匹配个股信息。
    lhb_and_tradedata_add_info = add_share_msg_to_df(lhb_and_tradedata)

    # 调整数据格式
    df_format_float = lhb_and_tradedata_add_info.astype({'open_y': 'float64', 'high_y': 'float64', 'low_y': 'float64',
                                                         'close_y': 'float64', 'pre_close_y': 'float64'}, copy=True)

    df_format_float['次日开盘涨幅'] = (
            df_format_float['open_y'] / df_format_float['pre_close_y'] * 100 - 100)
    df_format_float['次日最大涨幅'] = (
            df_format_float['high_y'] / df_format_float['pre_close_y'] * 100 - 100)
    df_format_float['次日最小涨幅'] = (
            df_format_float['low_y'] / df_format_float['pre_close_y'] * 100 - 100)
    df_format_float['次日收盘涨幅'] = (
            df_format_float['close_y'] / df_format_float['pre_close_y'] * 100 - 100)

    lhb_and_tradedata_remain = df_format_float.loc[:, ['trade_date_x', 'exalter', 'symbol', 'name', 'area',
                                                       'industry', 'market', 'list_date', '次日开盘涨幅',
                                                       '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅']]

    lhb_and_tradedata_remain.drop_duplicates(inplace=True)

    path = r'D:\00 量化交易\\' + my_datelist[0] + '-' + my_datelist[-1] + '龙虎榜次日表现明细' + '.xlsx'
    lhb_and_tradedata_remain.to_excel(path, sheet_name='龙虎榜次日表现明细', engine='openpyxl', index=None)

    return lhb_and_tradedata_remain


# 透视龙虎榜
def lhb_povit_df(alldata_as_type):
    startdate = alldata_as_type['trade_date_x'].min()
    enddate = alldata_as_type['trade_date_x'].max()
    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(alldata_as_type, index='exalter',
                                  values=['次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅'],
                                  aggfunc={'exalter': np.count_nonzero, '次日开盘涨幅': np.average, '次日最大涨幅': np.average,
                                           '次日最小涨幅': np.average,
                                           '次日收盘涨幅': np.average})

    # 导出结果
    path2 = r'D:\00 量化交易\\' + startdate + '-' + enddate + '龙虎榜次日表现透视汇总' + '.xlsx'
    lhb_df_povit.to_excel(path2, sheet_name='龙虎榜次日表现透视汇总', engine='openpyxl')

    return lhb_df_povit


'''# 选定分析周期
start_date = '20230106'
end_date = '20230213'
my_datelist = get_trade_datelist(start_date, end_date)
df = lhb_analysis(my_datelist)
df2 = lhb_povit_df(my_datelist, df)
print(df2.keys())
'''
