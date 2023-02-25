from sqlalchemy import create_engine
import tushare as ts
# 更新单日交易数据
from get_trade_date import get_trade_datelist
from get_tushare_token import get_tushare_token
from my_time_func import get_days_delta_tushare, get_today_date
from selet_sql_maxdate import get_dailytrade_maxdate


def update_tradedata_from_tushare(trade_date):
    # 建立mysql数据库的连接
    # 需要修改成自己配置的数据库参数
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mytoken = get_tushare_token()
    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    df = pro.daily(**{
        "ts_code": "",
        "trade_date": trade_date,
        "start_date": "",
        "end_date": "",
        "offset": "",
        "limit": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "pre_close",
        "change",
        "pct_chg",
        "vol",
        "amount"
    ])
    df.to_sql('dailytrade', con=conn, if_exists='append', index=False)

    # 写入mysql数据库
    print("交易日期：")
    print(trade_date)
    print("交易数据：")
    print(df)


# 更新多日交易数据
def update_tradedata_from_toshare_by_datelist(datelist):
    for i in range(0, len(datelist)):
        update_tradedata_from_tushare(datelist[i])


def first_time_trade_data(startdate):
    update_tradedata_from_tushare(startdate)


# 首次使用，手动指定开始日期，后续默认补全交易数据。
# first_time_trade_data('20180103')

def update_trade_data():
    # 获取mysql中，存储的最大交易日期
    maxdate = get_dailytrade_maxdate()

    # 生成已存的日期-今天的交易日期list
    # 起始日期是mysql日期的后一天
    update_start = get_days_delta_tushare(maxdate, 1)

    # 获取最新日期
    todaydate = get_today_date()

    # 判断mysql中是否已经更新最新数据，如果不是最新数据
    if maxdate != todaydate:
        # 生成需要更新的datelist
        date_list = get_trade_datelist(update_start, todaydate)
        # 更新日常交易数据
        update_tradedata_from_toshare_by_datelist(date_list)

# 备注，tushare文档提示：
# 数据说明：交易日每天15点～16点之间入库。本接口是未复权行情，停牌期间不提供数据
# 调取说明：120积分每分钟内最多调取500次，每次6000条数据，相当于单次提取23年历史
# 描述：获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据

#update_trade_data()
