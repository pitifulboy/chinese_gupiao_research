from update_daily_trade_data import update_trade_data
from update_longhubang import update_longhubang_auto

# 更新数据：
from update_share_msg import update_share_name_from_tushare

update_longhubang_auto()
update_trade_data()
update_share_name_from_tushare()
