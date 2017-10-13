#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: userfun.py
# Purpose:
#
# Author: 张歆韵(sean.Zhang)
#
# Created: 16/6/30 下午2:15

import logging
import os
import random
import traceback
from random import choice
import string

from pymongo import UpdateOne

import ujson
import config as cfg
from common import redisfun, mongfun, pf, sms, const, pf_http, gmfun
from define.resinfo import ResBase
from define.userinfo import UserSessInfo, UserSimple, UserPhone, UserListInfo, FriendInfo

log = logging.getLogger(cfg.g_log)


def create_random_id_by_length(length):
    """
    开发环境dev(20000-99999)
    生产环境prd(>=200000, 从6位数开始分配,避开所有1开头的,防止手机号冲突)
    :param length: id的长度
    :return:
    """
    # 生产环境
    if cfg.g_prd:
        num_s = int("2".ljust(length, "0"))
        num_e = int("9".ljust(length, "9"))
        return random.randint(num_s, num_e)
    # 开发环境
    else:
        return random.randint(20000, 99999)


def create_union_userid(role):
    """
    创建唯一的userid,不允许重复,至少2次找不到才加长度,否则升的太快
    :return:
    """
    tbl_user = get_user_tbl(role)

    # 生成一个userid,不允许重复,至少2次找不到才加长度,否则升的太快
    find_num = 0
    id_length = redisfun.get_userid_length()

    userid = create_random_id_by_length(id_length)
    while tbl_user.find_one(userid):
        find_num += 1
        if find_num >= 2:
            redisfun.incUserIdLength()
            id_length = redisfun.get_userid_length()
        userid = create_random_id_by_length(id_length)

    return userid


def create_invite_code():
    """
    创建唯一的邀请码,和uid类似,从4位开始,至少2次找不到才加长长度
    :return:
    """
    tbl_invite = get_invite_tbl()

    # 生成一个invite_code,不重复
    find_num = 0
    invite_code_length = redisfun.get_invite_code_length()

    invite_code = create_random_id_by_length(invite_code_length)
    while tbl_invite.find_one(invite_code):
        find_num += 1
        if find_num >= 2:
            redisfun.incInviteCodeLength()
            invite_code_length = redisfun.get_invite_code_length()
        invite_code = create_random_id_by_length(invite_code_length)

    return invite_code


def create_pwd(length=8, chars=const.PWD_RANGE):
    """
    创建密码,默认8位
    :return:
    """
    return ''.join([choice(chars) for i in range(length)])


def get_random_user_head_img():
    """
    无用户头像的用户返回随机头像
    :return:
    """
    return "uhead_{}.png".format(random.randint(1, 8))


def get_user_sess_info(mysess):
    """
    从redis中缓存中加载mesess对应的登录用户信息
    :param mysess:
    :return:
    """
    usi = UserSessInfo()
    usi.json_to_obj(redisfun.get_sess_info(mysess))

    return usi


def get_user_tbl(role, is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_%s" % role, is_read_slave)


def get_user_extra_tbl(role,is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_extra_%s" % role, is_read_slave)


def get_user_gold_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_gold", is_read_slave)


def get_login_tbl(role, is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "login_%s" % role, is_read_slave)


def get_user_role(role, is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_role_%s" % role, is_read_slave)


def get_friend_app_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "friend_app", is_read_slave)


def get_user_friends_tbl(is_read_slave=False):
    pass


def get_user_relationship_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_relationship", is_read_slave)


def get_user_local_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "local_info", is_read_slave)


def get_park_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "park_info", is_read_slave)


def get_invite_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('we_user_db', 'invite_code', is_read_slave)


def get_announcement_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection("we_user_db", "user_announcement", is_read_slave)


def get_advise_tbl(is_read_slave=False):
    return mongfun.get_mongo_collection('tempdb', 'advise', is_read_slave)


def getBopsRoleTbl():
    return mongfun.get_mongo_conn()['userdb']['bops_role']


def getViewPowerTbl():
    return mongfun.get_mongo_conn()['userdb']['view_power']


