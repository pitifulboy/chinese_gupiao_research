# 导入tushare
import tushare as ts
from sqlalchemy import create_engine

# 初始化pro接口
from get_tushare_token import get_tushare_token


def update_rzrq_rongzirongquan():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')

    mytoken = get_tushare_token()
    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    # 拉取数据
    df = pro.margin_detail(**{
        "trade_date": "",
        "ts_code": "",
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "trade_date",
        "ts_code",
        "rzye",
        "rqye",
        "rzmre",
        "rqyl",
        "rzche",
        "rqchl",
        "rqmcl",
        "rzrqye",
        "name"
    ])
    print(df)
    df.to_sql('rzrq_rongzirongquan', con=conn, if_exists='replace', index=False)
