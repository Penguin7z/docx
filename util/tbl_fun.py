#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: tbl_fun.py
# Purpose: PyCharm
#
# Author: 董佳佳(simon.Dong)
#
# Created: 16/12/9 上午00:22

from common import mongfun


def get_xxx_xxx_xxx_tbl(db_name, collection_name, is_read_slave=False):
    return mongfun.get_mongo_collection(db_name, collection_name,
                                        is_read_slave)


def get_activity_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db", "activity",
                                        is_read_slave)


def get_activity_share_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "activity",
                                        is_read_slave)


def get_activity_canal_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db", "activity_canal_log",
                                        is_read_slave)


def get_activity_join_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db", "activity_join",
                                        is_read_slave)


def get_activity_gift_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db", "activity_gift",
                                        is_read_slave)


def get_activity_gift_people_for_guess_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db",
                                        "activity_gift_people_for_guess",
                                        is_read_slave)


def get_activity_s_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db", "activity_s",
                                        is_read_slave)


def get_activity_s_bind_c_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_activity_db", "activity_s_bind_c",
                                        is_read_slave)


def get_activity_s_yh_use_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_activity_db',
                                        'activity_s_yh_use_log', is_read_slave)


def get_order_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_pay_db", "order", is_read_slave)


def get_fw_car_ser_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "car_ser",
                                        is_read_slave)


def get_cd_mt_ser_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "meetingroom_ser",
                                        is_read_slave)


def get_station_ser_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "station_ser",
                                        is_read_slave)


def get_on_sale_ser_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "on_sale_ser",
                                        is_read_slave)


def get_cy_catering_ser_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "catering_ser",
                                        is_read_slave)


def get_service_all_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "service_all",
                                        is_read_slave)


def get_user_c_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_c", is_read_slave)


def get_user_b_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_b", is_read_slave)


def get_user_s_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_s", is_read_slave)


def get_user_login_c_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "login_c", is_read_slave)


def get_user_relationship_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_relationship",
                                        is_read_slave)


def get_park_info_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "park_info",
                                        is_read_slave)


# 测试用户
def get_user_test_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_test_db", "user_test",
                                        is_read_slave)


def get_api_call_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_log_db", "api_call_log",
                                        is_read_slave)


def get_entry_action_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_log_db", "entry_action_log",
                                        is_read_slave)


def get_user_active_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_log_db", "user_active_log",
                                        is_read_slave)


def get_active_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_log_db", "active_log",
                                        is_read_slave)


def get_order_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_log_db", "order_log",
                                        is_read_slave)


def get_bi_base_data_by_park_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db",
                                        "bi_base_data_by_park", is_read_slave)


def get_bbs_post_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bbs_db", "post", is_read_slave)


def get_bbs_plate_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bbs_db", "plate", is_read_slave)


def get_bbs_like_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bbs_db", "ilike", is_read_slave)


def get_bbs_reply_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bbs_db", "reply", is_read_slave)


def get_bbs_user_follow_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bbs_db", "user_follow",
                                        is_read_slave)


def get_we_chat_follow_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "wechat_follow",
                                        is_read_slave)


def get_bi_base_data_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "bi_base_data",
                                        is_read_slave)


def get_bi_bbs_data_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "bi_bbs_data",
                                        is_read_slave)


def get_bi_park_data_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "bi_park_data",
                                        is_read_slave)


def get_bi_wx_follow_data_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "bi_wx_follow_data",
                                        is_read_slave)


def get_bi_refresh_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "bi_refresh_log",
                                        is_read_slave)


def get_db_refresh_log_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_sys_config_db", "db_refresh_log",
                                        is_read_slave)


def get_park_data_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "bi_park_data_temp",
                                        is_read_slave)


def get_bi_park_data_park_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db",
                                        "bi_park_data_park_temp",
                                        is_read_slave)


def get_item_set_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_service_db", "item_set",
                                        is_read_slave)


