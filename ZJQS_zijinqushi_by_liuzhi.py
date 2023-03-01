import numpy as np
import pandas as pd
from pyecharts.options import ComponentTitleOpts

from add_share_shizhi import add_shizhi_info_by_df
from draw_table import draw_table_by_df
from get_trade_date import get_trade_datelist
from my_num_func import my_round_45
from select_sql_tradedata import select_data_by_datelist, select_share_by_date
from select_tradedata_by_dataframe import select_zhangting_or_dieting_by_tradedf

from pyecharts.components import Table

# 按市值分组
from share_classify import get_share_market


def days():
    startday = '20230220'
    endday = '20230224'
    datelist = get_trade_datelist(startday, endday)
    print(datelist)
    # 获取datelist内，所有交易日内的数据
    tradedata_by_datelist_df = select_data_by_datelist(datelist)
    df = add_shizhi_info_by_df(tradedata_by_datelist_df, '全部')
    print(df)

    # 删除 流通市值为0 或者为 空的数据
    # 按照流动市值，分组，计算资金趋势+涨跌幅趋势
    # 0-100，100-300，300-500，500-1000，1000+
    # 0-50，50-100.。。。。。

    # 留值划分
    def shizhifenzu(x):
        if x < 50:
            result = '0-50'
        elif x < 100:
            result = '50-100'
        elif x < 200:
            result = '100-200'
        elif x < 300:
            result = '200-300'
        elif x < 500:
            result = '300-500'
        elif x < 1000:
            result = '500-1000'
        else:
            result = '1000+'
        return result

    # 分组
    df['流值分组'] = df['流值（亿）'].apply(shizhifenzu)
    df['板块'] = df['代码'].apply(get_share_market)
    print(df)

    # 删除市值为0 和市值为 空的行
    df.dropna(subset='流值（亿）', inplace=True)
    df_result = df[df['流值（亿）'] != 0].copy()

    path = r'D:\00 量化交易\\流值分析.xlsx'
    df_result.to_excel(path, sheet_name='1', engine='openpyxl')

    # 按天拉交易数据，统计。


# 流值划分
def shizhifenzu(x):
    if x < 50:
        result = '0-50'
    elif x < 100:
        result = '50-100'
    elif x < 200:
        result = '100-200'
    elif x < 300:
        result = '200-300'
    elif x < 500:
        result = '300-500'
    elif x < 1000:
        result = '500-1000'
    else:
        result = '1000+'
    return result


def one_day_bankuai_liuzhi_fenxi(queryday):
    # 获取datelist内，所有交易日内的数据
    tradedata_by_date = select_share_by_date(queryday)
    df = add_shizhi_info_by_df(tradedata_by_date, '全部')

    # 删除 流通市值为0 或者为 空的数据
    # 按照流动市值，分组，计算资金趋势+涨跌幅趋势
    # 0-100，100-300，300-500，500-1000，1000+
    # 0-50，50-100.。。。。。

    # 分组
    df['流值范围'] = df['流值（亿）'].apply(shizhifenzu)
    df['板块'] = df['代码'].apply(get_share_market)

    # 删除市值为0 和市值为 空的行
    df.dropna(subset='流值（亿）', inplace=True)
    df_result = df[df['流值（亿）'] != 0].copy()

    path = r'D:\00 量化交易\\' + queryday + '盘面分析.xlsx'
    df_result.to_excel(path, sheet_name='盘面分析', engine='openpyxl')

    # 透视
    df_result_povit = pd.pivot_table(df_result, index=['板块', '流值范围'],
                                     aggfunc={'代码': np.count_nonzero, '成交（亿）': np.sum, '当日涨幅': np.average})
    df_result_povit.columns = ['个数', '平均涨幅', '成交（亿）']

    # 调整格式
    df_result_povit['平均涨幅'] = df_result_povit['平均涨幅'].apply(lambda x: my_round_45(x, 1)).astype('float64')
    df_result_povit['成交（亿）'] = df_result_povit['成交（亿）'].apply(lambda x: my_round_45(x, 0)).astype('float64')

    # 导出结果
    path2 = r'D:\00 量化交易\\' + queryday + '盘面分析透视.xlsx'
    df_result_povit.to_excel(path2, sheet_name='盘面分析透视', engine='openpyxl')

    # 绘制表格。需要重置index，并调整格式
    df_draw = df_result_povit.reset_index().copy().round(2)
    draw_table_by_df(df_draw, queryday + '盘面分析透视')

# one_day_bankuai_liuzhi_fenxi('20230228')
