#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: sms.py
# Purpose:
#
# Author: 张歆韵(sean.Zhang)
#
# Created: 16-6-13 下午1:30

import logging

import mongfun
import config as cfg
import gmfun

log = logging.getLogger(cfg.g_log)


def get_sms_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_tempdb", "we_sms", is_read_slave)


def send_sms_async(tbl_code, para_map):
    """
    给指定手机发送短消息
    http://dev.wehome.live/post/
    :param mobile:
    :param msg:
    :return:
    """
    para_map['userid'] = cfg.sms_userid
    para_map['account'] = cfg.sms_account
    para_map['password'] = cfg.sms_password
    para_map['action'] = cfg.sms_action

    sms = cfg.buildInfoStrByMap(tbl_code, para_map)
    msg = para_map['mobile'] + ":" + sms
    send_sms_to_tempdb(para_map['mobile'], msg)
    para_map['content'] = sms

    # 测试手机号码用333开头
    if not para_map['mobile'].startswith("333"):
        gmfun.send_only('hy_send_sms', para_map)


def send_sms_to_tempdb(mob, msg):
    tbl_sms = get_sms_tbl()

    doc_sms = dict()
    doc_sms['mobile'] = mob
    doc_sms['sms'] = msg

    tbl_sms.insert_one(doc_sms)


# test use
if __name__ == '__main__':
    para_map = dict()
    para_map['uid'] = 'uAxhzDtKDELs'
    para_map['pas'] = '8dr5pzrm'
    # 接口返回类型：json、xml、txt。默认值为txt
    para_map['type'] = 'json'
    para_map['cid'] = 'xxxxtfSROzW'
    para_map['mobile'] = '13585602556'

    gmfun.send_only('send_sms', para_map)