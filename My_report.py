# 将多个图表在同一个网页展示
from GAOBIAO import caculate_ndays_zhangfu
from LBTT import draw_lbtt
from QX_oneday_qingxu import QX_zhibiao
from ZDFB_oneday import oneday_zhangdie_fenbu, draw_zhangdie_fenbu_bar
from ZJQS_dp_zt_zb import calulate_jiaoyie
from ZJQS_zijinqushi_by_liuzhi import one_day_bankuai_liuzhi_fenxi
from add_share_shizhi import one_day_zhangting_table
from my_time_func import get_today_date
from pyecharts.charts import Bar, Grid, Page, Tab
from pyecharts import options as opts



querydate = get_today_date()



def page_simple_layout():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        # 资金趋势
        calulate_jiaoyie(querydate, 15),
        # 计算涨跌分布
        draw_zhangdie_fenbu_bar(querydate),
        # 绘制连板天梯
        draw_lbtt(querydate),
        # 涨停信息
        one_day_zhangting_table(querydate, '涨停'),
        # 炸板信息
        one_day_zhangting_table(querydate, '炸板'),
        # 跌停信息
        one_day_zhangting_table(querydate, '跌停'),
        # 板块分析透视
        one_day_bankuai_liuzhi_fenxi(querydate),
        # 7日高标，top20
        caculate_ndays_zhangfu(querydate, 7)

    )
    page.render(querydate + "my_report.html")


def tab_layout():
    tab = Tab()

    tab.add(calulate_jiaoyie(querydate, 15), "大盘数据")
    tab.add(draw_zhangdie_fenbu_bar(querydate), "板块数据")
    tab.add(draw_lbtt(querydate), "连板数据")
    tab.add(draw_lbtt(querydate), "首板数据")

    tab.render("tab_base.html")


if __name__ == "__main__":
    # update数据
    page_simple_layout()
    # QX_zhibiao()
    tab_layout()
