from my_zhangdie_limit import get_zhangdie_limit


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
