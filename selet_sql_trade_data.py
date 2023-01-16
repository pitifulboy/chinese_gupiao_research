# 建立mysql数据库的连接
from sqlalchemy import create_engine
import pandas as pd


# 选出日常交易中，最大日期，便于更新日常数据
def get_dailytrade_maxdate():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql = "SELECT MAX(trade_date) FROM dailytrade "
    df = pd.read_sql(mysql, conn)
    return df.iloc[0, 0]
