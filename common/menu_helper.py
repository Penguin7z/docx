# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from scrapy.selector import Selector


def get_menu_list(html_str):
    """

    :param html_str:
    :return:
    """
    html = html_str
    soup = BeautifulSoup(html, "lxml")
    li_treeview_list = soup.find_all("li", attrs={"class": "treeview"})
    menu_list = []
    for li_treeview in li_treeview_list:
        doc_menu = {}
        a_list = li_treeview.find_all("a")
        for k, a in a_list:
            level = 2
            if k == 1:
                # 一级菜单
                level = 1

            href = a.attrs.get("href", "")
            doc = {
                "_id": menu_id,
                "name": menu_info["name"],
                "desc": menu_info["name"],
                "url": menu_info["url"],
                "class": "",
                "parent_id": str(menu_id),
                "mid": 999,
                "alias": alias,
                "menu_level": 1,
            }
            if href == "#":
                pass
if __name__ == "__main__":
    html_str = """<ul class="sidebar-menu">
                <li class="header"></li>
                <!-- Optionally, you can add icons to the links -->
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-map"></i>
                        <span>基础数据</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/base_data"><i class="fa fa-circle-o"></i>基础数据分析</a></li>
                        <li><a href="/outline/menber_distribution"><i class="fa fa-circle-o"></i>基础数据用户数量</a></li>
                        <li><a href="/outline/menber_login"><i class="fa fa-circle-o"></i>基础数据用户活跃</a></li>
                        <li><a href="/outline/order_outline"><i class="fa fa-circle-o"></i>基础数据订单交易</a></li>
                    </ul>
                    <!--<a href="/base_data"><i class="fa fa-bank"></i><span>基础数据分析</span>
                    </a>-->
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-map"></i>
                        <span>园区数据分析</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/park_data"><i class="fa fa-circle-o"></i>园区基础数据</a></li>
                        <li><a href="/park_data_park"><i class="fa fa-circle-o"></i>园区基础数据园区维度</a></li>
                        <li><a href="/park_sep/park_data_member_distribution"><i class="fa fa-circle-o"></i>园区用户分布</a></li>
                        <li><a href="/park_sep/park_data_member_login"><i class="fa fa-circle-o"></i>园区用户登录</a></li>
                        <li><a href="/park_sep/park_data_order_distribution"><i class="fa fa-circle-o"></i>园区用户订单</a></li>
                        <li><a href="/park_sep/park_com_menber_dis"><i class="fa fa-circle-o"></i>园区企业用户</a></li>
                        <li><a href="/company/all"><i class="fa fa-circle-o"></i>园区企业信息</a></li>
                    </ul>
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-twitter"></i>
                        <span>活动数据分析</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/activity_data"><i class="fa fa-circle-o"></i> 活动数据分析 </a></li>
                        <li><a href="/new_activity_data"><i class="fa fa-circle-o"></i> 活动数据分析（分会员） </a></li>
                    </ul>
                </li>
                <li class="treeview">
                    <a href="/user_detail">
                        <i class="fa fa-twitter"></i>
                        <span>注册用户明细数据</span>
                    </a>
                </li>
                <li class="treeview active">
                    <a href="/bbs_data">
                        <i class="fa fa-twitter"></i>
                        <span>论坛数据分析</span>
                    </a>
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-twitter"></i>
                        <span>订单数据分析</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/order_data"><i class="fa fa-circle-o"></i> 7日订单流水 </a></li>
                        <li><a href="/order_s_data"><i class="fa fa-circle-o"></i> 商户订单报表 </a></li>
                        <li><a href="/order_s_sum"><i class="fa fa-circle-o"></i> 商户订单统计表 </a></li>
                        <li><a href="/order_last_week"><i class="fa fa-circle-o"></i> 上周商户订单报表 </a></li>
                        <li><a href="/order_park_data"><i class="fa fa-circle-o"></i> 园区订单报表 </a></li>
                        <!--<li><a href="/order_distribution"><i class="fa fa-circle-o"></i> 用户订单分布 </a></li>-->
                    </ul>
                </li>

                <li class="treeview">
                    <a href="/search">
                        <i class="fa fa-search"></i>
                        <span>数据检索</span>
                    </a>
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-folder"></i>
                        <span>活动定向分析</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/activity/214"><i class="fa fa-circle-o"></i> 情人节活动 </a></li>
                        <li><a href="/activity/small_game"><i class="fa fa-circle-o"></i> 小游戏推广 </a></li>
                        <li><a href="/activity/coupon_get"><i class="fa fa-circle-o"></i> 抢券活动 </a></li>
                        <li><a href="/activity/happy_gift"><i class="fa fa-circle-o"></i> 欢乐送推广 </a></li>
                        <li><a href="/activity/wehome_set"><i class="fa fa-circle-o"></i> wehome套餐 </a></li>
                        <li><a href="/activity/invite"><i class="fa fa-circle-o"></i> 邀请好友 </a></li>
                        <li><a href="/activity/comunity_beauty"><i class="fa fa-circle-o"></i> 最美社群天使 </a></li>
                    </ul>
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-folder"></i>
                        <span>用户活跃度分析</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/live/week"><i class="fa fa-circle-o"></i> 周活跃度 </a></li>
                        <li><a href="/live/total_view"><i class="fa fa-circle-o"></i> 园区用户总览 </a></li>
                        <li><a href="/live/total_nodobe"><i class="fa fa-circle-o"></i> 园区用户总览（非德必） </a></li>
                        <li><a href="/live/user_leave"><i class="fa fa-circle-o"></i> 月用户留存率 </a></li>
                        <li><a href="/live/user_remain_nodobe"><i class="fa fa-circle-o"></i> 月用户留存率(非德必) </a></li>
                        <li><a href="/live/remain_table"><i class="fa fa-circle-o"></i> 用户留存率 </a></li>
                        <li><a href="/live/remain_table_nodobe"><i class="fa fa-circle-o"></i> 用户留存率(非德必) </a></li>
                        <li><a href="/live/week_percentage"><i class="fa fa-circle-o"></i> 周登录比例分析 </a></li>
                        <li><a href="/live/percentage_nodobe"><i class="fa fa-circle-o"></i> 周登录比例(非德必)分析 </a></li>
                        <li><a href="/live/week_static"><i class="fa fa-circle-o"></i> 周登录人数分析 </a></li>
                        <li><a href="/live/login_times"><i class="fa fa-circle-o"></i> 登录次数分析 </a></li>
                    </ul>
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-folder"></i>
                        <span>会员活跃度分析</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/active_user/day"><i class="fa fa-circle-o"></i> 日活跃度 </a></li>
                        <li><a href="/active_user/week"><i class="fa fa-circle-o"></i> 周活跃度 </a></li>
                        <li><a href="/active_user/month"><i class="fa fa-circle-o"></i> 月活跃度 </a></li>
                        <li><a href="/remain_rate"><i class="fa fa-circle-o"></i> 月留存率 </a></li>
                    </ul>
                </li>
                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-folder"></i>
                        <span>app分析报表</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/app/app_outline"><i class="fa fa-circle-o"></i> app总览 </a></li>
                        <li><a href="/app/app_download"><i class="fa fa-circle-o"></i> app下载渠道统计 </a></li>
                        <li><a href="/app/sep_by_park"><i class="fa fa-circle-o"></i> app各园区使用情况 </a></li>
                        <li><a href="/app/app_user"><i class="fa fa-circle-o"></i> app会员数 </a></li>
                    </ul>
                </li>
                

                
                    <li class="treeview">
                        <a href="#">
                            <i class="fa fa-folder"></i>
                            <span>系统配置</span>
                            <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                        </a>
                        <ul class="treeview-menu">
                            <li><a href="/refresh_db"><i class="fa fa-circle-o"></i> 数据库刷新 </a></li>
                        </ul>
                    </li>
                

                <li class="treeview">
                    <a href="#">
                        <i class="fa fa-folder"></i>
                        <span>权限管理</span>
                        <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>
                    </a>
                    <ul class="treeview-menu">
                        <li><a href="/role/group"><i class="fa fa-circle-o"></i> 权限组管理 </a></li>
                        <li><a href="/role/vector"><i class="fa fa-circle-o"></i> 权限维度管理 </a></li>
                        <li><a href="/role/menu"><i class="fa fa-circle-o"></i> 菜单管理 </a></li>
                        <li><a href="/role/page"><i class="fa fa-circle-o"></i> 界面管理 </a></li>
                        <li><a href="/role/list/999"><i class="fa fa-circle-o"></i> 权限管理 </a></li>
                    </ul>
                </li>

            </ul>"""
    print get_menu_list(html_str)
