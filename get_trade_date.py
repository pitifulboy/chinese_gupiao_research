import tushare as ts


def get_trade_datelist(startdate, enddate):
    pro = ts.pro_api()
    # tushare 交易日历数据接口
    df = pro.trade_cal(exchange='', start_date=startdate, end_date=enddate)
    df.sort_values(by="cal_date", inplace=True, ascending=True)
    df_trade_date = df[df['is_open'] == 1]

    df_trade_date_list = df_trade_date['cal_date'].tolist()
    # 升序排列
    df_trade_date_list.sort(reverse=False)

    return df_trade_date_list


# eg 使用示例：
# print(get_trade_datelist('20180101', '20181231'))

# 获取指定交易日期n个交易日后的交易日期
def get_trade_date_n_days_after(startdate, n):
    pro = ts.pro_api()
    # tushare 交易日历数据接口,获取完整的交易日历
    df = pro.trade_cal(exchange='')
    # 将df 按照cal_date升序排列
    df.sort_values(by="cal_date", inplace=True, ascending=True)

    # 获取指定日期所在行序号的名称
    index_n = df[df['cal_date'] == startdate].index.tolist()[0]
    df_trade_date = df[df['is_open'] == 1]
    # 获取从指定日期后续的交易日期表df
    df_trade_date_startdate = df_trade_date.loc[index_n:]
    # 将交易日期转换成list
    df_trade_date_startdate_n_days_after_list = df_trade_date_startdate['cal_date'].tolist()

    # 获取n天后的交易日期
    n_days_after = df_trade_date_startdate_n_days_after_list[n]

    return n_days_after


# 指定截止日期enddate，和交易日的数量n，最后一个交易日前的n个交易日的日期
def get_tradedate_by_enddate_tradedates(enddate, n):
    pro = ts.pro_api()
    # tushare 交易日历数据接口,获取完整的交易日历
    df = pro.trade_cal(exchange='')
    df.sort_values(by="cal_date", inplace=True, ascending=True)

    # 获取指定日期所在行序号的名称
    index_n = df[df['cal_date'] == enddate].index.tolist()[0]
    # 获取从指定日期前面的日期表df
    df_trade_date_enddate = df.loc[:index_n]
    # 筛选出交易日的数据
    df_trade_date = df_trade_date_enddate[df_trade_date_enddate['is_open'] == 1]
    # 将交易日期转换成list
    df_trade_date_enddate_n_tradedays_before = df_trade_date['cal_date'].tolist()
    # 获取n天前的交易日期
    n_traddedays_before = df_trade_date_enddate_n_tradedays_before[-n - 1]

    return n_traddedays_before