def get_notice_doc(notice_id):
    """
    通知信息中的
    :param notice_id: string类型
    :return:
    """
    tbl = get_announcement_tbl(const.READ_SLAVE)
    return tbl.find_one(mongfun.to_mongo_id(notice_id))


def get_user_doc(userid, role, fileds=[], method=mongfun.READ_PRIMARY):
    """
    获取指定用户的个人信息部分
    :param role:
    :param userid:
    :param fileds:
    :param method:
    :return:
    """
    if method == mongfun.READ_SLAVE:
        tbl = get_user_tbl(role, const.READ_SLAVE)
    else:
        tbl = get_user_tbl(role)

    if len(fileds) == 0:
        return tbl.find_one(userid)
    else:
        return tbl.find_one(userid, fileds)


def get_user_extra_doc(userid, role, fileds=[], method=mongfun.READ_PRIMARY):
    """
    获取指定用户的额外信息
    :param role:
    :param userid:
    :param fileds:
    :param method:
    :return:
    """
    if method == mongfun.READ_SLAVE:
        tbl = get_user_extra_tbl(role, const.READ_SLAVE)
    else:
        tbl = get_user_extra_tbl(role)

    if len(fileds) == 0:
        return tbl.find_one(userid)
    else:
        return tbl.find_one(userid, fileds)


def get_relationship_doc(myid, fri_id, fileds=[], method=mongfun.READ_SLAVE):
    """
    获取好友确认表信息
    myid: 我的id
    fri_id: 好友id
    :return:
    """
    if method == mongfun.READ_SLAVE:
        tbl = get_user_relationship_tbl(const.READ_SLAVE)
    else:
        tbl = get_user_relationship_tbl()

    key_id = "{}_{}".format(myid, fri_id)
    if len(fileds) == 0:
        return tbl.find_one(key_id)
    else:
        return tbl.find_one(key_id, fileds)


def get_friend_doc(myid, fri_id, fileds=[], method=mongfun.READ_SLAVE):
    """
    获取好友确认表信息
    myid: 我的id
    fri_id: 好友id
    :return:
    """
    if method == mongfun.READ_SLAVE:
        tbl = get_user_relationship_tbl(const.READ_SLAVE)
    else:
        tbl = get_user_relationship_tbl()

    key_id = "{}_{}".format(myid, fri_id)
    if len(fileds) == 0:
        return tbl.find_one(key_id)
    else:
        return tbl.find_one(key_id, fileds)


def get_friend_info(doc_friend, need_md5):
    """
    朋友信息
    1: 不让TA查看我的日程安排 2: 只可以查看我日程的时间段 3: 可以查看我的日程明细
    :param doc_friend:
    :return:
    """
    fri_info = FriendInfo()
    fri_info.userid = doc_friend['userid']
    fri_info.fid = doc_friend['fid']

    fri_simple = get_user_simple(fri_info.fid, mongfun.READ_SLAVE)
    fri_info.fimg = fri_simple.img
    fri_info.fname = fri_simple.name

    fri_info.fnick = pf.get_default_val(doc_friend, 'fnick', fri_simple.name)
    fri_info.fstar = doc_friend['fstar']
    fri_info.state = doc_friend['state']
    # 我看对方的日程权限
    fri_info.schpow = doc_friend['schpow']
    # 对方看我的日程权限
    op_doc = get_friend_doc(fri_info.fid, fri_info.userid)
    fri_info.sch_op = pf.get_default_val(op_doc, "schpow", 1)

    py_array = redisfun.get_pinyin(fri_info.fnick).split(" ")
    fri_info.pyall = py_array[0]
    fri_info.py = py_array[1]

    if need_md5:
        fri_info.md5 = doc_friend['md5']

    return fri_info


def is_my_friend(myid, fri_id):
    """
    判断是否是好友
    :param myid:
    :param fri_id:
    :return:
    """
    key_id = "{}_{}".format(myid, fri_id)
    doc = get_user_friends_tbl(const.READ_SLAVE).find_one(key_id)
    if doc:
        return True
    else:
        return False


