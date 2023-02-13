# 每日涨停，匹配流通股本，总股本，行业数据。
# 每日涨幅top200，匹配流通股本，总股本，行业数据。
from add_share_msg import add_share_guben_to_df
from select_sql_tradedata import select_share_by_date
from select_tradedata_by_dataframe import select_zhangting_or_dieting_by_tradedf


# sharetype select_zhangting_or_dieting_by_tradedf。可选 涨停 和跌停 和炸板
def querydate_tradedata_add_msg(querydate, sharetype):
    # 获取指定日期的交易数据
    today_trade_df_origin = select_share_by_date(querydate)
    # 补充个股的信息。名称——股本等等
    df_add_msg_add_guben = add_share_guben_to_df(today_trade_df_origin)

    # 调整数据格式
    df_format_float = df_add_msg_add_guben.astype(
        {'close': 'float64', 'float_share': 'float64', 'total_share': 'float64', 'amount': 'float64'},
        copy=True)

    # 计算个股的流值和总值。暂缺北交所数据
    df_format_float['float_share_amount'] = df_format_float['close'] * df_format_float['float_share']
    df_format_float['total_share_amount'] = df_format_float['close'] * df_format_float['total_share']

    # 以下代码为调整格式，和筛选数据的代码。

    df_zhangting = select_zhangting_or_dieting_by_tradedf(df_format_float, sharetype)
    # 交易额由 千 调整为 亿
    df_zhangting['amount'] = df_zhangting.loc[:, 'amount'] / 100000
    # 保留部分字段
    df_total_share_remain = df_zhangting.loc[
                            :, ['ts_code', 'trade_date_x', 'pct_chg', 'amount', 'name',
                                'industry', 'area', 'float_share_amount', 'total_share_amount', '分析类型']]
    #  重置列名
    df_total_share_remain.columns = ['代码', '交易日', '涨幅', '成交（亿）', '名称', '行业', '城市', '流值（亿）', '总值（亿）', '分析类型']
    # 调整顺序
    df_total_share_remain_ordered = df_total_share_remain[
        ['交易日', '代码', '名称', '行业', '城市', '总值（亿）', '流值（亿）', '成交（亿）', '涨幅', '分析类型']]
    # 以上代码为调整格式，和筛选数据的代码。

    # TODO 排序

    share_df_sorted = df_total_share_remain_ordered.sort_values(by=['涨幅', '成交（亿）'],
                                                                ascending=False,
                                                                ignore_index=True)

    path = r'D:\00 量化交易\\' + querydate + '日' + sharetype + '（含市值流值）.xlsx'
    # 取2位小数，并导出数据
    share_df_sorted.round(2).to_excel(path, sheet_name='1', engine='openpyxl')

    print('计算' + querydate + '日' + sharetype + '数据')
    print(df_total_share_remain_ordered)

    # 返回计算的数据
    return df_total_share_remain_ordered


def querydate_tradedata_add_msg_zt_and_dt(querydate):
    querydate_tradedata_add_msg(querydate, '涨停跌停炸板')
    querydate_tradedata_add_msg(querydate, '涨停')
    querydate_tradedata_add_msg(querydate, '炸板')
    querydate_tradedata_add_msg(querydate, '跌停')


# querydate = get_today_date()

'''querydate = '20230209'
querydate_tradedata_add_msg_zt_and_dt(querydate)
'''