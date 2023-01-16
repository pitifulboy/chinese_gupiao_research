import tushare as ts


def get_trade_datelist(startdate, enddate):
    pro = ts.pro_api()
    # tushare 交易日历数据接口
    df = pro.trade_cal(exchange='', start_date=startdate, end_date=enddate)
    df_trade_date = df[df['is_open'] == 1]

    df_trade_date_list = df_trade_date['cal_date'].tolist()

    return df_trade_date_list

# eg 使用示例：
# get_trade_datelist('20180101', '20181231')
