#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: redisfun.py
# Purpose:
#
# Author: 张歆韵(sean.Zhang)
#
# Created: 16/6/30 下午2:15

import logging
import random
import traceback

from pymongo import DeleteOne, InsertOne

import config as cfg
import const
import gmfun
import mongfun
import pf
import pf_http
from define.comminfo import IpInfo

log = logging.getLogger(cfg.g_log)


def get_sess_info(mysess):
    """
    登录用户的session
    :param userid:
    :return:
    """
    key = "sess:" + mysess
    return cfg.g_redis_conn.get(key)


def remove_sess_info(mysess):
    """
    移除登录信息
    :param mysess:
    :return:
    """
    key = "sess:" + mysess
    cfg.g_redis_conn.delete(key)


def set_sess_info(mysess, json_cont, account="", mysess_lst=[], style=const.LOGIN_INNER):
    """
    登录用户的session的内容设置
    :param style:
    :param mysess_lst:
    :param account:
    :param mysess:
    :param json_cont:
    :return:
    """
    key = "sess:" + mysess
    key2 = "sess_lst:" + account
    if style == const.LOGIN_INNER:
        cfg.g_redis_conn.set(key, json_cont, 7 * 24 * 3600)
    else:
        cfg.g_redis_conn.set(key, json_cont, 24 * 3600)
    if mysess_lst:
        cfg.g_redis_conn.set(key2, mysess_lst, 7 * 24 * 3600)


def set_sess_bbs(userid):
    """
    创建用户后论坛的验证key
    :param style:
    :param mysess_lst:
    :param account:
    :param mysess:
    :param json_cont:
    :return:
    """
    key = "sess:" + str(userid)
    cfg.g_redis_conn.set(key, pf.to_json({"foo": "bar"}), 300)


def get_sms_code(mobile, state):
    """
    获取redis中的短信验证码
    传入的做了abs处理,所以-1肯定无法匹配
    :param mobile:
    :param key:
    :return:
    """
    key = state + ":" + mobile
    code = cfg.g_redis_conn.get(key)
    if code:
        return pf.str2int(code)
    else:
        return -1


def get_sms_times(mobile, state):
    """
    获取redis中的短信发送次数
    传入的做了abs处理,所以-1肯定无法匹配
    :param mobile:
    :param key:
    :return:
    """
    key = state + ":" + mobile + ":times"
    code = cfg.g_redis_conn.get(key)
    if code:
        return pf.str2int(code)
    else:
        return -1


def get_find_pwd_lock(mobile):
    """
    找回密码请勿频繁操作,每天1次!
    传入的做了abs处理,所以-1肯定无法匹配
    :param mobile:
    :param key:
    :return:
    """
    key = "findpwd:" + mobile + ":lock"
    code = cfg.g_redis_conn.get(key)
    if code:
        return True
    else:
        return False


def build_sms_code(mobile, state):
    """
    设置redis中的短信验证码,默认10分钟内有效
    :param mobile:
    :param state:
    :return:
    """
    key = state + ":" + mobile
    code = random.randint(100000, 999999)
    cfg.g_redis_conn.set(key, code, 10 * 60)

    para_map = dict()
    para_map['mobile'] = mobile
    para_map['p1'] = str(code)  # 验证码
    para_map['p2'] = str(10)  # 10分钟

    tbl_code = ''
    if state == "regist":
        tbl_code = 'new_regist_sms'
    elif state == "newmob":
        tbl_code = 'new_mob_sms'
    elif state == "findpwd":
        tbl_code = 'find_pwd_sms'
    elif state == "chgmob":
        tbl_code = 'chg_mob_sms'
        # 找回密码请勿频繁操作,每天1次!
        cfg.g_redis_conn.set(key + ":lock", 1, 24 * 3600)

    elif state == "sendpwd":
        tbl_code = 'send_pwd'
        return tbl_code, para_map

    if cfg.g_redis_conn.exists(key + ":times"):
        times = pf.str2int(cfg.g_redis_conn.get(key + ":times")) + 1
    else:
        times = 1
    cfg.g_redis_conn.set(key + ":times", times, 24 * 3600)

    return tbl_code, para_map