def add_friend(myid, fri_id, fri_img, fri_name, fri_nick, sch_pow, state):
    """
    加为好友
    :param myid:
    :param fri_id:
    :param fri_img:
    :param fri_name:
    :param fri_nick:
    :param sch_pow:
    :param state:  1:好友 3:黑名单
    :return:
    """
    doc = mongfun.get_mongo_dict()
    doc['_id'] = "{}_{}".format(myid, fri_id)
    now = pf.get_utc_millis()
    doc['c'] = now
    doc['m'] = now
    doc['userid'] = myid
    doc['fid'] = fri_id
    doc['fimg'] = fri_img
    doc['fname'] = fri_name
    doc['fnick'] = fri_nick
    doc['fstar'] = 1  # 1: 正常 2: 标星
    doc['state'] = state
    doc['schpow'] = sch_pow
    doc['md5'] = pf.str_sha(pf.to_json(get_friend_info(doc, False)))
    get_user_friends_tbl().replace_one({"_id": doc['_id']}, doc, True)


def change_friend(myid, fri_id, fld_name, fld_val):
    """
    修改好友相关信息
    :param myid:
    :param fri_id:
    :param fld_name:
    :param fld_val:
    :return:
    """
    doc = get_friend_doc(myid, fri_id)
    if doc:
        doc['m'] = pf.get_utc_millis()
        doc[fld_name] = fld_val
        doc['md5'] = pf.str_sha(pf.to_json(get_friend_info(doc, False)))
        get_user_friends_tbl().replace_one({"_id": doc['_id']}, doc, True)

        return doc['md5']
    else:
        return ""


def get_user_simple(userid, method=mongfun.READ_PRIMARY):
    """
    只获取id, name, img
    :param userid:
    :param method:
    :return:
    """
    if method == mongfun.READ_SLAVE:
        tbl = get_user_tbl(const.READ_SLAVE)
    else:
        tbl = get_user_tbl()

    doc = tbl.find_one(pf.str2int(userid), ['_id', 'name', 'img'])
    res = UserSimple()
    if doc:
        res.id = pf.get_default_val(doc, '_id', userid)
        res.name = pf.get_default_val(doc, 'name', '')
        res.img = pf.get_default_val(doc, 'img', get_random_user_head_img())

    return res


def get_user_phone(role, userid, method=mongfun.READ_PRIMARY):
    """
    只获取id, name, img, phone
    :param userid:
    :param method:
    :return:
    """
    if method == mongfun.READ_SLAVE:
        tbl = get_user_tbl(True)
    else:
        tbl = get_user_tbl(role)

    doc = tbl.find_one(pf.str2int(userid), ['_id', 'name', 'img', 'phone'])
    res = UserPhone()
    if doc:
        res.id = pf.get_default_val(doc, '_id', userid)
        res.name = pf.get_default_val(doc, 'name', '')
        res.phone = pf.get_default_val(doc, 'phone', '')
        res.img = pf.get_default_val(doc, 'img', get_random_user_head_img())

    return res


def invite_one_person(usi_sender, phone):
    """
    推荐给好友使用
    http://gitlab.wx-inc.com/system/share_docs/wikis/user_db
    :param usi_sender:
    :param phone:
    :return:
    """
    para_map = dict()
    para_map['mob'] = phone
    para_map['p1'] = usi_sender.name
    sms.send_sms_async("invite_use_sms", para_map)


def get_user_role_list(userid):
    """
    获取用户权限 vx_admin: 系统管理员 vx_dev: 微侠开发人员 vx_kf: 微侠客服
    :param userid:
    :return:
    """
    doc = get_user_extra_doc(userid, ["role"], mongfun.READ_SLAVE)
    return pf.get_default_val(doc, "role", [])


def update_sync_hash(userid, role):
    """
    更新员工信息的hash值
    :param userid:
    :return:
    """
    if userid:
        doc_user = get_user_doc(userid, role)
        if doc_user:
            doc_user['c'] = 0
            doc_user['m'] = 0
            doc_user[const.SYNC_HASH] = ""

            self_hash = pf.str_sha(pf.to_json(doc_user))
            get_user_tbl(role).update_one({'_id': userid}, {'$set': {const.SYNC_HASH: self_hash}})


