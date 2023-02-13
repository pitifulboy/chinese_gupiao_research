# 每日涨停，匹配流通股本，总股本，行业数据。
# 每日涨幅top200，匹配流通股本，总股本，行业数据。
from add_share_msg import add_share_guben_to_df
from my_time_func import get_today_date, get_my_start_end_date_list
from select_sql_tradedata import select_share_by_date, select_data_by_datelist
from select_tradedata_by_dataframe import select_zhangting_or_dieting_by_tradedf


def query_sharetype_by_day_or_days(day_or_days):
    # 判断输入的是str格式的day。还是list格式的days

    if isinstance(day_or_days, str):
        print('计算单日')
        today_trade_df_origin = select_share_by_date(day_or_days)
    if isinstance(day_or_days, list):
        print('计算多日')
        today_trade_df_origin = select_data_by_datelist(day_or_days)

    # 根据df计算一天内的   涨停 和跌停 和炸板

    query_zt_zb_dt_by_df(today_trade_df_origin, '涨停跌停炸板')
    query_zt_zb_dt_by_df(today_trade_df_origin, '涨停')
    query_zt_zb_dt_by_df(today_trade_df_origin, '炸板')
    query_zt_zb_dt_by_df(today_trade_df_origin, '跌停')


# sharetype select_zhangting_or_dieting_by_tradedf。可选 涨停 和跌停 和炸板
def query_zt_zb_dt_by_df(df, sharetype):
    querydate = get_today_date()

    # 补充个股的信息。名称——股本等等
    df_add_msg_add_guben = add_share_guben_to_df(df)

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

    #  排序
    share_df_sorted = df_total_share_remain_ordered.sort_values(by=['涨幅', '成交（亿）'], ascending=False, ignore_index=True)

    path = r'D:\00 量化交易\\' + querydate + '日查询' + sharetype + '（含市值流值）.xlsx'
    # 取2位小数，并导出数据
    share_df_sorted.round(2).to_excel(path, sheet_name='1', engine='openpyxl')

    print(querydate + '日,查询' + sharetype + '数据')
    print(share_df_sorted)

    # 返回计算的数据
    return share_df_sorted


# querydate = get_today_date()
'''day_or_days = '20230208'
# day_or_days = get_my_start_end_date_list('20230201', '20230210')
query_sharetype_by_day_or_days(day_or_days)
'''