def get_mem_val(uuid):
    """
    从redis的mem:XXX得到数据
    :param key:
    :return:
    """
    key = "mem:" + uuid
    val = cfg.g_redis_conn.get(key)
    if val:
        return pf.json_to_map(val)
    else:
        return None


def set_mem_val(val):
    """
    设置redis mem value, 1小时
    :param val:
    :return:
    """
    uuid = pf.create_uuid_str()
    key = "mem:" + uuid
    cfg.g_redis_conn.set(key, pf.to_json(val), 3600)

    return uuid


def getLoginErrTimes(mobile):
    """
    登录错误次数
    :param mobile:
    :return:
    """
    key = "login:" + mobile
    times = cfg.g_redis_conn.get(key)
    if times:
        return pf.str2int(times)
    else:
        cfg.g_redis_conn.set(key, 0, 300)
        return 0


def incLoginErrTimes(mobile):
    """
    登录密码输错一次,就加1, 5分钟内密码错误5次锁定5分钟
    :param mobile:
    :return:
    """
    key = "login:" + mobile
    cfg.g_redis_conn.incr(key)

    if getLoginErrTimes(mobile) >= 5:
        keylock = "loginlock:" + mobile
        cfg.g_redis_conn.set(keylock, 1, 300)


def isLoginLocked(mobile):
    """
    判定是否被阻止登录
    :param mobile:
    :return:
    """
    keylock = "loginlock:" + mobile
    if cfg.g_redis_conn.get(keylock):
        return True
    else:
        return False


def removeLoginLock(mobile):
    """
    正常登录,解除锁定计数
    :param mobile:
    :return:

    """
    key = "login:" + mobile
    keylock = "loginlock:" + mobile
    cfg.g_redis_conn.delete(key)
    cfg.g_redis_conn.delete(keylock)


def get_userid_length():
    """
    随机分配userid的长度,从200000(6位数)开始分配
    :return:
    """
    key = "id_length"
    id_length = cfg.g_redis_conn.get(key)
    if id_length:
        return pf.str2int(id_length)
    else:
        cfg.g_redis_conn.set(key, 6)
        return 6

def get_invite_code_length():
    """
    随机分配userid的长度,从200000(6位数)开始分配
    :return:
    """
    key = "invite_code_length"
    invite_code_length = cfg.g_redis_conn.get(key)
    if invite_code_length:
        return pf.str2int(invite_code_length)
    else:
        cfg.g_redis_conn.set(key, 4)
        return 4


def incUserIdLength():
    """
    如果有重复,那么随机分配userid的长度+1
    :return:
    """
    key = "id_length"
    cfg.g_redis_conn.incr(key)


def incInviteCodeLength():
    """
    如果有重复,那么随机分配邀请码的长度+1
    :return:
    """
    key = "invite_code_length"
    cfg.g_redis_conn.incr(key)


def get3rdToken():
    """
    从redis的获取第三方聊天平台的token
    :param key:
    :return:
    """
    key = "3rd:token"
    val = cfg.g_redis_conn.get(key)
    if val:
        return pf.json_to_map(val)
    else:
        return None


def set3rdToken(tokenMap, expires):
    """
    设置第三方聊天平台的token
    :param val:
    :return:
    """
    key = "3rd:token"
    cfg.g_redis_conn.set(key, pf.to_json(tokenMap), expires - 100)


def get_pinyin(stxt):
    """
    获取汉字的全拼和简拼
    :param txt:
    :return:
    """
    try:
        lst_a = []  # 全拼
        lst_s = []  # 声母

        tbl_py = mongfun.get_mongo_collection("commdb", "pinyin", const.READ_SLAVE)

        for i in range(0, len(stxt)):
            tmp = stxt[i]
            key = "py:" + tmp
            doc = cfg.g_redis_conn.get(key)
            if doc:
                doc = pf.json_to_map(doc)
            else:
                doc = tbl_py.find_one(tmp)
                if doc:
                    cfg.g_redis_conn.set(key, pf.to_json(doc))

            if doc:
                lst_a.append(doc['a'])
                lst_s.append(doc['s'][0])
            else:
                # 找不到保持原样
                lst_a.append(tmp)
                lst_s.append(tmp)

        return ''.join(lst_a) + ' ' + ''.join(lst_s)
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)
        return ''


