import pandas as pd
from sqlalchemy import create_engine


def add_share_msg_to_df(trade_df):
    df_msg = select_share_msg()
    x = pd.merge(left=trade_df, right=df_msg, on='ts_code',how='left')
    return x


# 选择一组股票信息
def select_share_msg():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')
    mysql_1 = "SELECT  * FROM share_list"
    df1 = pd.read_sql(mysql_1, conn)

    return df1
