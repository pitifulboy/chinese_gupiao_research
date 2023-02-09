# 导入tushare
import tushare as ts
from sqlalchemy import create_engine

# 初始化pro接口
from get_tushare_token import get_tushare_token


# 更新股票的公司信息
def update_ci_company_information():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/chinesemarket', encoding='utf8')

    mytoken = get_tushare_token()
    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    # 拉取数据
    df = pro.stock_company(**{
        "ts_code": "",
        "exchange": "",
        "status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "exchange",
        "reg_capital",
        "setup_date",
        "province",
        "city",
        "employees",
        "ann_date",
        "office",
    ])
    print(df)

    df.to_sql('ci_company_information', con=conn, if_exists='replace', index=False)
