# 导入tushare
import tushare as ts
# 建立mysql数据库的连接
from sqlalchemy import create_engine

from get_tushare_token import get_tushare_token


def update_share_msg_guben():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')

    mytoken = get_tushare_token()

    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    # 拉取数据
    df = pro.bak_basic(**{
        "trade_date": "",
        "ts_code": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "trade_date",
        "ts_code",
        "name",
        "industry",
        "area",
        "float_share",
        "total_share",
        "list_date"
    ])
    print(df)

    df.to_sql('share_msg_guben', con=conn, if_exists='replace', index=False)
