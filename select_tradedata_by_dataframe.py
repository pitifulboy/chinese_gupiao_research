from share_classify import get_zhangdie_limit
from select_sql_tradedata import select_share_by_date


def select_zhaban_df_bydf(daylitrade_df):
    # 调整数据格式
    df_format_float = daylitrade_df.astype({'close': 'float64', 'high': 'float64', 'pre_close': 'float64'}, copy=True)
    df1 = df_format_float
    share_list_num = []

    for i in range(len(df1)):
        ts_code = df1['ts_code'].tolist()[i]
        limit = get_zhangdie_limit(ts_code)

        high = '%.2f' % (df1["high"].tolist()[i])
        close = '%.2f' % (df1["close"].tolist()[i])
        pre_close = df1["pre_close"].tolist()[i]
        # 涨停价
        up_limit = '%.2f' % (pre_close * (1 + limit))

        # 炸板股票
        if high == up_limit and close < up_limit:
            share_list_num.append(i)

    return df1.iloc[share_list_num]


def select_zhangtingban_df_bydf(daylitrade_df):
    # 调整数据格式
    df_format_float = daylitrade_df.astype({'close': 'float64', 'pre_close': 'float64'}, copy=True)
    df1 = df_format_float

    # 涨停个股角标数字
    share_list_num = []
    for i in range(len(df1)):
        ts_code = df1['ts_code'].tolist()[i]
        limit = get_zhangdie_limit(ts_code)

        close = '%.2f' % (df1["close"].tolist()[i])
        pre_close = df1["pre_close"].tolist()[i]
        # 涨停价
        up_limit = '%.2f' % (pre_close * (1 + limit))

        if close == up_limit:
            share_list_num.append(i)

    return df1.iloc[share_list_num]


# type 类型可选“涨停”或者“”跌停
def select_zhangting_or_dieting_by_tradedf(mydf, mytype):
    # type 类型可选“涨停”或者“”跌停
    # 调整格式
    df_format_float = mydf.astype(
        {'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64', 'pre_close': 'float64',
         'change': 'float64', 'pct_chg': 'float64', 'vol': 'float64', 'amount': 'float64'}, copy=True)

    # 计算涨跌幅上下限，并判断是否涨跌停

    df_format_float['涨跌幅'] = df_format_float['ts_code'].apply(lambda x: get_zhangdie_limit(x))

    df_format_float['涨停价'] = (df_format_float['pre_close'] * (1 + df_format_float['涨跌幅'])).astype('float64', copy=True)
    df_format_float['涨停价'] = df_format_float['涨停价'].apply(lambda x: '%.2f' % x).astype('float64')

    df_format_float['跌停价'] = df_format_float['pre_close'] * (1 - df_format_float['涨跌幅']).astype('float64', copy=True)
    df_format_float['跌停价'] = df_format_float['跌停价'].apply(lambda x: '%.2f' % x).astype('float64')

    df_format_float['分析类型'] = ''

    # 给个股添加涨停，跌停，炸板状态
    # 最高价是涨停价的，设置为“炸板”（内含涨停），然后，再次设置，收盘价为“涨停价”的，设置为”涨停“
    df_format_float.loc[df_format_float['涨停价'] == df_format_float['high'], '分析类型'] = "炸板"
    df_format_float.loc[df_format_float['涨停价'] == df_format_float['close'], '分析类型'] = "涨停"
    df_format_float.loc[df_format_float['跌停价'] == df_format_float['close'], '分析类型'] = "跌停"

    if mytype == '涨停':
        return df_format_float[df_format_float['分析类型'] == '涨停']
    if mytype == '跌停':
        return df_format_float[df_format_float['分析类型'] == '跌停']
    if mytype == '炸板':
        return df_format_float[df_format_float['分析类型'] == '炸板']
    if mytype == '涨停跌停炸板':
        return df_format_float[df_format_float['分析类型'] != '']


# 示例
# 获取制定日期的交易数据
'''df = select_share_by_date('20230203')
print(select_zhangting_or_dieting_by_tradedf(df, '涨停跌停炸板'))'''
