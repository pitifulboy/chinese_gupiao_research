import pandas as pd
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from operator import itemgetter
from add_share_msg import add_share_msg_to_df
from get_trade_date import get_trade_datelist
from my_time_func import get_today_date, get_my_start_end_date_list
# 查询单日连板天梯并作图
from select_sql_tradedata import select_data_by_shareslist_lastdate
from select_sql_zhangting import select_zhangtingban_df


def oneday_lbtt(querydate):
    # 截止日涨停股票list
    ztb_df = select_zhangtingban_df(querydate)

    # 查询当天涨停个股，所有的历史交易数据
    shares_df = select_data_by_shareslist_lastdate(ztb_df.ts_code.to_list(), querydate)

    # 调整数据格式
    df_format_float = shares_df.astype({'close': 'float64', 'pre_close': 'float64'}, copy=True)

    lbtt = []

    # 添加个股信息( #连板数据中如果出现已经退市的个股，退市后股票信息数据缺失。需提前匹配个股数据）

    share_df_full = add_share_msg_to_df(df_format_float)
    # 将名字补充
    share_df_full.name.fillna("已退市", inplace=True)

    # 遍历当日涨停个股，计算其连板数
    for i in range(0, len(ztb_df)):

        df_this_share = share_df_full.loc[share_df_full.ts_code == ztb_df.ts_code.iloc[i]]
        # print(df_this_share)

        # 连板天数
        n = 0
        # 个股交易数据天数
        l = len(df_this_share)

        # 计算个股连板天数
        for j in range(0, l):
            close = '%.2f' % (df_this_share["close"].iloc[-1 - j])
            pre_close = df_this_share["pre_close"].iloc[-1 - j]
            # 涨停价
            up_limit = '%.2f' % (pre_close * 1.1)
            if close == up_limit:
                n = n + 1
            else:
                break

        if n > 1:
            #  【代码+名称，日期，连板天数】
            # print(df_this_share.ts_code.iloc[0])
            # print(df_this_share.name.iloc[0])
            lbtt.append([df_this_share.ts_code.iloc[0] + df_this_share.name.iloc[0], querydate, n])

    lbtt_ordered = sorted(lbtt, key=itemgetter(2), reverse=False)
    # 隐藏 部分代码，名称信息
    # name = [x[0][3:11] for x in lbtt_ordered]
    # 完整显示 代码 和名称
    name = [x[0] for x in lbtt_ordered]
    num = [x[2] for x in lbtt_ordered]

    # 作图
    mybar = (
        Bar()
        .add_xaxis(name)
        .add_yaxis("连板数", num)
        .reversal_axis()
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, font_size=18, color="#000000", position='right'),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=querydate + "连板天梯", pos_top='5%',
                                      pos_left='center', title_textstyle_opts=opts.TextStyleOpts(font_size=36), ),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=18)),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    mygrid = Grid(opts.InitOpts(bg_color='white', width="800px", height="1200px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_left='30%', pos_top='10%'))
    mygrid.render(querydate + "lbtt.html")

    make_snapshot(snapshot, querydate + "lbtt.html", querydate + "_lbtt.png", pixel_ratio=2)

    return lbtt_ordered


# 查询当日连板天梯
def today_lbtt():
    querydate = get_today_date()
    # 生成今日涨跌分布
    oneday_lbtt(querydate)


# 查询多日连板天梯
def date_list_lbtt(startday, enddate):
    t = get_trade_datelist(startday, enddate)
    for i in range(len(t)):
        print(t[i])
        oneday_lbtt(t[i])

# 查询今日连板天梯
# today_lbtt()

# 查询多日连板天梯
# date_list_lbtt('20220101', '20230120')