def update_relation_info(userid, doc_user):
    """

    :param doc_user:
    :param userid:
    :param role:
    :return:
    """
    relationship_tbl = get_user_relationship_tbl()
    if relationship_tbl.find({'rid': userid}).count():
        relationship_tbl.update({'rid': userid}, {'$set': {'rimg': doc_user['img'],
                                                                      'rname': doc_user['name'],
                                                                      'rnick': doc_user['nick'],
                                                                      'sex': doc_user['sex'],
                                                                      'post': doc_user['post'],
                                                                      'com_name': doc_user['com_name']}})


def getUserHash(userid, method=mongfun.READ_PRIMARY):
    """
    获取员工信息的个人部分和公司部分的hash值
    :param method:
    :param userid:
    :return:
    """
    doc_user = get_user_doc(userid, [const.SYNC_HASH], method)
    self_hash = pf.get_default_val(doc_user, const.SYNC_HASH, "")
    return self_hash


def get_user_info_map(userid, style, method=mongfun.READ_PRIMARY):
    """
    获取员工信息
    :param userid:
    :param style:
        all: 所有信息

    :param method:
    :return:
    """
    res_dict = dict()
    doc_user = None

    if style == const.USER_INFO_ALL:
        doc_user = get_user_doc(userid, [], method)
    elif style == const.USER_INFO_STRANGER:
        doc_user = get_user_doc(userid, ['sex', 'motto', 'name', 'img', 'star'], method)
    elif style == const.USER_INFO_ALL_GOLD:
        doc_user = get_user_doc(userid, [], method)
        doc_extra = get_user_extra_doc(userid, [], method)
        res_dict['g1'] = pf.get_default_val(doc_extra, 'g1', 10)
        res_dict['g2'] = pf.get_default_val(doc_extra, 'g2', 100)
        res_dict['g3'] = pf.get_vip_lv_by_g2(res_dict['g2'])
    elif style == const.USER_INFO_GOLD:
        doc_user = get_user_doc(userid, ['sex', 'motto', 'name', 'img', 'star'], method)
        doc_extra = get_user_extra_doc(userid, [], method)
        res_dict['g1'] = pf.get_default_val(doc_extra, 'g1', 10)
        res_dict['g2'] = pf.get_default_val(doc_extra, 'g2', 100)
        res_dict['g3'] = pf.get_vip_lv_by_g2(res_dict['g2'])
    elif style == const.USER_INFO_SET:
        doc_user = get_user_doc(userid, ["phone", "mail", 'img'], method)

    if doc_user:
        for k, v in doc_user.items():
            if k.endswith('lst'):
                continue
            res_dict[k] = v

    res_dict['id'] = userid
    # res_dict['img'] = pf.get_default_val(res_dict, 'img', get_random_user_head_img())

    # 处理掉不需要返回的内容
    pf.del_map_safe(res_dict, "_id")
    pf.del_map_safe(res_dict, "c")
    pf.del_map_safe(res_dict, "m")
    pf.del_map_safe(res_dict, "md5_sha")

    return res_dict


def get_user_setting(userid):
    """
    获取员工对应的个人设置, 以"ps_"开头在 user_db.user_extra 表中
    :param userid:
    :return:
    """
    res_dict = dict()
    doc_extra = get_user_extra_doc(userid, [], mongfun.READ_SLAVE)

    if doc_extra:
        for k, v in doc_extra.items():
            if k.startswith('ps_'):
                res_dict[k] = int(v)

    return res_dict


def update_phone_city(phone):
    """
    获取手机号码的运营商和注册地并更新数据库
    :param phone:
    :return:
    """
    try:
        xml_cont = pf_http.get_url_cont("http://life.tenpay.com/cgi-bin/mobile/MobileQueryAttribution.cgi",
                                        {"chgmobile": phone}, "gb2312")
        xml = pf.parse_xml_dict(xml_cont)
        if xml['root']['retmsg'].lower() == "ok":
            get_login_tbl().update_one({"_id": phone},
                                       {"$set": {"city": xml['root']['province'] + xml['root']['city'],
                                                 "carrier": xml['root']['supplier']}})
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        gmfun.log_error_to_es(err_msg)


