#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: util_file.py
# Purpose: PyCharm
#
# Author: 企鹅(simon.dong)
#
# Created: 2017/8/2 下午3:51


import os


def get_file_list_from_directories(directories_path, ext="", re_name=""):
    """
    获取目录下所有文件列表
    :param directories_path:
    :param ext:
    :param re_name:
    :return:
    """
    file_list = os.listdir(directories_path)
    return_list = []
    for file_item in file_list:
        if ext and not file_item.endswith(".{}".format(ext)):
            continue
        if re_name and re_name not in file_item:
            continue

        file_path = "{}/{}".format(directories_path, file_item)
        return_list.append(file_path)

    return return_list


def get_file_content(file_path, re_name=""):
    """
    获取文件内容
    :param file_path:
    :param re_name:
    :return:
    """
    if not file_path:
        return []
    with open(file_path) as fp:
        lines = fp.read().split("\n")

    if not re_name:
        return lines
    line_list = []
    for line in lines:
        if re_name and re_name not in line:
            continue
        line_list.append(line)
    return line_list


def gen_group_sep_url():
    """
    生成url映射界面名称列表
    :return:
    """
    return {
        "ICF首页": "/static/activity/icf/index.html",
        "关于主题": "/static/activity/icf/about.html",
        "活动议程": "/static/activity/icf/activity.html",
        "我的报名": "/static/activity/icf/mine.html",
        "关于ICF": "/static/activity/icf/about_icf.html",
        "国际创交汇": "",
        "大学生创业": "/static/activity/icf/life_geek.html",
        "支持伙伴": "/static/activity/icf/partner.html",
        "直播回放": "",
        "问与答": "/static/activity/icf/qa.html",
        "banner1": "/hd?icf_id=851577&icf_type=1",
        "banner2": "/hd?icf_id=832109&icf_type=1",
        "banner3": "/index?page=icf",
    }


if __name__ == "__main__":
    pass
    # dic_topic_count = {}
    # url_list = gen_group_sep_url()
    # for topic, url in url_list.iteritems():
    #     dic_topic_count[topic] = dic_topic_count.get(topic, 0)
    director = "/Users/e/Documents/wehome_log"
    file_list = get_file_list_from_directories(director, ext="log", re_name="")
    dic_topic_count = {}
    for file_item in file_list:
        url_list = gen_group_sep_url()
        for topic, url in url_list.iteritems():
            if not url:
                continue
            lines = get_file_content(file_item, re_name=url)
            dic_topic_count[topic] = dic_topic_count.get(topic, 0) + len(lines)

    for topic, value in dic_topic_count.iteritems():
        print "{}: {}".format(topic, value)



