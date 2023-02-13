# 个股特性，直接与ts_code匹配。添加字段

# 暂不考虑st股票
# 沪市主板 6开头  10%涨跌幅
# 深市主板 0开头  10%涨跌幅
# 北交所 4，8开头  30%涨跌幅
# 创业板 3开头   20%涨跌幅
# 科创板 68开头  20%涨跌幅
from select_sql_tradedata import select_share_by_date


def get_zhangdie_limit(ts_code):
    limit = 0
    if ts_code[0:1] == '0':
        limit = 0.1
    elif ts_code[0:1] == '3':
        limit = 0.2
    elif ts_code[0:1] == '4':
        limit = 0.3
    elif ts_code[0:1] == '8':
        limit = 0.3
    elif ts_code[0:2] == '68':
        limit = 0.2
    elif ts_code[0:1] == '6':
        limit = 0.1
    return limit


# 给含有ts_code 的dataframe 添加涨跌幅上下限。
def add_zhangdie_limit_to_df(df):
    df['zhangdie_limit'] = df['ts_code'].apply(get_zhangdie_limit)
    return df


'''
测试用
 
# 获取指定日期的交易数据
querydate = '20230209'
today_trade_df_origin = select_share_by_date(querydate)
dfdf=add_zhangdie_limit_to_df(today_trade_df_origin)
print(dfdf)

path = r'D:\00 量化交易\\aaa.xlsx'
dfdf.to_excel(path, sheet_name='1', engine='openpyxl')'''