def get_remain_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_bi_local_db", "remain_temp",
                                        is_read_slave)


def get_remain_table_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'remain_table_temp',
                                        is_read_slave)


def get_remained_nodobe_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'remained_nodobe_temp', is_read_slave)


def get_remain_table_nodobe_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'remain_table_nodobe', is_read_slave)


def get_activity_week_cnt1_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_cnt1_temp',
                                        is_read_slave)


def get_activity_week_cnt2_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_cnt2_temp',
                                        is_read_slave)


def get_activity_week_no_pay_cnt1_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_no_pay_cnt1_temp',
                                        is_read_slave)


def get_activity_week_no_pay_cnt2_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_no_pay_cnt2_temp',
                                        is_read_slave)


def get_activity_week_pct1_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_pct1_temp',
                                        is_read_slave)


def get_activity_week_pct2_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_pct2_temp',
                                        is_read_slave)


def get_activity_week_no_pay_pct1_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_no_pay_pct1_temp',
                                        is_read_slave)


def get_activity_week_no_pay_pct2_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_no_pay_pct2_temp',
                                        is_read_slave)


def get_login_week_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'login_week_temp',
                                        is_read_slave)


def get_new_activity_fun_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'new_activity_fun_temp', is_read_slave)


def get_last_week_order_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'last_week_order_temp', is_read_slave)


def get_app_ouline_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'app_ouline_temp',
                                        is_read_slave)


def get_app_sep_by_park_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'app_sep_by_park_temp', is_read_slave)


def get_xyx_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'xyx_temp',
                                        is_read_slave)


def get_happy_gift_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'happy_gift',
                                        is_read_slave)


def get_coupon_get_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'coupon_get',
                                        is_read_slave)


def get_package_analysis_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'package_analysis_temp', is_read_slave)


def get_activity_week_pct1_nodobe_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'activity_week_pct1_nodobe_temp',
                                        is_read_slave)


def get_happy_gift_new_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'happy_gift_new_temp', is_read_slave)


def get_get_user_info_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'get_user_info',
                                        is_read_slave)


def get_men_dist_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'men_dist_temp',
                                        is_read_slave)


def get_park_menber_dis_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'park_menber_dis_temp', is_read_slave)


def get_menber_login_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'menber_login_temp',
                                        is_read_slave)


def get_order_outline_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db', 'order_outline_temp',
                                        is_read_slave)


def get_activity_angel_votes_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_activity_db',
                                        'activity_angel_votes', is_read_slave)


def get_menber_login_park_temp_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_bi_local_db',
                                        'menber_login_park_temp',
                                        is_read_slave)


def get_icf_plate_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_icf_db", "icf_plate",
                                        is_read_slave)


def get_icf_section_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_icf_db", "icf_section",
                                        is_read_slave)


def get_icf_node_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_icf_db", "icf_node", is_read_slave)


def get_icf_join_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_icf_db", "icf_join", is_read_slave)


def get_icf_archive_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_icf_db", "icf_archive",
                                        is_read_slave)


def get_am_admin_group_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_am_admin_db", "am_admin_group",
                                        is_read_slave)


def get_am_role_vector_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_am_admin_db", "am_role_vector",
                                        is_read_slave)


def get_am_role_vector_detail_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_am_admin_db",
                                        "am_role_vector_detail",
                                        is_read_slave)


def get_am_user_role_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_am_admin_db", "am_user_role",
                                        is_read_slave)


def get_am_group_role_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_am_admin_db", "am_group_role",
                                        is_read_slave)


def get_am_user_role_basic_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_am_admin_db",
                                        "am_user_role_basic",
                                        is_read_slave)


def get_am_menu_tbl(is_read_slave=False):






    return mongfun.get_mongo_collection("we_am_admin_db", "am_menu",
                                        is_read_slave)


def get_sl_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_shortlink_db", "shortlink",
                                        is_read_slave)


if __name__ == '__main__':
    pass