def getSearchDoc(compid, userid):
    """
    获取一个向搜索引擎填充的数据包
    :param compid:
    :param userid:
    :return:
    """
    doc = get_user_info_map(compid, userid, mongfun.READ_SLAVE)

    # 复制一份
    userdoc = pf.json_to_map(pf.to_json(doc))
    pf.del_map_safe(userdoc, "compid")
    pf.del_map_safe(userdoc, "md5_sha")
    pf.del_map_safe(userdoc, "id")
    pf.del_map_safe(userdoc, "img")

    userdoc['star'] = const.EMP_STAR_LIST[pf.str2int(pf.get_default_val(doc, 'star', 0))]
    if pf.is_has_val(doc, 'leader', const.MAP_HAS_KEY_AND_VAL):
        userdoc['leader'] = doc['leader'].id
        userdoc['ld_name'] = doc['leader'].name

    for k, v in userdoc.items():
        if isinstance(v, (str, unicode)):
            if v:
                userdoc[k] = pf.removeHCandHH(v)
            else:
                pf.del_map_safe(userdoc, k)

    userdoc['dates'] = "{} {} {} {}".format(pf.get_default_val(doc, 'joindate', ''),
                                            pf.get_default_val(doc, 'birth', ''),
                                            pf.get_default_val(doc, 'condate', ''),
                                            pf.get_default_val(doc, 'trydate', ''))
    userdoc[const.ES_DOC] = pf.to_json(getUserListInfo(compid, userid))

    return userdoc


def getUserListInfo(compid, userid):
    """
    批量加载同事信息
    :param compid:
    :param userid:
    :return:
    """
    doc = get_user_info_map(compid, userid, mongfun.READ_SLAVE)
    ui = UserListInfo()
    ui.id = userid
    ui.name = pf.get_default_val(doc, 'name', '')
    ui.img = pf.get_default_val(doc, 'img', '')
    ui.dept = pf.get_default_val(doc, 'dept', '')
    ui.inner = pf.get_default_val(doc, 'inner', '')
    ui.phone = pf.get_default_val(doc, 'phone', '')
    ui.post = pf.get_default_val(doc, 'post', '')
    ui.isin = pf.get_default_val(doc, 'isin', '')

    return ui


def set_user_img_url(userid, url):
    """
    用户头像地址save
    :param userid:
    :param url:
    :return:
    """
    get_user_tbl().update_one({"_id": userid}, {"$set": {"img": url}})


def get_view_userid_lst(compid, userid, style):
    """
    加载有权查看我的周报或日程的人员列表
    :param compid:
    :param userid:
    :param style:
    :return:
    """
    tbl = getViewPowerTbl()
    cursor = tbl.find({"userid": userid, "type": style, "compid": compid}, read_preference=mongfun.READ_SLAVE)

    seeid_list = list()
    for doc in cursor:
        seeid_list.append(doc['seeid'])

    return seeid_list


def is_i_can_see(compid, myid, userid, style):
    """
    我是否有权看指定人的指定业务
    :param compid:
    :param myid:
    :param userid:
    :param style: wr: 周报 / sch: 日程
    :return:
    """
    doc = getViewPowerTbl().find_one({"compid": compid, "type": style, "seeid": myid, "userid": userid},
                                     read_preference=mongfun.READ_SLAVE)
    if doc:
        return True
    else:
        return False


def get_user_state_dc(role, userid=0):
    """

    :param userid:
    :param role:
    :return:
    """
    tbl_login = get_login_tbl(role)
    if not userid:
        state_dc = {}
        login_doc = tbl_login.find({}, {'state': 1, 'userid': 1})
        for doc in login_doc:
            state_dc.update({doc['userid']: doc['state']})
        if state_dc:
            return state_dc
        else:
            return {}
    else:
        account = '{}_{}'.format(role, userid)
        login_doc = tbl_login.find_one(account)
        if login_doc['state']:
            return 1
        else:
            return 0


