# 导入tushare
import tushare as ts
# 建立mysql数据库的连接
from sqlalchemy import create_engine

from get_tushare_token import get_tushare_token


def update_share_name_from_tushare():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')

    mytoken = get_tushare_token()

    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    # 拉取数据
    df = pro.stock_basic(**{
        "ts_code": "",
        "name": "",
        "exchange": "",
        "market": "",
        "is_hs": "",
        "list_status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "symbol",
        "name",
        "area",
        "industry",
        "market",
        "list_date"
    ])

    # TODO： 将替换replace 改为update，设置ts_code为主键

    df.to_sql('share_list', con=conn, if_exists='replace', index=False)
    print(df)


