# 建立mysql数据库的连接
from sqlalchemy import create_engine
import pandas as pd


# 指定datelist所有交易数据
def select_data_by_datelist(datelist):
    date_str = ",".join(datelist)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date IN (" + date_str + ") "
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择一组股票交易数据，指定datelist,指定股票代码
def select_data_by_shareslist_datelist(share_list, datelist):
    share_str = "','".join(share_list)
    date_str = ",".join(datelist)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE ts_code IN ('" + share_str + "') AND trade_date IN (" + date_str + ") "
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择一组股票交易数据，设置截止日期
def select_data_by_shareslist_lastdate(share_list, lastdate):
    str = "','".join(share_list)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE ts_code IN ('" + str + "') AND trade_date <= " + lastdate + " ORDER BY trade_date ASC"
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选出一天的所有交易数据
def select_share_by_date(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    return df1