def deal_3rd_head_url(userid, role, nick, head_url):
    """
    启动线程下载微信头像
    :param role:
    :param userid:
    :param nick:
    :param head_url:
    :return:
    """
    # 下载头像并上传
    if head_url:
        # img_name = "vx_{}.jpg".format(userid)
        # img_path = "/tmp/vx_{}.jpg".format(userid)
        # pf_http.http_download(head_url, img_path)
        # 上传头像图片
        # gmfun.send_only("uploadfile", {"file": "", "fname": img_name})
        # os.remove(img_path)
        # 写入数据库
        get_user_tbl(role).update_one({"_id": userid}, {"$set": {"img": head_url, "nick": nick}})
    else:
        get_user_tbl(role).update_one({"_id": userid}, {"$set": {"img": ""}})


def set_login_info(res, role, pid):
    """
    设置用户登陆信息
    :param res:
    :param role:
    :param pid:
    :return:
    """
    img_list = []
    cursor = get_user_tbl(role).find({"pid": pid})
    res.body['user']['admin_grp_doc'] = {}
    if role == const.USER_ROLE_M and res.body['user'].get('ro_type', "") == 6:
        # 为前台展示W的权限名称
        for k in res.body['user'].get('role_lst', []):
            res.body['user']['admin_grp_doc'].update({k: const.ROLE_W_DICT.get(int(k), "")})

    # 用户c需要返回相应公司及团队的信息
    elif role == const.USER_ROLE_C:
        use_doc_b = get_user_doc(pid, const.USER_ROLE_B)
        # 给前段用户企业信息
        res.body['use_b'] = {"com_name": use_doc_b['com_name'], "img": use_doc_b['img'],
                             "com_desc": use_doc_b.get('com_desc', ""),
                             "com_addr": use_doc_b['com_addr'], "slogan": use_doc_b.get('slogan', ""),
                             "email": use_doc_b.get('email', ""),"state": use_doc_b['state'],
                             "url": use_doc_b.get('url', ""), "com_tel": use_doc_b.get('com_tel', 0)}

        # 为前台展示权限名称
        for k in res.body['user'].get('role_lst', []):
            res.body['user']['admin_grp_doc'].update({k: const.ROLE_B_DICT.get(int(k), "")})
        # 登陆返回额外信息
        extra_doc = get_user_extra_doc(res.body['user']['_id'], role)
        pf.del_map_safe(extra_doc, "init_pwd")
        res.body['extra'] = extra_doc

    # 暂时只对b和c的用户登陆做处理
    elif role != const.USER_ROLE_B:
        return
    for doc in cursor:
        img_list.append(doc.get('c_img', ""))
    res.body['img_list'] = img_list


def set_login_success(res, role, userid, account, style=const.LOGIN_INNER):
    """
    成功登录后的设置
    :param style:
    :param role:
    :param res:
    :param userid:
    :param account:
    :return:
    """
    now = pf.get_utc_millis()
    user_doc = get_user_doc(userid, role)
    get_user_tbl(role).update_one({"_id": userid}, {"$set": {"log_time": now}})

    # 获取权限组信息
    role_doc = get_user_role(role).find_one(user_doc.get('grp_id', ""))

    # M用户获得权限类型
    if role_doc and role == const.USER_ROLE_M:
        user_doc['ro_type'] = role_doc.get('ro_type', "")

    user_doc['park_id'] = str(user_doc.get('park_id', ""))
    user_doc['grp_id'] = str(user_doc.get('grp_id', ""))
    user_doc['role'] = role
    res.body['user'] = user_doc
    # 返回客户端body结构
    res.body['mysess'] = pf.create_uuid_str()
    pid = user_doc.get('pid', 0)
    if pid:
        # 设置特殊登陆信息
        set_login_info(res, role, pid)

    # 用户redis信息结构
    usi = UserSessInfo()
    # user_simple= UserSimple
    usi.id = userid
    usi.name = user_doc.get("name", "")
    usi.com_name = user_doc.get('com_name', "")
    usi.role = role
    usi.img = user_doc.get('img', "")
    usi.mobile = user_doc.get("mobile", "")
    usi.account = account
    usi.a_type = user_doc.get('a_type', "")
    usi.ro_type = user_doc.get('ro_type', 99)
    usi.pid = user_doc.get('pid', 0)
    usi.mid = user_doc.get('mid', 0)
    mysess_lst = redisfun.get_user_mysess(account)
    if mysess_lst:
        mysess_lst = ujson.loads(mysess_lst)
        mysess_lst.append(res.body['mysess'])
    else:
        mysess_lst = [res.body['mysess']]
    redisfun.set_sess_info(res.body['mysess'], pf.to_json(usi), account, pf.to_json(mysess_lst), style)


