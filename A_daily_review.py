from GAOBIAO import caculate_gaobiao_7_14
from JYE_dapan_zhangting_zhaban import calulate_jiaoyie
from LBTT import oneday_lbtt
from QX_oneday_qingxu import QX_zhibiao
from ZDFB_oneday import draw_zhangdie_fenbu_bar
from ZTFX_dangrizhangtingfenxi import ZTFX_dangri_zhangting_zhaban
from my_time_func import get_today_date
from select_sql_tradedata import select_share_by_date
from update_daily_trade_data import update_trade_data
from update_longhubang import update_longhubang_auto
from update_share_msg import update_share_name_from_tushare

# 跟新数据
update_trade_data()
update_longhubang_auto()
update_share_name_from_tushare()

querydate = get_today_date()
print('日期：' + querydate)
# 生成指定日期涨跌分布
print('计算涨跌分布')
draw_zhangdie_fenbu_bar(querydate)

# 涨跌分布（内含连板数据计算）
print('计算当日涨停炸板数据')
ZTFX_dangri_zhangting_zhaban(querydate)

# 15日资金流
print('计算大盘交易额')
calulate_jiaoyie(querydate, 15)

print('计算情绪指标，内含连板天梯')
QX_zhibiao(select_share_by_date(querydate))

# 高标动态
caculate_gaobiao_7_14()
