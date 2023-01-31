from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

# 计算单日交易量相关数据
from get_trade_date import get_tradedate_by_enddate_tradedates, get_trade_datelist
from my_time_func import get_my_start_end_date_list
from select_sql_tradedata import select_share_by_date, select_data_by_datelist
from select_sql_zhangting import select_zhangtingban_df_bydf, select_zhaban_df_bydf


def qinxu_jiaoyie_oneday(trade_data_oneday):
    # 交易日的日期
    querday = trade_data_oneday['trade_date'].tolist()[0]

    # 调整数据格式
    df_format_float = trade_data_oneday.astype({'amount': 'float64'}, copy=True)

    # 今日总交易额
    total_df_amount = '% .0f ' % (df_format_float.amount.sum() / 100000)
    # 涨停板
    zhangtingban_df = select_zhangtingban_df_bydf(df_format_float)
    # 涨停个股交易额
    zhangtingban_df_amount = '% .0f ' % (zhangtingban_df.amount.sum() / 100000)
    n_zhangtingban_df = len(zhangtingban_df)

    # 炸板
    zhaban_df = select_zhaban_df_bydf(df_format_float)
    zhaban_df_amount = '% .0f ' % (zhaban_df.amount.sum() / 100000)
    n_zha_df = len(zhaban_df)
    # 日期，大盘交易额，涨停交易额，涨停数，炸板交易额，炸板数
    datalist = [querday, total_df_amount, zhangtingban_df_amount, n_zhangtingban_df, zhaban_df_amount,
                n_zha_df]
    return datalist


# 计算多日交易量相关数据
def days_jiaoyie(endday, day_num):
    # 获取开始的交易日
    start_trade_date = get_tradedate_by_enddate_tradedates(endday, day_num)
    # 获取交易日list
    datelist = get_trade_datelist(start_trade_date, endday)

    # 获取datelist内，所有交易日内的数据
    tradedata_by_datelist_df = select_data_by_datelist(datelist)
    print(datelist)

    # 计算大盘交易额、涨停个股交易额、跌停个股交易额数据。
    data_all = []

    print('交易日，大盘交易额，涨停交易额，涨停数，炸板交易额，炸板数')
    # 倒序查询day_num交易日的数据，用于绘图
    for i in range(0, len(datelist)):
        # 指定日期的交易数据
        trade_data_oneday = tradedata_by_datelist_df[tradedata_by_datelist_df['trade_date'] == datelist[i]]
        # 计算每日交易额数据
        x = qinxu_jiaoyie_oneday(trade_data_oneday)
        data_all.append(x)
        print(x)
    return data_all


# 绘制交易额组合图。大盘交易额+涨停交易额+炸板交易额
def draw_pic_amounts_data(tradedata_list):
    # 获取pyecharts所需数据
    date_list = [x[0] for x in tradedata_list]
    zhangting_amount_list = [x[2] for x in tradedata_list]
    zhaban_amount_list = [x[4] for x in tradedata_list]
    # 大盘交易额
    dapan_amount_list = [x[1] for x in tradedata_list]

    mybar = (
        Bar()
        .add_xaxis(date_list)
        .add_yaxis("涨停交易额", zhangting_amount_list, stack="stack1",
                   itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"), z=0)
        .add_yaxis("炸板交易额", zhaban_amount_list, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"), z=0)
        .extend_axis(yaxis=opts.AxisOpts(is_show=False))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, font_weight='lighter',
                                      color='#000000'))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90, font_size=16)),
            yaxis_opts=opts.AxisOpts(is_show=False),
            title_opts=opts.TitleOpts(
                title=date_list[-1] + "日资金趋势", pos_top='5%',
                title_textstyle_opts=opts.TextStyleOpts(font_size=36),
                pos_left='center', ),
        )
    )

    myLine = (
        Line()
        .add_xaxis(date_list)
        .add_yaxis(
            "大盘交易额",
            dapan_amount_list,
            yaxis_index=1,
        )
        .set_series_opts(
            linestyle_opts=opts.LineStyleOpts(width=4),
            label_opts=opts.LabelOpts(position='top', font_size=24, font_weight='lighter', color='#000000'))
    )
    overlap_bar_line = mybar.overlap(myLine)

    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(overlap_bar_line, grid_opts=opts.GridOpts(pos_bottom='10%', pos_top='10%'), is_control_axis_index=True)
    mygrid.render("jiaoyie.html")

    make_snapshot(snapshot, "jiaoyie.html", date_list[-1] + "交易资金.png", pixel_ratio=2)


def draw_pic_zhangtingzhaban_num_data(tradedata_list):
    # 获取pyecharts所需数据
    date_list = [x[0] for x in tradedata_list]
    zhangting_amount_list = [x[3] for x in tradedata_list]
    zhaban_amount_list = [x[5] for x in tradedata_list]

    mybar = (
        Bar()
        .add_xaxis(date_list)
        .add_yaxis("涨停个数", zhangting_amount_list, stack="stack1",
                   itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"), )
        .add_yaxis("炸板个数", zhaban_amount_list, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, rotate=-90, font_weight='lighter',
                                      color='#000000'))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90, font_size=16)),
            yaxis_opts=opts.AxisOpts(is_show=False),
            title_opts=opts.TitleOpts(title="涨停炸板个数", pos_top='5%',
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=36),
                                      pos_left='center', ),
        )
    )
    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_bottom='10%', pos_top='10%'))
    mygrid.render("zhangdingzhaban_num.html")

    make_snapshot(snapshot, "zhangdingzhaban_num.html", date_list[-1] + "涨停炸板个数.png", pixel_ratio=2)

    return mygrid


def calulate_jiaoyie(enddate, n_trade_days):
    tradedata_list = days_jiaoyie(enddate, n_trade_days - 1)
    draw_pic_amounts_data(tradedata_list)


# 计算：长交易日期周期内，每30天生成一个图片。
def calculate_days_per_n_days(startday, ndays, per_n_days):
    # 计算周期内交易额数据。
    jiaoyie_data = days_jiaoyie(startday, ndays - 1)
    for i in range(ndays - per_n_days + 1):
        # 按照指定周期切片
        data_list = jiaoyie_data[i:i + per_n_days]
        draw_pic_amounts_data(data_list)


# 计算：截止日期为20230121，交易日数量为10。的资金数据
# calulate_jiaoyie('20230121', 10)

# 计算2022年，交易额大盘
# calculate_days_per_n_days(startday='20230101', ndays=290, per_n_days=30)
