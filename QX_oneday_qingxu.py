from ZJQS_dp_zt_zb import qinxu_jiaoyie_oneday
from LBTT import oneday_lbtt
from select_sql_tradedata import select_share_by_date
from select_tradedata_by_dataframe import select_zhangting_or_dieting_by_tradedf


def QX_zhibiao(trade_data_oneday):
    # data :日期，大盘交易额，涨停交易额，涨停数，炸板交易额，炸板数，跌停交易额，跌停数
    data = qinxu_jiaoyie_oneday(trade_data_oneday)
    querydate = trade_data_oneday['trade_date'].tolist()[0]

    # 连板
    lb_df = oneday_lbtt(querydate)
    n_lb_df = len(lb_df)

    print(querydate)
    print('A股今日交易额：' + str(data[1]) + '亿')

    print('-------------------------------')
    print('今日涨停:' + str(data[3]) + '个')
    print('其中连板:' + str(n_lb_df) + '个')

    print('涨停个股今日交易额：' + str(data[2]) + '亿')

    print('-------------------------------')
    print('炸板：' + str(data[5]) + '个')
    print('炸板个股今日交易额：' + str(data[4]) + '亿')

    print('跌停：' + str(data[7]) + '个')
    print('跌停个股今日交易额：' + str(data[6]) + '亿')

    print('-------------------------------')
    print('备注：忽略部分ST个股。')


#QX_zhibiao(select_share_by_date('20230224'))