def get_ip_info(ip):
    """
    获取ip地址对应的国家,城市信息
    http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=175.45.218.72
    #{"ret":1,"start":-1,"end":-1,"country":"\u97e9\u56fd","province":"Seoul-t'ukpyolsi","city":"Seoul","district":"","isp":"","type":"","desc":""}
    :param txt:
    :return:
    """
    ip_info = IpInfo()

    try:
        if ip:
            key = "ip:" + ip

            ip_info_str = cfg.g_redis_conn.get(key)
            if ip_info_str:
                ip_info.from_json(ip_info_str)
            else:
                # 先到mongodb中找
                tbl_ip = mongfun.get_mongo_collection("commdb", "ipaddr", False)
                doc = tbl_ip.find_one(ip)
                if doc:
                    ip_info_str = pf.to_json(doc)
                    cfg.g_redis_conn.set(key, ip_info_str, 24 * 3600)
                    ip_info.from_json(ip_info_str)
                else:
                    # 调用新浪IP地址查询API接口
                    rtn_map = pf.json_to_map(pf_http.get_url_cont("http://int.dpool.sina.com.cn/iplookup/iplookup.php",
                                                                  {"format": "json", "ip": ip}))
                    if pf.str2int(pf.get_default_val(rtn_map, 'ret', 0)) == 1:
                        ip_info.country = rtn_map['country']
                        ip_info.province = rtn_map['province']
                        ip_info.city = rtn_map['city']

                        # 保存到mongodb和redis中
                        ip_info_str = pf.to_json(ip_info)
                        cfg.g_redis_conn.set(key, ip_info_str, 24 * 3600)

                        # 总是有主键冲突的错误,那就先删除再插入吧
                        doc_ins = pf.json_to_map(ip_info_str)
                        doc_ins['_id'] = ip

                        req_list = list()
                        req_list.append(DeleteOne({"_id": ip}))
                        req_list.append(InsertOne(doc_ins))
                        tbl_ip.bulk_write(req_list)
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)
    finally:
        return ip_info


def clear_user_sch_redis(userid):
    """
    通知或日程有更新的时候清空 userid:schedule:*
    key = "{}:{}:{}-{}".format(userid, "schedule", year, month)
    :param userid:
    :return:
    """
    remove_keys("{}:{}:*".format(userid, "schedule"))


def clear_room_list_count(roomid):
    """
    会议室预定或取消的时候清空 roomid:schedule:*
    key = "{}:{}:{}-{}".format(roomid, "schedule", year, month)
    :param userid:
    :return:
    """
    remove_keys("{}:{}:*".format(roomid, "schedule"))


def get_val(k):
    v = cfg.g_redis_conn.get(k)
    if v:
        return pf.json_to_map(v)
    else:
        return None


def set_val(k, v):
    cfg.g_redis_conn.set(k, pf.to_json(v), 24 * 3600)


def remove_val(k):
    cfg.g_redis_conn.delete(k)


def remove_keys(pattern):
    keys = cfg.g_redis_conn.keys(pattern)
    for k in keys:
        cfg.g_redis_conn.delete(k)


def exists(key):
    result = cfg.g_redis_conn.exists(key)
    return result


def get_fun_translate(fun_name):
    """
    获取接口的翻译,用redis
    :param fun_name:
    :return:
    """
    try:
        key = "log_fun:" + fun_name
        trans_str = cfg.g_redis_conn.get(key)
        if trans_str:
            return trans_str
        else:
            tbl = mongfun.get_mongo_collection("sys_db", "fun_translate", const.READ_SLAVE)
            doc = tbl.find_one(fun_name)
            if doc:
                cfg.g_redis_conn.set(key, doc['zh-cn'], 24 * 3600)
                return doc['zh-cn']
            else:
                # 这样能保证设置后1分钟后生效
                cfg.g_redis_conn.set(key, fun_name, 60)
                return fun_name
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)
        return ''


def get_user_mysess(account):
    """
    随机分配userid的长度,从200000(6位数)开始分配
    :return:
    """
    key = "sess_lst:" + account
    mysees_lst = cfg.g_redis_conn.get(key)
    if mysees_lst:
        return mysees_lst
    else:
        return '[]'


# test use
if __name__ == '__main__':
    print get_fun_translate("pv_ChatListViewController")
