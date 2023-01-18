# 建立mysql数据库的连接
from sqlalchemy import create_engine
import pandas as pd


# 选择多日的龙虎榜
def select_days_longhubang(datelist):
    datelist_str = ",".join(datelist)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')

    mysql_1 = "SELECT  * FROM longhubang WHERE trade_date IN (" + datelist_str + ") "

    df = pd.read_sql(mysql_1, conn)

    return df