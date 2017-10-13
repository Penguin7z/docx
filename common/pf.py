#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: pf.py
# Purpose:
#
# Author: 张歆韵(sean.Zhang)
#
# Created: 16-6-13 下午1:30

import base64
import datetime
import hmac
import random
import re
import string
import time
import ujson
import uuid
from ConfigParser import ConfigParser
from copy import deepcopy

import pytz
import rsa
import xmltodict

import const
from configobj import ConfigObj

utc_0 = int(time.mktime(datetime.datetime(1970, 01, 01).timetuple()))


def getConfig(filename):
    config = ConfigParser()
    config.read(filename)
    return config


def get_utc_millis():
    """
    获取系统从1970-1-1至今的utc毫秒数
    :return:
    """
    return datetime_to_utc_ms(datetime.datetime.utcnow())


def get_unix_curdate():
    """
    获取今天的0点的时间戳
    :return:
    """
    return int(time.mktime(datetime.date.today().timetuple())) * 1000


def date_str2ms(date_str, style='%Y-%m-%d %H:%M:%S'):
    """
    日期str转utc时间戳
    :param date_str:
    :param style:
    :return:
    """
    dt = str_to_datetime(date_str, style=style)
    return datetime_to_utc_ms(dt)


def datetime_to_utc_ms(dt):
    """
    转化为utc的毫秒数
    :param dt:
    :return:
    """
    return int((time.mktime(dt.utctimetuple()) - utc_0) * 1000) + int(dt.microsecond / 1000)


def get_utc_time_from_ms(ms):
    """
    获取国际标准时
    :param ms:
    :return:
    """
    return datetime.datetime.utcfromtimestamp(int(ms) / 1000)


def get_china_time_from_ms(ms):
    """
    获取中国时间
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000.0, pytz.timezone('Asia/Shanghai'))


def get_datetime_by_ms_timezone(ms, tzstr):
    """
    获取中国时间
    :param ms: UTC毫秒数
    :param tzstr 字符串: Asia/Shanghai  US/Eastern
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000.0, pytz.timezone(tzstr))


def get_datetime_ymd(dt):
    """
    获取年月日的整数值
    :param dt:
    :return:
    """
    year = dt.year
    month = dt.month
    day = dt.day
    return year, month, day


