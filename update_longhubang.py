from sqlalchemy import create_engine
import tushare as ts
import time
from get_trade_date import get_trade_datelist
from get_tushare_token import get_tushare_token
from my_time_func import get_today_date, get_days_after_tushare
from selet_sql_maxdate import get_lhb_maxdate


def update_longhubang(querydate):
    # 建立mysql数据库的连接
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')

    mytoken = get_tushare_token()

    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    # 拉取数据
    df = pro.top_inst(**{
        "trade_date": querydate,
        "ts_code": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "trade_date",
        "ts_code",
        "exalter",
        "buy",
        "buy_rate",
        "sell",
        "sell_rate",
        "net_buy",
        "side",
        "reason"
    ])
    print(df)

    new_df = df.fillna(value=0)
    new_df.to_sql('longhubang', con=conn, if_exists='append', index=False)


def first_time_longhubang(startdate):
    update_longhubang(startdate)


# 首次使用，手动指定开始日期，后续默认补全
# update_longhubang('20180103')

def update_longhubang_auto():
    #  更新龙虎榜
    # 获取最新日期
    todaydate = get_today_date()
    # 获取mysql中存入的龙虎榜的最新日期
    maxdate = get_lhb_maxdate()
    # 起始日期是mysql日期的后一天
    update_start = get_days_after_tushare(maxdate, 1)
    print(update_start)

    # 判断mysql中是否已经更新最新数据，如果不是最新数据
    if maxdate != todaydate:
        # 生成需要更新的datelist
        date_list = get_trade_datelist(update_start, todaydate)
        for i in range(0, len(date_list)):
            # 分钟最多访问该接口60次，权限的具体详情访问：https://tushare.pro/document/1?doc_id=108。
            # 运行60次后，休息61秒
            if (i + 1) % 60 == 0:
                time.sleep(61)
                print("暂停读取")
            else:
                update_longhubang(date_list[i])



