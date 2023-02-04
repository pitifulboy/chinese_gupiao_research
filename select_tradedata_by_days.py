# 建立mysql数据库的连接
from sqlalchemy import create_engine
import pandas as pd
# 涨停股票dataframe,根据涨跌幅限制选择.10%,20%,30%涨跌幅
from my_zhangdie_limit import get_zhangdie_limit


def select_zhangtingban_df(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    # 调整数据格式
    df_format_float = df1.astype({'close': 'float64', 'pre_close': 'float64'}, copy=True)

    # 涨停个股角标数字
    share_list_num = []
    for i in range(len(df_format_float)):
        ts_code = df_format_float['ts_code'][i]
        limit = get_zhangdie_limit(ts_code)
        close = '%.2f' % (df_format_float["close"][i])
        pre_close = df_format_float["pre_close"][i]
        # 涨停价
        up_limit = '%.2f' % (pre_close * (1 + limit))

        if close == up_limit:
            share_list_num.append(i)

    return df_format_float.iloc[share_list_num]


# 选出炸板股票dataframe，根据涨跌幅限制选择.10%,20%,30%涨跌幅
def select_zhaban_df(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    # 调整数据格式
    df_format_float = df1.astype({'high': 'float64', 'close': 'float64', 'pre_close': 'float64'}, copy=True)

    share_list_num = []

    for i in range(len(df_format_float)):
        ts_code = df_format_float['ts_code'][i]
        limit = get_zhangdie_limit(ts_code)

        high = '%.2f' % (df_format_float["high"][i])
        close = '%.2f' % (df_format_float["close"][i])
        pre_close = df_format_float["pre_close"][i]
        # 涨停价
        up_limit = '%.2f' % (pre_close * (1 + limit))

        # 炸板股票
        if high == up_limit and close < up_limit:
            share_list_num.append(i)

    return df_format_float.iloc[share_list_num]


def select_dietingban_df(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    # 调整数据格式
    df_format_float = df1.astype({'high': 'float64', 'close': 'float64', 'pre_close': 'float64'}, copy=True)

    share_list_num = []

    for i in range(len(df_format_float)):
        ts_code = df_format_float['ts_code'][i]
        limit = get_zhangdie_limit(ts_code)

        close = '%.2f' % (df_format_float["close"][i])
        pre_close = df_format_float["pre_close"][i]
        # 跌停价
        down_limit = '%.2f' % (pre_close * (1 - limit))

        if close == down_limit:
            share_list_num.append(i)

    return df_format_float.iloc[share_list_num]