def get_datetime_str(dt, style="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(style)


def get_datetime_str_with_ms(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:23]


def str_to_datetime(str_date, style='%Y-%m-%d %H:%M:%S', tzstr='Asia/Shanghai'):
    """
    style:格式字符串是python的标准日期格式码，例如：
        %Y-%m-%d %H:%M:%S
        %Y-%m-%d
    """
    dt = datetime.datetime.strptime(str_date, style)
    dt = pytz.timezone(tzstr).localize(dt)
    return dt


def del_http_headers(rcv_map):
    """
    去除rcv中通用的http头
    :param rcv_map:
    :return:
    """
    del_map_safe(rcv_map, "mysess")
    del_map_safe(rcv_map, "seqnum")
    del_map_safe(rcv_map, "user_ip")
    del_map_safe(rcv_map, "user_agent")
    del_map_safe(rcv_map, "web_st")
    del_map_safe(rcv_map, "role")
    del_map_safe(rcv_map, "style")
    del_map_safe(rcv_map, "sort")
    del_map_safe(rcv_map, "page_size")
    del_map_safe(rcv_map, "s")
    del_map_safe(rcv_map, "keywords")


def del_map_safe(doc, field):
    """
    安全删除map字段
    :param doc:
    :param field:
    :return:
    """
    if is_has_val(doc, field, const.MAP_HAS_KEY):
        del doc[field]


def get_hy_account(role, userid):
    """
    获取会员帐号
    :param role:
    :param userid:
    :return:
    """
    return "{}_{}".format(role, userid)


def get_hy_relation_id(userid, rid):
    """
    获取会员帐号
    :param role:
    :param userid:
    :return:
    """
    return "{}_{}".format(userid, rid)


def isEmail(mail):
    """
    是否是邮件地址
    :param mail:
    :return:
    """
    if re.search(r'[\w.-]+@[\w.-]+.\w+', mail):
        return True
    else:
        return False


def isString(val):
    """
    是否是字符串
    :param val:
    :return:
    """
    if isinstance(val, (str, unicode)):
        return True
    else:
        return False


def isNumberAndAlpha(txt):
    """
    判定字符串是否在 [0-9][a-z]
    :param txt:
    :return:
    """
    if re.match('^[0-9a-z]+$', txt.lower()):
        return True
    else:
        return False


def check_array_str(arrayStr):
    """
    判断字符串是否为list对象
    :param arrayStr:
    :return:
    """
    r = re.compile(r'^\[\s*((\d+)\s*\,??\s*)+?\]$')
    return r.match(arrayStr)


def str2int(value):
    """
    转换为整数
    :param value:
    :return:
    """
    try:
        return int(float(value))
    except Exception as e:
        print e
        return 0


def removeHCandHH(txt):
    """
    去掉回车换行符
    :param txt:
    :return:
    """
    txt = txt.replace('\r', '')
    txt = txt.replace('\n', '')
    return txt


def get_mobile_num_11(mobile, role=""):
    """
    获取手机号码的后11位,如果是个邮件地址,就返回邮件地址
    :param role:
    :param mobile:
    :return:
    """
    # 如果登陆的是m用户mobile就是用户的帐号
    if role == const.USER_ROLE_M:
        return mobile
    # 其实是个email
    if isEmail(mobile):
        return None
    else:
        # 去掉所有的非数字
        new_lst = list()
        for char in list(mobile):
            if char.isdigit():
                new_lst.append(char)
        new_txt = "".join(new_lst)

        if len(new_txt) < 11:
            # 小于11位不是合法的手机号码
            return None
        else:
            idx = len(new_txt) - 11
            idx = max(idx, 0)
            return new_txt[idx:]


def to_json(doc):
    """
    转换成utf-8的json字符串
    :param doc:
    :return:
    """
    return ujson.dumps(doc, ensure_ascii=False)


def json_to_map(json):
    """
    把json字符串转化为obj
    :param json:
    :return:
    """
    if isinstance(json, (str, unicode)):
        if json:
            return ujson.loads(json)
        else:
            return dict()
    else:
        return json


def buildErrJson(errcode, seq, errmsg, ip=''):
    """
    构造用于错误返回的json
    :param msg:
    :return:
    """
    map = dict()
    map['ip'] = ip
    map['seqnum'] = seq
    map['msg'] = errmsg
    map['status'] = errcode

    return to_json(map)


def build_filter_map(rcv):
    """
    构造过滤条件map
    :param rcv:
    :return:
    """
    flt_map = dict()
    for k in rcv.keys():
        if k.startswith("flt_"):
            if rcv[k]:
                tmp = rcv[k].split(":")
                if tmp[1].isnumeric():
                    flt_map[str(tmp[0])] = str2int(tmp[1])
                else:
                    flt_map[str(tmp[0])] = tmp[1]

    return flt_map


def build_filter_list(rcv):
    """
    构造过滤条件list
    :param rcv:
    :return:
    """
    flt_map = build_filter_map(rcv)
    flt_list = list()
    for k, v in flt_map.items():
        flt_list.append({"term": {k: v}})

    return flt_list


def get_log_info(fun, seqnum):
    """
    获取函数执行信息
    :param fun:
    :param seqnum:
    :return:
    """
    now = get_utc_millis()
    return u"{}:worker: begin {} ......:{}".format(get_datetime_str(get_china_time_from_ms(seqnum)),
                                                   fun, str2int(now) - str2int(seqnum))


def str_sha(vs):
    """
    计算输入字符串的sha后的base64编码
    :param vs:
    :return:
    """
    sec_key = b"mb*we0pgn!z!z9t&ftet%w3npri3fci%mlxiy5*!q94q-3v7tz"
    h = hmac.new(sec_key)
    if isinstance(vs, str):
        h.update(vs)
    else:
        h.update(vs.encode('ascii', 'xmlcharrefreplace'))
    return base64.urlsafe_b64encode(h.digest())


def parse_query(qry_str):
    """
    解析查询字符串
    :param qry_str:
    :return:
    """
    style = const.ES_QRY_NO_FIELDS
    qry_list = qry_str.split(' ')
    new_list = list()
    for qry in qry_list:
        if ":" in qry:
            # 指定了搜索字段
            style = const.ES_QRY_WITH_FIELDS
            tmp = qry.split(":")
            if isNumberAndAlpha(tmp[1]):
                # 数字的搜索用模糊方式
                new_list.append("{}:*{}*".format(tmp[0], tmp[1]))
            else:
                new_list.append(qry)
        else:
            if isNumberAndAlpha(qry):
                # 数字的搜索用模糊方式
                new_list.append("*{}*".format(qry))
            else:
                new_list.append(qry)

    return style, " ".join(new_list)


def deSSLPass(pass_in):
    """
    解密
    :param pass_in: rsa public key加密后的base64编码
    """
    try:
        privkey = rsa.PrivateKey.load_pkcs1(bytes(const.SSL_KEY_PRI))
        p1 = base64.decodestring(pass_in)

        return rsa.decrypt(p1, privkey)
    except Exception as e:
        print e
        return '==A7U9n3MZR@vxia@RPlC@cxh@J8NSYfrEw=='


def enSSLPass(msg):
    """
    加密
    """
    try:
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(bytes(const.SSL_KEY_PUB))
        return base64.encodestring(rsa.encrypt(msg, pubkey))
    except Exception as e:
        print e
        return '==enSSLPass==error=='


def base64ToFile(fn, cont):
    """
    base64字符串转为二进制文件流,写到tmp目录
    :param cont:
    :return:
    """
    fname = "/tmp/" + fn
    g = open(fname, "w")
    g.write(base64.decodestring(cont))
    g.close()
    return fname


def fileToBase64(filename):
    """
    二进制文件流转换为base64
    :param cont:
    :return:
    """
    with open(filename, "rb") as bin_file:
        return base64.encodestring(bin_file.read())


def create_random_str(num):
    """
    创建指定个数的随机字符串
    :param num:
    :return:
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(num))


def create_uuid_str():
    return str(uuid.uuid4())


def is_has_val(doc, field, style):
    """
    :param doc: map or mongodb doc
    :param field: 需要判断对应字段是否存在
    :param style:
    """
    if doc:
        if style == const.MAP_HAS_KEY:
            if field in doc:
                return True
            else:
                return False
        else:
            if (field in doc) and doc[field]:
                return True
            else:
                return False
    else:
        return False


def get_default_val(doc, field, default):
    """
    从dict从取指定field的值,如果没有,返回 default 的值
    """
    if isinstance(doc, dict):
        if is_has_val(doc, field, const.MAP_HAS_KEY_AND_VAL):
            return doc[field]
        else:
            return default
    else:
        return default


def get_vip_lv_by_g2(g2_num):
    """
    获取VIP等级
    :param g2_num:
    :return:
    """
    if g2_num <= const.VIP_LV_LIST[0]:
        return 1

    lv_len = len(const.VIP_LV_LIST)
    lv_reverse = deepcopy(const.VIP_LV_LIST)
    lv_reverse.reverse()

    for lv, num in enumerate(lv_reverse):
        if g2_num > num:
            break

    return lv_len - lv


def obj2dict(obj):
    """
    class 属性转化为字典
    :param obj:
    :return:
    """
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


def add_int_to_list_rm_exist(val, lst):
    """
    去重加入list
    :param val:
    :param lst:
    :return:
    """
    if val:
        itmp = str2int(val)
        if itmp not in lst:
            lst.append(itmp)


def add_str_to_list_rm_exist(val, lst):
    """
    去重加入list
    :param val:
    :param lst:
    :return:
    """
    if val:
        stmp = str(val).strip()
        if stmp not in lst:
            lst.append(stmp)


def check_time_conflict(st1, et1, st2, et2):
    """
    检测时间冲突
    :param st1:
    :param et1:
    :param st2:
    :param et2:
    :return:
    """
    # 1.尾部冲突
    if st1 < et2 <= et1:
        return True
    # 2.头部冲突
    if st1 <= st2 < et1:
        return True
    # 3. 2包含1
    if st2 <= st1 and et2 >= et1:
        return True

    return False


def parse_xml_dict(xml_cont):
    """
    把xml内容转换为字典对象
    :param xml_cont:
    :return:
    """
    return xmltodict.parse(xml_cont)


def conf_to_obj(filename):
    """
    读取配置文件返回obj对象
    :return:
    """
    config = ConfigObj(filename)
    return config


# test use
if __name__ == '__main__':
    # print str2int(float('3'))
    mysess = "b259a903-05ef-4406-b203-ac92ddeb640d"
    auth_str = base64.encodestring("{}:{}".format(get_utc_millis(), mysess))
    print "Basic {}".format(auth_str)
    print base64.decodestring(auth_str)
    print datetime_to_utc_ms(str_to_datetime('2016-09-18 11:00:00'))
    print datetime_to_utc_ms(str_to_datetime('2016-09-18 14:00:00'))

    print "========"
    print get_china_time_from_ms(1461147000558)
    print get_china_time_from_ms(1461147007171)

    tmp_t1 = get_utc_millis()
    print tmp_t1
    # print datetime_to_utc_ms(str_to_datetime('2015-07-27 11:00:00'))
    #
    print get_china_time_from_ms(tmp_t1)
    tt1 = get_datetime_by_ms_timezone(tmp_t1, "Asia/Shanghai")
    tt2 = get_datetime_by_ms_timezone(tmp_t1, "US/Eastern")
    tt3 = get_datetime_by_ms_timezone(tmp_t1, "Pacific/Honolulu")

    dl1 = tt1 - tt2
    dl2 = tt1 - tt3

    print get_datetime_ymd(get_datetime_by_ms_timezone(tmp_t1, "Asia/Shanghai"))
    print get_datetime_ymd(get_datetime_by_ms_timezone(tmp_t1, "Pacific/Honolulu"))
    print get_datetime_ymd(get_datetime_by_ms_timezone(tmp_t1, "UTC"))
