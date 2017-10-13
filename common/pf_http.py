#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: pf_http.py
# Purpose:
#
# Author: 张歆韵(sean.Zhang)
#
# Created: 16/6/30 下午2:15

import logging
import traceback

import requests
from requests import RequestException

import config as cfg
import gmfun

log = logging.getLogger(cfg.g_log)


def get_url_cont(url, para_map, encoding=None):
    """
    获取url内容
    :param url:
    :param para_map:
    :param encoding: http返回数据的编码
    :return:
    """
    try:
        res = requests.get(url, params=para_map)
        if res.status_code == requests.codes.ok:
            if encoding:
                res.encoding = encoding
            return res.text
        else:
            return ""
    except RequestException:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)
        return ""


def http_post(url, para_map):
    """
    post 递交数据
    :param url:
    :param para_map:
    :return:
    """
    try:
        res = requests.post(url, para_map)
        if res.status_code == requests.codes.ok:
            return res.text
        else:
            return ""
    except RequestException:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)
        return ""


def http_download(url, file_path):
    """
    下载网络文件
    :param url:
    :param file_path:
    :return:
    """
    try:
        res = requests.get(url)
        with open(file_path, "wb") as out_file:
            out_file.write(res.content)

    except RequestException:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)

# test use
if __name__ == '__main__':
    # test get
    import pf

    my_map = pf.json_to_map(get_url_cont("http://int.dpool.sina.com.cn/iplookup/iplookup.php",
                                         {"format": "json", "ip": "116.235.8.20"}))
    print my_map

    http_download("http://wx.qlogo.cn/mmopen/3BlHe3SEgyOlDr2A6tdoOHX1JG6co7Ib5zamdicjLTfALkibicBQTxEC7xQENnFiax6AIrrREg7StudynELeUZaXq5ib0PpIkT6TK/0", "/tmp/aaa.jpg")

    # # test post
    # sms_map = dict()
    # sms_map['uid'] = 'uAxhzDtKDELs'
    # sms_map['pas'] = '8dr5pzrm'
    # sms_map['type'] = 'json'
    # sms_map['cid'] = '4r9WEtfSROzW'
    # sms_map['mob'] = '13585602556'
    # sms_map['p1'] = u"胡海红"
    #
    # # my_text = http_post("http://api.weimi.cc/2/sms/send.html", sms_map)
    # # my_map =pf.fromJSON(my_text)
    # # print  my_map
    #
    # push_map = dict()
    # push_map['title'] = u'会议'
    # push_map['msg'] = u'调整了"研讨会"的时间地点,请重新确认!'
    # push_map['extra'] = {'type': 'meet', 'id': 'xxx123'}
    # # push_map['userid'] = "122921847"
    # push_map['sender'] = u"令狐冲"
    #
    # gmfun.send_only("push_msg", push_map)
