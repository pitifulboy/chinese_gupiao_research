import numpy as np
from numpy import sort
from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_start_end_date_list, datelist_add_days
from select_shares import select_days_longhubang, select_data_by_shareslist_datelist

import pandas as pd
from update_longhubang import update_longhubang_auto


def lhb_analysis(my_datelist):
    # 获取指定周期内，龙虎榜数据
    lhb_data = select_days_longhubang(my_datelist)
    # 增加3个自然日，认为3天内必有一个交易日。（暂只考虑周末2天休息）
    my_tradedate_datelist = datelist_add_days(my_datelist, 3)
    # 股票list去重
    lhb_sharelist = list(set(lhb_data['ts_code'].tolist()))
    # 根据日期和代码，获取所需的全部交易数据
    tradedata = select_data_by_shareslist_datelist(lhb_sharelist, my_tradedate_datelist)

    # 在龙虎榜数据中，计算上榜日后一个交易日。
    trade_date_list = sort(tradedata['trade_date'].tolist())
    # 交易日期去重，默认升序排列
    trade_date_list_sorted = [i for n, i in enumerate(trade_date_list) if i not in trade_date_list[:n]]
    # 在龙虎榜数据中，增加上榜日后一个交易日。字段
    lhb_data['next_trade_date'] = lhb_data['trade_date'].apply(
        lambda x: trade_date_list_sorted[trade_date_list_sorted.index(x) + 1])

    # 根据龙虎榜中的 代码+日期，匹配龙虎榜当日交易数据。
    lhb_and_tradedata = pd.merge(lhb_data, tradedata, on=['trade_date', 'ts_code'])
    # 根据龙虎榜中的 代码+日期，匹配龙虎榜次日交易数据。
    lhb_and_tradedata = pd.merge(lhb_and_tradedata, tradedata, left_on=['next_trade_date', 'ts_code'],
                                 right_on=['trade_date', 'ts_code'])
    # 根据龙虎榜中的 代码，匹配个股信息。
    lhb_and_tradedata_add_info = add_share_msg_to_df(lhb_and_tradedata)

    # 格式整理，并计算次日收益指标。
    # TODO：异常情况：龙虎榜次日停牌，无交易数据。各项收益指标填为0.

    lhb_and_tradedata_add_info['次日开盘涨幅'] = (
            lhb_and_tradedata_add_info['open_y'] / lhb_and_tradedata_add_info['pre_close_y'] * 100 - 100)
    lhb_and_tradedata_add_info['次日最大涨幅'] = (
            lhb_and_tradedata_add_info['high_y'] / lhb_and_tradedata_add_info['pre_close_y'] * 100 - 100)
    lhb_and_tradedata_add_info['次日最小涨幅'] = (
            lhb_and_tradedata_add_info['low_y'] / lhb_and_tradedata_add_info['pre_close_y'] * 100 - 100)
    lhb_and_tradedata_add_info['次日收盘涨幅'] = (
            lhb_and_tradedata_add_info['close_y'] / lhb_and_tradedata_add_info['pre_close_y'] * 100 - 100)

    lhb_and_tradedata_remain = lhb_and_tradedata_add_info.loc[:, ['trade_date_x', 'exalter', 'symbol', 'name', 'area',
                                                                  'industry', 'market', 'list_date', '次日开盘涨幅',
                                                                  '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅']]

    lhb_and_tradedata_remain.drop_duplicates(inplace=True)

    path = r'D:\00 量化交易\\' + my_datelist[0] + '-' + my_datelist[-1] + '龙虎榜次日表现明细' + '.xlsx'
    lhb_and_tradedata_remain.to_excel(path, sheet_name='龙虎榜次日表现明细', engine='openpyxl', index=None)

    lhb_povit_df(my_datelist, lhb_and_tradedata_remain)


def lhb_povit_df(my_datelist, alldata_as_type):
    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(alldata_as_type, index='exalter',
                                  values=['次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅'],
                                  aggfunc={'exalter': np.count_nonzero, '次日开盘涨幅': np.average, '次日最大涨幅': np.average,
                                           '次日最小涨幅': np.average,
                                           '次日收盘涨幅': np.average})

    # 导出结果
    path2 = r'D:\00 量化交易\\' + my_datelist[0] + '-' + my_datelist[-1] + '龙虎榜次日表现透视汇总' + '.xlsx'
    lhb_df_povit.to_excel(path2, sheet_name='龙虎榜次日表现透视汇总', engine='openpyxl')


# 更新龙虎榜
update_longhubang_auto()

# 选定分析周期（结束日期最好是本周首个交易日，避免数据不足引起的错误）
my_datelist = get_my_start_end_date_list('20230101', '20230111')
lhb_analysis(my_datelist)