def regist_by_3rd(union_id, role, nick, head_url, source, invite_code):
    """
    第三方登录注册
    :param invite_code:
    :param role:
    :param union_id:
    :param nick:
    :param head_url:
    :param source: 注册来源
    :return:
    """
    tbl_login = get_login_tbl(role)

    # 开始注册
    tbl_user = get_user_tbl(role)

    # 生成一个不重复的userid
    userid = create_union_userid(role)

    doc_login = mongfun.get_mongo_dict()
    now = pf.get_utc_millis()
    doc_login['c'] = now
    doc_login['m'] = now
    doc_login['_id'] = "{}_{}".format(const.USER_ROLE_C, userid)
    doc_login['id_3rd'] = union_id
    doc_login['mobile'] = ""
    doc_login['userid'] = userid
    doc_login['style'] = source
    doc_login['salt'] = ""
    doc_login['pwd'] = ""
    doc_login['headurl'] = head_url
    doc_login['state'] = const.ACCOUNT_UNFREEZE  # 账户状态

    tbl_login.insert_one(doc_login)

    # user_db.user表保存
    doc_user = mongfun.get_mongo_dict()
    doc_user['c'] = now
    doc_user['m'] = now
    doc_user['_id'] = userid
    doc_user['pid'] = 0  # 所属商户id
    doc_user['mobile'] = ""
    doc_user['nick'] = nick
    doc_user['img'] = ""
    doc_user['name'] = ""
    doc_user['email'] = ""
    doc_user['post'] = ""
    doc_user['now_addr'] = ""
    doc_user['park'] = ""
    doc_user['park_id'] = ""
    doc_user['sex'] = 0
    doc_user['a_type'] = 2  # c用户默认为子账户
    doc_user['hr_ok'] = 0  # 是否公司认证,默认未认证
    doc_user['bid'] = 0  # 绑定的b主帐号id
    doc_user['bid_lst'] = []  # 绑定的b子帐号列表
    doc_user['la_lst'] = []  # 技能标签
    doc_user['intro'] = ""  # 个人简介
    doc_user['pro_type'] = ""  # 行业类型
    doc_user['pro_name'] = ""  # 行业类型名称
    doc_user['state'] = 1

    doc_user['state'] = const.ACCOUNT_UNFREEZE  # 账户状态

    tbl_user.insert_one(doc_user)

    # user_db.user_extra表保存
    get_user_extra_tbl(const.USER_ROLE_C).insert_one({"_id": userid, "vip": 0})

    # 启动线程下载微信头像
    # thread.start_new_thread(deal_3rd_head_url, (userid, const.USER_ROLE_C, nick, head_url))
    deal_3rd_head_url(userid, const.USER_ROLE_C, nick, head_url)
    # 更新人员信息的hash值
    update_sync_hash(userid, const.USER_ROLE_C)

    # 创建论坛相关信息
    redisfun.set_sess_bbs(userid)
    param_bbs = {'mysess': str(userid), 'u_id': userid, 'u_type': role}
    gmfun.send_only("lt_create_user", param_bbs)

    return userid


def get_invite_code_info(invite_code):

    invite_doc = get_invite_tbl().find_one({"inv_code": invite_code})

    return invite_doc


