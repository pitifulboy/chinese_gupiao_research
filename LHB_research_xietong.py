# 协同营业部研究
from my_time_func import get_my_start_end_date_list
import pandas as pd
from select_sql_lhb import select_days_longhubang


def lhb_xietong(my_datelist):
    # 查询龙虎榜信息
    lhb_data = select_days_longhubang(my_datelist)

    # 数据预处理。筛选买入席位，保留交易日期，代码，席位字段。
    lhb_data_handled = lhb_data.loc[lambda lhb_data: lhb_data['side'] == '0', 'trade_date':'exalter']

    # 数据去重
    lhb_data_handled_drop = lhb_data_handled.drop_duplicates()

    # 计算协同关系
    df_xietong = pd.merge(lhb_data_handled_drop, lhb_data_handled_drop, how='outer', on=['trade_date', 'ts_code'])

    # 删除席位自匹配数据。
    df_xietong_drop = df_xietong.drop(df_xietong[df_xietong['exalter_x'] == df_xietong['exalter_y']].index)
    print(df_xietong_drop)

    # 导出结果
    path = r'D:\00 量化交易\\' + my_datelist[0] + '-' + my_datelist[-1] + '席位协同关系' + '.xlsx'
    df_xietong_drop.to_excel(path, sheet_name='协同明细', engine='openpyxl')


# 选定日期段
my_datelist = get_my_start_end_date_list('20221012', '20230112')
# 计算席位协同关系
lhb_xietong(my_datelist)