def switch_account(res, s_uid, t_uid, s_role, t_role):
    """
    用户帐号切换
    :param t_userid: 目标账户id
    :param res:
    :param userid: 原账户id
    :param s_role: 原账户
    :param t_role: 目标账户
    :return:
    """
    # 判断是否真实绑定
    if not s_role or not t_role:
        return "STATUS_NOT_BINDED"

    elif t_role == const.USER_ROLE_B:
        # 获取目标账户信息
        user_t_doc = get_user_tbl(t_role).find_one(t_uid)
        if user_t_doc['cid'] != s_uid:
            return "STATUS_NOT_BINDED"
    else:
        # 获取目标账户信息
        user_t_doc = get_user_tbl(t_role).find_one(t_uid)
        if s_uid not in user_t_doc['bid_lst'] and s_uid != user_t_doc['bid']:
            return "STATUS_NOT_BINDED"

    t_account = pf.get_hy_account(t_role, t_uid)
    doc_login = get_login_tbl(t_role).find_one(t_account)

    # 查看是否被锁定
    if redisfun.isLoginLocked(doc_login['_id']):
        return "STATUS_LOGINLOCK"

    # 查看帐号是否被冻结
    if doc_login['state'] == 0:
        return 'STATUS_ACCOUNT_FREEZE'

    # 确认信息,开始登陆
    redisfun.removeLoginLock(t_account)
    set_login_success(res, t_role, user_t_doc['_id'], doc_login['_id'])
    return const.SUSSES


def load_userinfo_by_pid(user_connent, where_or_lst, pid, master, s_log_t, e_log_t):
    """
    通过主账户pid查询主账户和子账户信息
    :param s_log_t:
    :param e_log_t:
    :param user_connent:
    :param where_or_lst:
    :param pid:
    :param master:是否显示主账户
    :return:
    """

    if s_log_t:
        where_and_lst = [{"pid": pid}, {"log_time": {'$gt': s_log_t}}, {"log_time": {'$lt': e_log_t}}]
    else:
        where_and_lst = [{"pid": pid}]
    # 是否显示主帐号
    if master:

        if where_or_lst:  # 模糊查询关键字列表
            cursor = user_connent.find({"$and": where_and_lst, "$or": where_or_lst})

        else:
            cursor = user_connent.find({"$and": where_and_lst})

    else:
        where_and_lst.append({"a_type": 2})
        if where_or_lst:  # 模糊查询关键字列表
            cursor = user_connent.find({"$and": where_and_lst, "$or": where_or_lst})

        else:

            cursor = user_connent.find({"$and": where_and_lst})
    return cursor


def load_all_userinfo(user_connent, res, rcv, where_or_lst, page_index, a_type):
    """

    :param user_connent: collection对象
    :param res: http出参
    :param rcv: http入参
    :param where_and_lst:and 查询条件
    :param where_or_lst: or查询条件
    :param page_index: 分页
    :return:
    """
    where_and_lst = [{"a_type": a_type}]
    pf.del_http_headers(rcv)
    # 选取额外查询条件
    for k, v in rcv.items():
        if k == 'serv_lst' or k == 'state' or k == 'sel_type':
            where_and_lst.append({k: int(v)})
        elif k == 'park' or k == 'com_addr':
            where_and_lst.append({k: {'$regex': v}})
        else:
            where_and_lst.append({k: v})

    if where_or_lst:  # 模糊查询关键字列表
        cursor = user_connent.find({"$and": where_and_lst, "$or": where_or_lst})
        total = cursor.count()
    else:
        cursor = user_connent.find({"$and": where_and_lst})
        total = cursor.count()
    res.body.update({"total": total, "s": page_index})

    return cursor


def refesh_main_info(tbl_user, chi_doc, pid):
    """

    :param tbl_user:
    :param chi_doc:
    :param pid:
    :return:
    """
    pri_user = tbl_user.find_one(pid)
    for k, v in chi_doc.items():
        if k in const.MAIN_FIELD_NAME_LST:
            chi_doc[k] = pri_user.get(k, "")
    return tbl_user

if __name__ == '__main__':
    # add_friend(10, 20, "", "test3", "test3", 2, 1)
    # add_friend(10, 20, "", "test4", "test4", 2, 1)
    print create_union_userid()


