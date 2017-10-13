#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: role_demo.py.py
# Purpose: PyCharm
#
# Author: 企鹅(simon.dong)
#
# Created: 2017/7/14 上午1:02
import json
import pinyin
import re
from bson import ObjectId

from common import pf
from util import tbl_fun


class RoleVectorType(object):
    RoleVectorTypePark = 1
    RoleVectorTypeCompany = 2
    RoleVectorTypeRole = 3
    RoleVectorTypePage = 4
    RoleVectorTypeMenu = 5
    RoleVectorTypeIndustry = 6
    RoleVectorTypeAction = 7
    RoleVectorTypeService = 8

CONST_ROLE_VECTOR_TYPE = {
    RoleVectorType.RoleVectorTypePark: u"园区",
    RoleVectorType.RoleVectorTypeCompany: u"企业",
    RoleVectorType.RoleVectorTypeRole: u"角色",
    RoleVectorType.RoleVectorTypePage: u"页面",
    RoleVectorType.RoleVectorTypeMenu: u"菜单",
    RoleVectorType.RoleVectorTypeIndustry: u"行业",
    RoleVectorType.RoleVectorTypeAction: u"行为",
    RoleVectorType.RoleVectorTypeService: u"服务",
}


class ResInfo(object):
    def __init__(self):
        self.status = 200
        self.msg = 'ok'
        self.body = {}


def is_alpha(data):
    regex_str = '^[a-z_]+$'
    if re.match(regex_str, data):
        return True
    return False


def create_admin_group(data):
    """
    创建 管理员类型 admin_group
    :param data:
    :return:
    """
    res = ResInfo()
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "sta": 1,
        "mid": 0,
        "c": pf.get_utc_millis(),
        "m": pf.get_utc_millis(),
    }

    if "role_" in alias or "_list" in alias:
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_admin_group_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}]
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    insert_result = tbl_fun.get_am_admin_group_tbl(False).insert_one(doc)
    res.body = {
        "_id": str(insert_result.inserted_id)
    }
    return res


def update_admin_group(data):
    """
    修改 管理员类型 admin_group
    :param data:
    :return:
    """
    res = ResInfo()
    single_id = data.get("single_id", "")
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    if len(single_id) != 24:
        res.status = 920
        res.msg = u"参数错误single_id"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "m": pf.get_utc_millis(),
    }

    if "role_" in alias or "_list" in alias:
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_admin_group_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}],
        "_id": {"$ne": ObjectId(single_id)}
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    tbl_fun.get_am_admin_group_tbl(False).update_one(
        {"_id": ObjectId(single_id)}, {"$set": doc})
    res.body = {
        "_id": single_id
    }
    return res


def create_role_vector(data):
    """
    创建 权限维度 role_vector
    :param data:
    :return:
    """
    res = ResInfo()
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    vector_type = data.get("vector_type", 0)
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    if vector_type not in CONST_ROLE_VECTOR_TYPE.keys():
        res.status = 920
        res.msg = u"权限组类型不正确"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "vector_type": vector_type,
        "sta": 1,
        "mid": 0,
        "c": pf.get_utc_millis(),
        "m": pf.get_utc_millis(),
    }

    if "role_" in alias or "_list" in alias:
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 判断是否有重复的vector_type
    if tbl_fun.get_am_role_vector_tbl(False).find_one({
        "vector_type": vector_type
    }):
        res.status = 920
        res.msg = u"已存在同类型的权限维度"
        return res

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_role_vector_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}]
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    insert_result = tbl_fun.get_am_role_vector_tbl(False).insert_one(doc)
    res.body = {
        "_id": str(insert_result.inserted_id)
    }
    return res


def update_role_vector(data):
    """
    修改 权限维度 role_vector
    :param data:
    :return:
    """
    res = ResInfo()
    single_id = data.get("single_id", "")
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    vector_type = data.get("vector_type", 0)
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    if len(single_id) != 24:
        res.status = 920
        res.msg = u"参数错误single_id"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    if vector_type not in CONST_ROLE_VECTOR_TYPE.keys():
        res.status = 920
        res.msg = u"权限组类型不正确"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "m": pf.get_utc_millis(),
    }

    if "role_" in alias or "_list" in alias:
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_role_vector_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}],
        "_id": {"$ne": ObjectId(single_id)}
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 查看老的数据有无 vector_type
    old_vector_info = tbl_fun.get_am_role_vector_tbl(False).find_one(
        {"_id": ObjectId(single_id)})
    if not old_vector_info:
        res.status = 920
        res.msg = u"找不到权限维度"
        return res

    if not old_vector_info.get("vector_type", 0):
        doc.update({"vector_type": vector_type})

    tbl_fun.get_am_role_vector_tbl(False).update_one(
        {"_id": ObjectId(single_id)}, {"$set": doc})
    res.body = {
        "_id": single_id
    }
    return res


def create_role_vector_detail(data):
    """
    创建 权限维度详情 role_vector_detail
    :param data:
    :return:
    """
    res = ResInfo()
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    rv_id = data.get("rv_id", "")
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    if len(rv_id) != 24:
        res.status = 920
        res.msg = u"参数错误rv_id"
        return res

    # 根据rv_id取vector_type
    vector_info = tbl_fun.get_am_role_vector_tbl(False).find_one(
        {"_id": ObjectId(rv_id)})
    if not vector_info:
        res.status = 920
        res.msg = u"参数错误rv_id"
        return res
    vector_type = vector_info.get("vector_type", 0)

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "rv_id": rv_id,
        "vector_type": vector_type,
        "sta": 1,
        "mid": 0,
        "c": pf.get_utc_millis(),
        "m": pf.get_utc_millis(),
    }

    # 判断rv_id是否存在
    if not tbl_fun.get_am_role_vector_tbl(False).find_one({
        "_id": ObjectId(rv_id)
    }):
        res.status = 920
        res.msg = u"参数错误rv_id"
        return res

    if "role_" in alias or "_list" in alias:
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_role_vector_detail_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}]
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    insert_result = tbl_fun.get_am_role_vector_detail_tbl(False).insert_one(
        doc)
    res.body = {
        "_id": str(insert_result.inserted_id)
    }
    return res


def update_role_vector_detail(data):
    """
    修改 权限维度详情 role_vector_detail
    :param data:
    :return:
    """
    res = ResInfo()
    single_id = data.get("single_id", "")
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    if len(single_id) != 24:
        res.status = 920
        res.msg = u"参数错误single_id"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "m": pf.get_utc_millis(),
    }

    if "role_" in alias or "_list" in alias:
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_role_vector_detail_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}],
        "_id": {"$ne": ObjectId(single_id)}
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    tbl_fun.get_am_role_vector_detail_tbl(False).update_one(
        {"_id": ObjectId(single_id)}, {"$set": doc})
    res.body = {
        "_id": single_id
    }
    return res


def create_user_role(data):
    """
    创建 admin_group
    :param data:
    :return:
    """
    res = ResInfo()
    name = data.get("name", "")
    desc = data.get("desc", "")
    if not (name and desc):
        res.status = 920
        res.msg = u"参数错误"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "sta": 1,
        "mid": 0,
        "c": pf.get_utc_millis(),
        "m": pf.get_utc_millis(),
    }

    insert_result = tbl_fun.get_am_admin_group_tbl(False).insert_one(doc)
    res.body = {
        "_id": str(insert_result.inserted_id)
    }
    return res


def get_admin_group_list():
    """
    获取 管理员组列表 admin_group
    :return:
    """
    data_cursor = tbl_fun.get_am_admin_group_tbl(False).find()
    data_list = []
    for data in data_cursor:
        doc = {
            "id": str(data.get("_id", "")),
            "name": data.get("name", ""),
            "desc": data.get("desc", ""),
            "alias": data.get("alias", ""),
            "sta": data.get("sta", ""),
            "c": data.get("c", ""),
            "m": data.get("m", ""),
        }
        data_list.append(doc)

    return data_list


def get_role_vector_list():
    """
    获取 权限维度列表 admin_group
    :return:
    """
    data_cursor = tbl_fun.get_am_role_vector_tbl(False).find()
    data_list = []
    for data in data_cursor:
        doc = {
            "id": str(data.get("_id", "")),
            "name": data.get("name", ""),
            "desc": data.get("desc", ""),
            "alias": data.get("alias", ""),
            "vector_type": data.get("vector_type", ""),
            "vector_type_str": CONST_ROLE_VECTOR_TYPE.get(
                data.get("vector_type", ""), data.get("vector_type", "")),
            "sta": data.get("sta", ""),
            "c": data.get("c", ""),
            "m": data.get("m", ""),
        }

        data_list.append(doc)

    return data_list


def get_role_vector_detail_list(vector_id):
    """
    获取 权限维度列表 admin_group
    :param vector_id:
    :return:
    """
    if len(vector_id) != 24:
        return []
    data_cursor = tbl_fun.get_am_role_vector_detail_tbl(False).find(
        {"rv_id": vector_id})
    data_list = []
    for data in data_cursor:
        doc = {
            "id": str(data.get("_id", "")),
            "name": data.get("name", ""),
            "desc": data.get("desc", ""),
            "alias": data.get("alias", ""),
            "rv_id": data.get("rv_id", ""),
            "sta": data.get("sta", ""),
            "c": data.get("c", ""),
            "m": data.get("m", ""),
        }

        data_list.append(doc)

    return data_list


def get_role_vector_detail(vector_id):
    """
    获取 权限维度详情 role_vector_detail
    :param vector_id:
    :return:
    """
    if len(vector_id) != 24:
        return {}
    data_info = tbl_fun.get_am_role_vector_tbl(False).find_one(
        {"_id": ObjectId(vector_id)})
    if not data_info:
        return {}

    if data_info:
        data_info["_id"] = str(data_info.get("_id", ""))
    return data_info


def get_role_config_info(user_id):
    """
    获取 可配置权限信息 get_role_config_info
    :param user_id:
    :return:
    """

    # 获取当前用户的创建者的权限列表
    # 获取当前用户的权限列表
    # mid是999的，读取admin_group_id对应的数据，作为最大范围权限
    # mid不是999的，读取mid用户对应的数据，作为最大范围权限

    if not user_id:
        return []

    # 获取改用户当前权限
    user_role_info = tbl_fun.get_am_user_role_tbl(False).find_one(
        {"user_id": user_id})

    # 所属权限组ID
    admin_group_id = user_role_info.get("admin_group_id", "")
    if not admin_group_id:
        return []

    if not user_role_info:
        return []

    # 找到其父级用户权限
    mid = user_role_info.get("mid", 0)
    if not mid:
        return []
    user_parent_role_info = tbl_fun.get_am_user_role_tbl(False).find_one(
        {"user_id": mid})

    if mid == 999:
        user_parent_role_info = tbl_fun.get_am_group_role_tbl(False).find_one(
            {"group_id": admin_group_id})
    if not user_parent_role_info:
        # 未配置admin_group权限
        return []

    role_vector_alias_full_list = []
    role_vector_full_list = []
    for key in user_parent_role_info.keys():
        if key.startswith("role_") and key.endswith("_list"):
            role_vector_full_list.append(key)
            alias_name = key
            alias_name = alias_name.replace("role_", "", 1)
            alias_name = alias_name.replace("_list", "", 1)
            role_vector_alias_full_list.append(alias_name)

    if not role_vector_alias_full_list:
        return []

    # 获取维度详情列表
    vector_detail_id_full_list = []
    for key in role_vector_full_list:
        vector_detail_id_full_list.extend(user_parent_role_info.get(key, []))

    # 根据维度详情id，获取维度详情
    vector_detail_id_full_list = [ObjectId(
        x) for x in vector_detail_id_full_list]
    role_vector_detail_cursor = tbl_fun.get_am_role_vector_detail_tbl(
        False).find({"_id": {"$in": vector_detail_id_full_list}})

    # 根据别名，获取维度详情
    dic_vector_detail_id_mapping_detail = {}
    for role_vector_detail in role_vector_detail_cursor:
        _id = str(role_vector_detail.get("_id", ""))
        dic_vector_detail_id_mapping_detail[_id] = role_vector_detail

    # 根据别名，获取维度信息列表
    role_vector_cursor = tbl_fun.get_am_role_vector_tbl(False).find(
        {"alias": {"$in": role_vector_alias_full_list}})

    # 根据别名，获取维度详情
    dic_vector_alias_mapping_detail = {}
    for role_vector in role_vector_cursor:
        alias_name = role_vector.get("alias", "")
        dic_vector_alias_mapping_detail[alias_name] = role_vector

    # 得到当前用户可得的维度列表名称，再获取其每一个维度的子列表
    full_role_vector_list = []
    for vector_alias in role_vector_alias_full_list:
        vector_detail_list_temp = []
        role_name = "{}_{}_list".format("role", vector_alias)
        vector_detail_id_list = user_parent_role_info.get(role_name, [])
        for vector_detail_id in vector_detail_id_list:
            vector_detail_list_temp.append(
                dic_vector_detail_id_mapping_detail.get(vector_detail_id, {}))

        vector_info = dic_vector_alias_mapping_detail.get(vector_alias, {})
        vector_info["vector_list"] = vector_detail_list_temp
        if vector_detail_list_temp:
            full_role_vector_list.append(vector_info)

    # 设置是否已经有权限
    for role_vector in full_role_vector_list:
        for role_vector_detail in role_vector.get("vector_list", []):
            role_vector_id = str(role_vector_detail.get("_id", ""))
            role_name = "{}_{}_list".format(
                "role", role_vector.get("alias", ""))
            role_list = user_role_info.get(role_name, [])
            role_vector_detail["role_own"] = 0

            if role_vector_id in role_list:
                role_vector_detail["role_own"] = 1

    # 把_id 改成 id
    for role_vector in full_role_vector_list:
        # 把别名改成 role_alias_list 形式
        role_vector["alias"] = "role_{}_list".format(role_vector["alias"])
        role_vector["id"] = str(role_vector["_id"])
        for role_vector_detail in role_vector.get("vector_list", []):
            role_vector_detail["id"] = str(role_vector_detail["_id"])

    # 如果有menu，把menu变成二级形式
    for role_vector in full_role_vector_list:
        vector_type = role_vector.get("vector_type", 0)
        if vector_type == RoleVectorType.RoleVectorTypeMenu:
            vector_list = role_vector.get("vector_list", [])
            menu_list = get_menu_list(vector_list)
            role_vector["vector_list"] = menu_list

    return full_role_vector_list


def get_all_role_config(group_id):
    """
    获取全部权限列表
    :return:
    """
    # 获取全部的权限列表
    if not group_id or len(group_id) != 24:
        return []
    dic_role_mapping_detail = {}
    role_vector_detail_cursor = tbl_fun.get_am_role_vector_detail_tbl(
        False).find()
    for role_vector_detail in role_vector_detail_cursor:
        _id = str(role_vector_detail["rv_id"])
        role_vector_detail["rv_id"] = _id
        role_vector_detail["_id"] = str(role_vector_detail["_id"])
        role_vector_detail_list = dic_role_mapping_detail.get(_id, [])
        role_vector_detail_list.append(role_vector_detail)
        dic_role_mapping_detail[_id] = role_vector_detail_list

    role_vector_cursor = tbl_fun.get_am_role_vector_tbl(False).find()
    role_vector_list = []
    for role_vector in role_vector_cursor:
        _id = str(role_vector.get("_id", ""))
        role_vector["_id"] = _id
        role_vector["vector_list"] = dic_role_mapping_detail.get(_id, [])
        if role_vector["vector_list"]:
            role_vector_list.append(role_vector)

    # 获取该权限组的当前权限情况
    group_role_info = tbl_fun.get_am_group_role_tbl(False).find_one(
        {"group_id": group_id})
    group_got_role_list = []
    if group_role_info:
        for key in group_role_info.keys():
            if key.startswith("role_") and key.endswith("_list"):
                group_got_role_list.extend(group_role_info[key])

    for role_vector in role_vector_list:
        for role_vector_detail in role_vector.get("vector_list", []):
            role_vector_id = str(role_vector_detail.get("_id", ""))
            role_vector_detail["role_own"] = 0
            if role_vector_id in group_got_role_list:
                role_vector_detail["role_own"] = 1

    # 把_id 改成 id
    for role_vector in role_vector_list:
        # 把别名改成 role_alias_list 形式
        role_vector["alias"] = "role_{}_list".format(role_vector["alias"])
        role_vector["id"] = str(role_vector["_id"])
        for role_vector_detail in role_vector.get("vector_list", []):
            role_vector_detail["id"] = str(role_vector_detail["_id"])

    # 把菜单按二级分组
    for role_vector in role_vector_list:
        vector_type = role_vector.get("vector_type", 0)
        if vector_type == RoleVectorType.RoleVectorTypeMenu:
            vector_list = role_vector.get("vector_list", [])
            menu_list = get_menu_list(vector_list)
            role_vector["vector_list"] = menu_list

    # 获取页面列表
    return role_vector_list


def get_user_admin_list(user_id):
    user_role_list = []
    dic_group_info = {}
    data_cursor = tbl_fun.get_am_admin_group_tbl(False).find()
    for data in data_cursor:
        dic_group_info[str(data.get("_id", ""))] = data.get("name", "")
    user_role_cursor = tbl_fun.get_am_user_role_tbl(False).find(
        {"mid": user_id, "user_id": {"$ne": user_id}})
    for user_role in user_role_cursor:
        user_role["_id"] = str(user_role.get("_id", ""))
        user_role["admin_group_str"] = dic_group_info.get(
            user_role.get("admin_group_id", 0), "")
        user_role_list.append(user_role)

    return user_role_list


def set_user_admin_group(user_id, group_id):
    """
    给管理员配置权限组
    :param user_id:
    :param group_id:
    :return:
    """
    res = ResInfo()
    if not user_id or not group_id:
        res.status = 920
        res.msg = u"参数错误"
        return res
    user_role_info = tbl_fun.get_am_user_role_tbl(False).find_one(
        {"user_id": user_id})
    if not user_role_info:
        res.status = 920
        res.msg = u"参数错误，找不到用户信息"
        return res
    if user_role_info.get("admin_group_id", ""):
        res.status = 920
        res.msg = u"用户已有有所属权限组"
        return res

    group_info = tbl_fun.get_am_admin_group_tbl(False).find_one(
        {"_id": ObjectId(group_id)})
    if not group_info:
        res.status = 920
        res.msg = u"参数错误，找不到权限组"
        return res

    doc_update = {
        "admin_group_id": group_id,
        "m": pf.get_utc_millis(),
    }
    tbl_fun.get_am_user_role_tbl(False).update_one(
        {"user_id": user_id}, {"$set": doc_update})

    return res


def update_user_role_config(data):
    """
    配置用户权限信息
    :param data:
    :return:
    """
    res = ResInfo()

    user_id = pf.str2int(data.get("user_id", 0))
    mid = pf.str2int(data.get("mid", 0))

    if not user_id or not mid:
        res.status = 920
        res.msg = u"参数错误"
        return res

    role_detail_update_list = []
    dic_role_detail_list = {}
    for key in data.keys():
        if key.startswith("role_") and key.endswith("_list"):
            vector_detail_update_list = json.loads(data.get(key, "[]"))
            role_detail_update_list.extend(vector_detail_update_list)
            dic_role_detail_list[key] = vector_detail_update_list

    if not role_detail_update_list:
        res.status = 920
        res.msg = u"没有新的修改"
        return res

    # 获取该用户当前权限
    user_role_info = tbl_fun.get_am_user_role_tbl(False).find_one(
        {"user_id": user_id})

    # 所属权限组ID
    admin_group_id = user_role_info.get("admin_group_id", "")
    if not admin_group_id:
        return []

    if not user_role_info:
        res.status = 920
        res.msg = u"用户信息错误"
        return res

    # 找到其父级用户权限
    user_parent_role_info = tbl_fun.get_am_user_role_tbl(False).find_one(
        {"user_id": mid})
    if mid == 999:
        user_parent_role_info = tbl_fun.get_am_group_role_tbl(False).find_one(
            {"group_id": admin_group_id})
    if not user_parent_role_info:
        res.status = 920
        res.msg = u"创建者信息错误"
        return res

    # 根据其父级权限，获取权限列表
    role_detail_full_list = []
    for key in user_parent_role_info.keys():
        if key.startswith("role_") and key.endswith("_list"):
            vector_detail_list = user_parent_role_info.get(key, [])
            role_detail_full_list.extend(vector_detail_list)

    if not role_detail_full_list:
        res.status = 920
        res.msg = u"没有权限可增加"
        return res

    not_allowed_list = [x for x in role_detail_update_list
                        if x not in role_detail_full_list]
    if not_allowed_list:
        res.status = 920
        res.msg = u"权限不足"
        return res

    dic_role_detail_list.update({"mid": mid, "m": pf.get_utc_millis()})

    tbl_fun.get_am_user_role_tbl(False).update_one(
        {"user_id": user_id}, {"$set": dic_role_detail_list})

    return res


def update_role_group_config(data):
    """
    配置用户权限信息
    :param data:
    :return:
    """
    res = ResInfo()

    group_id = data.get("group_id", "")

    if not group_id:
        res.status = 920
        res.msg = u"参数错误"
        return res

    role_detail_update_list = []
    dic_role_detail_list = {}
    for key in data.keys():
        if key.startswith("role_") and key.endswith("_list"):
            vector_detail_update_list = json.loads(data.get(key, "[]"))
            role_detail_update_list.extend(vector_detail_update_list)
            dic_role_detail_list[key] = vector_detail_update_list

    if not role_detail_update_list:
        res.status = 920
        res.msg = u"没有新的修改"
        return res

    old_group_role_info = tbl_fun.get_am_group_role_tbl(False).find_one(
        {"group_id": group_id})
    t_now = pf.get_utc_millis()
    c = t_now
    if old_group_role_info:
        c = old_group_role_info.get("c", t_now)

    dic_role_detail_list.update({"group_id": group_id,
                                 "mid": 999,
                                 "m": t_now,
                                 "c": c})

    tbl_fun.get_am_group_role_tbl(False).replace_one({"group_id": group_id},
                                                     dic_role_detail_list,
                                                     upsert=True)

    return res


def create_menu(data):
    """
    创建菜单 create_menu
    :param data:
    :return:
    """
    res = ResInfo()
    name = data.get("name", "")
    desc = data.get("desc", "")
    alias = data.get("alias", "").lower()
    url = data.get("url", "").lower()
    parent_id = data.get("parent_id", "")
    if not all((name, desc, alias)):
        res.status = 920
        res.msg = u"参数错误"
        return res

    # 别名必须纯小写字母
    if not is_alpha(alias):
        res.status = 920
        res.msg = u"别名必须纯小写字母或下划线组合"
        return res

    if parent_id and len(parent_id) != 24:
        res.status = 920
        res.msg = u"参数错误parent_id"
        return res

    doc = {
        "name": name,
        "desc": desc,
        "alias": alias,
        "parent_id": parent_id,
        "sta": 1,
        "mid": 0,
        "url": url,
        "c": pf.get_utc_millis(),
        "m": pf.get_utc_millis(),
    }

    # 判断名字和别名是否有重复
    if tbl_fun.get_am_menu_tbl(False).find_one({
        "$or": [{"name": name},
                {"alias": alias}]
    }):
        res.status = 920
        res.msg = u"名称或别名重复"
        return res

    insert_result = tbl_fun.get_am_menu_tbl(False).insert_one(doc)
    res.body = {
        "_id": str(insert_result.inserted_id)
    }
    return res


def get_menu_list(vector_list):
    """
    获取菜单列表
    :return:
    """
    # 获取一级菜单列表
    dic_header_menu = {}
    header_menu_cursor = tbl_fun.get_am_role_vector_detail_tbl(False).find(
        {"vector_type": RoleVectorType.RoleVectorTypeMenu,
         "menu_level": 1,
         })
    for header_menu in header_menu_cursor:
        dic_header_menu[str(header_menu.get("_id", ""))] = header_menu

    dic_menu_mapping_child = {}
    for menu in vector_list:
        menu_id = str(menu.get("_id", ""))
        parent_id = menu.get("parent_id", "")
        if not parent_id or not menu_id:
            continue
        init_menu_obj = {
            "menu_info": {},
            "sub_menu_list": [],
        }
        menu_obj = dic_menu_mapping_child.get(parent_id, init_menu_obj)
        if menu_id == parent_id:
            menu_obj["menu_info"] = menu
        url = menu.get("url", "")
        if url and url != "#" and menu_id != parent_id:
            menu_obj["sub_menu_list"].append(menu)
        if not menu_obj.get("menu_info", {}):
            menu_obj["menu_info"] = dic_header_menu.get(parent_id, {})
        dic_menu_mapping_child[parent_id] = menu_obj

    menu_list = dic_menu_mapping_child.values()
    menu_list = sorted(menu_list,
                       key=lambda k: k.get("menu_info", {}).get('sort_num', 0))
    return menu_list


def get_role_group_type_list():
    """
    获取权限组类型
    :return:
    """
    role_type_list = []
    for key, value in CONST_ROLE_VECTOR_TYPE.items():
        role_type_list.append({"name": key,
                               "value": value})
    return role_type_list


def init_data():
    data_admin_group_list = [
        {
            "name": "M-F",
            "desc": "财务组",
            "alias": "mf",
        },

        {
            "name": "M-B",
            "desc": "企业组",
            "alias": "mb",
        },

        {
            "name": "M-D",
            "desc": "数据组",
            "alias": "md",
        },

        {
            "name": "M-S",
            "desc": "商户组",
            "alias": "ms",
        },

        {
            "name": "M-W",
            "desc": "运营组",
            "alias": "mw",
        }
    ]

    data_role_vector_list = [
        {
            "name": "园区",
            "desc": "园区维度",
            "alias": "park",
            "vector_type": RoleVectorType.RoleVectorTypePark
        },

        {
            "name": "企业",
            "desc": "企业维度",
            "alias": "company",
            "vector_type": RoleVectorType.RoleVectorTypeCompany
        },

        {
            "name": "角色",
            "desc": "角色维度",
            "alias": "role",
            "vector_type": RoleVectorType.RoleVectorTypeRole
        },

        {
            "name": "页面",
            "desc": "页面维度",
            "alias": "page",
            "vector_type": RoleVectorType.RoleVectorTypePage
        },

        {
            "name": "菜单",
            "desc": "菜单维度",
            "alias": "menu",
            "vector_type": RoleVectorType.RoleVectorTypeMenu
        },

        {
            "name": "行业",
            "desc": "行业维度",
            "alias": "industry",
            "vector_type": RoleVectorType.RoleVectorTypeIndustry
        },

        {
            "name": "行为",
            "desc": "行为维度",
            "alias": "action",
            "vector_type": RoleVectorType.RoleVectorTypeAction
        },

        {
            "name": "服务",
            "desc": "服务维度",
            "alias": "service",
            "vector_type": RoleVectorType.RoleVectorTypeService
        },
    ]

    for x in data_admin_group_list:
        create_admin_group(x)

    for x in data_role_vector_list:
        create_role_vector(x)

    menu_list = [{'menu': {}, 'sub_menu_list': []}, {'menu': {'url': '#', 'name': u'\u57fa\u7840\u6570\u636e', 'class': ''}, 'sub_menu_list': [{'url': '/base_data', 'name': u'\u57fa\u7840\u6570\u636e\u5206\u6790', 'class': ''}, {'url': '/outline/menber_distribution', 'name': u'\u57fa\u7840\u6570\u636e\u7528\u6237\u6570\u91cf', 'class': ''}, {'url': '/outline/menber_login', 'name': u'\u57fa\u7840\u6570\u636e\u7528\u6237\u6d3b\u8dc3', 'class': ''}, {'url': '/outline/order_outline', 'name': u'\u57fa\u7840\u6570\u636e\u8ba2\u5355\u4ea4\u6613', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u56ed\u533a\u6570\u636e\u5206\u6790', 'class': ''}, 'sub_menu_list': [{'url': '/park_data', 'name': u'\u56ed\u533a\u57fa\u7840\u6570\u636e', 'class': ''}, {'url': '/park_data_park', 'name': u'\u56ed\u533a\u57fa\u7840\u6570\u636e\u56ed\u533a\u7ef4\u5ea6', 'class': ''}, {'url': '/park_sep/park_data_member_distribution', 'name': u'\u56ed\u533a\u7528\u6237\u5206\u5e03', 'class': ''}, {'url': '/park_sep/park_data_member_login', 'name': u'\u56ed\u533a\u7528\u6237\u767b\u5f55', 'class': ''}, {'url': '/park_sep/park_data_order_distribution', 'name': u'\u56ed\u533a\u7528\u6237\u8ba2\u5355', 'class': ''}, {'url': '/park_sep/park_com_menber_dis', 'name': u'\u56ed\u533a\u4f01\u4e1a\u7528\u6237', 'class': ''}, {'url': '/company/all', 'name': u'\u56ed\u533a\u4f01\u4e1a\u4fe1\u606f', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u6d3b\u52a8\u6570\u636e\u5206\u6790', 'class': ''}, 'sub_menu_list': [{'url': '/activity_data', 'name': u'\u6d3b\u52a8\u6570\u636e\u5206\u6790', 'class': ''}, {'url': '/new_activity_data', 'name': u'\u6d3b\u52a8\u6570\u636e\u5206\u6790\uff08\u5206\u4f1a\u5458\uff09', 'class': ''}]}, {'menu': {}, 'sub_menu_list': [{'url': '/user_detail', 'name': u'\u6ce8\u518c\u7528\u6237\u660e\u7ec6\u6570\u636e', 'class': ''}]}, {'menu': {}, 'sub_menu_list': [{'url': '/bbs_data', 'name': u'\u8bba\u575b\u6570\u636e\u5206\u6790', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u8ba2\u5355\u6570\u636e\u5206\u6790', 'class': ''}, 'sub_menu_list': [{'url': '/order_data', 'name': u'7\u65e5\u8ba2\u5355\u6d41\u6c34', 'class': ''}, {'url': '/order_s_data', 'name': u'\u5546\u6237\u8ba2\u5355\u62a5\u8868', 'class': ''}, {'url': '/order_last_week', 'name': u'\u4e0a\u5468\u5546\u6237\u8ba2\u5355\u62a5\u8868', 'class': ''}, {'url': '/order_park_data', 'name': u'\u56ed\u533a\u8ba2\u5355\u62a5\u8868', 'class': ''}]}, {'menu': {}, 'sub_menu_list': [{'url': '/search', 'name': u'\u6570\u636e\u68c0\u7d22', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u6d3b\u52a8\u5b9a\u5411\u5206\u6790', 'class': ''}, 'sub_menu_list': [{'url': '/activity/214', 'name': u'\u60c5\u4eba\u8282\u6d3b\u52a8', 'class': ''}, {'url': '/activity/small_game', 'name': u'\u5c0f\u6e38\u620f\u63a8\u5e7f', 'class': ''}, {'url': '/activity/coupon_get', 'name': u'\u62a2\u5238\u6d3b\u52a8', 'class': ''}, {'url': '/activity/happy_gift', 'name': u'\u6b22\u4e50\u9001\u63a8\u5e7f', 'class': ''}, {'url': '/activity/wehome_set', 'name': u'wehome\u5957\u9910', 'class': ''}, {'url': '/activity/invite', 'name': u'\u9080\u8bf7\u597d\u53cb', 'class': ''}, {'url': '/activity/comunity_beauty', 'name': u'\u6700\u7f8e\u793e\u7fa4\u5929\u4f7f', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u7528\u6237\u6d3b\u8dc3\u5ea6\u5206\u6790', 'class': ''}, 'sub_menu_list': [{'url': '/live/week', 'name': u'\u5468\u6d3b\u8dc3\u5ea6', 'class': ''}, {'url': '/live/total_view', 'name': u'\u56ed\u533a\u7528\u6237\u603b\u89c8', 'class': ''}, {'url': '/live/total_nodobe', 'name': u'\u56ed\u533a\u7528\u6237\u603b\u89c8\uff08\u975e\u5fb7\u5fc5\uff09', 'class': ''}, {'url': '/live/user_leave', 'name': u'\u6708\u7528\u6237\u7559\u5b58\u7387', 'class': ''}, {'url': '/live/user_remain_nodobe', 'name': u'\u6708\u7528\u6237\u7559\u5b58\u7387(\u975e\u5fb7\u5fc5)', 'class': ''}, {'url': '/live/remain_table', 'name': u'\u7528\u6237\u7559\u5b58\u7387', 'class': ''}, {'url': '/live/remain_table_nodobe', 'name': u'\u7528\u6237\u7559\u5b58\u7387(\u975e\u5fb7\u5fc5)', 'class': ''}, {'url': '/live/week_percentage', 'name': u'\u5468\u767b\u5f55\u6bd4\u4f8b\u5206\u6790', 'class': ''}, {'url': '/live/percentage_nodobe', 'name': u'\u5468\u767b\u5f55\u6bd4\u4f8b(\u975e\u5fb7\u5fc5)\u5206\u6790', 'class': ''}, {'url': '/live/week_static', 'name': u'\u5468\u767b\u5f55\u4eba\u6570\u5206\u6790', 'class': ''}, {'url': '/live/login_times', 'name': u'\u767b\u5f55\u6b21\u6570\u5206\u6790', 'class': ''}]}, {'menu': {'url': '#', 'name': u'app\u5206\u6790\u62a5\u8868', 'class': ''}, 'sub_menu_list': [{'url': '/app/app_outline', 'name': u'app\u603b\u89c8', 'class': ''}, {'url': '/app/app_download', 'name': u'app\u4e0b\u8f7d\u6e20\u9053\u7edf\u8ba1', 'class': ''}, {'url': '/app/sep_by_park', 'name': u'app\u5404\u56ed\u533a\u4f7f\u7528\u60c5\u51b5', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u7cfb\u7edf\u914d\u7f6e', 'class': ''}, 'sub_menu_list': [{'url': '/refresh_db', 'name': u'\u6570\u636e\u5e93\u5237\u65b0', 'class': ''}]}, {'menu': {'url': '#', 'name': u'\u6743\u9650\u7ba1\u7406', 'class': ''}, 'sub_menu_list': [{'url': '/role/group', 'name': u'\u6743\u9650\u7ec4\u7ba1\u7406', 'class': ''}, {'url': '/role/vector', 'name': u'\u6743\u9650\u7ef4\u5ea6\u7ba1\u7406', 'class': ''}, {'url': '/role/menu', 'name': u'\u83dc\u5355\u7ba1\u7406', 'class': ''}, {'url': '/role/page', 'name': u'\u754c\u9762\u7ba1\u7406', 'class': ''}, {'url': '/role/list/999', 'name': u'\u6743\u9650\u7ba1\u7406', 'class': ''}]}]
    rv_info = tbl_fun.get_am_role_vector_tbl(False).find_one(
        {"vector_type": RoleVectorType.RoleVectorTypeMenu})
    rv_id = str(rv_info.get("_id", ""))
    need_insert_main_menu_list = []
    need_insert_sub_menu_list = []
    for k1, menu in enumerate(menu_list):
        menu_info = menu.get("menu", {})
        sub_menu_info = menu.get("sub_menu_list", [])
        if (not menu_info) and (not sub_menu_info):
            continue
        menu_id = ObjectId()
        if not menu_info:
            menu_info = sub_menu_info[0]
        alias = pinyin.get_initial(menu_info["name"], delimiter="_")
        alias = "{}_{}".format(alias, pf.create_random_str(3).lower())
        doc_menu_info = {
            "_id": menu_id,
            "name": menu_info["name"],
            "desc": menu_info["name"],
            "url": menu_info["url"],
            "class": "",
            "parent_id": str(menu_id),
            "sort_num": k1,
            "c": pf.get_utc_millis(),
            "m": pf.get_utc_millis(),
            "mid": 999,
            "alias": alias,
            "menu_level": 1,
            "rv_id": rv_id,
            "vector_type": RoleVectorType.RoleVectorTypeMenu
        }
        need_insert_main_menu_list.append(doc_menu_info)

        for k2, sub_menu in enumerate(sub_menu_info):
            sub_menu_id = ObjectId()
            alias = pinyin.get_initial(sub_menu["name"], delimiter="_")
            doc_sub_menu_info = {
                "_id": sub_menu_id,
                "name": sub_menu["name"],
                "desc": sub_menu["name"],
                "url": sub_menu["url"],
                "class": "",
                "parent_id": str(menu_id),
                "sort_num": k2,
                "c": pf.get_utc_millis(),
                "m": pf.get_utc_millis(),
                "mid": 999,
                "alias": alias,
                "menu_level": 2,
                "rv_id": rv_id,
                "vector_type": RoleVectorType.RoleVectorTypeMenu
            }
            need_insert_sub_menu_list.append(doc_sub_menu_info)

    need_insert_main_menu_list.extend(need_insert_sub_menu_list)
    from pymongo import InsertOne
    upsert_list = []
    for menu in need_insert_main_menu_list:
        upsert_list.append(InsertOne(menu))

    if upsert_list:
        tbl_fun.get_am_menu_tbl(False).remove()
        tbl_fun.get_am_role_vector_detail_tbl(False).bulk_write(upsert_list)


def test_data():
    init_data()
    import json
    import random
    from common import pf
    user_id = random.randint(20000, 30000)
    # user_id = 999
    role_vector_list = get_all_role_config()
    dic_role = {
        "user_id": user_id,
        "c": pf.get_utc_millis(),
        "m": pf.get_utc_millis(),
        "mid": 999,
        "admin_group_id": "",
    }
    for role_vector in role_vector_list:
        alias = role_vector.get("alias", "")
        role_name = "{}_{}_list".format("role", alias)
        role_list = []
        for role_vector_detail in role_vector.get("vector_list", []):
            role_vector_detail["role_own"] = random.randint(0, 1)
            if role_vector_detail["role_own"] == 1:
                role_list.append(str(role_vector_detail["_id"]))

        dic_role[role_name] = role_list

    print json.dumps(dic_role)


if __name__ == "__main__":
    u = 26479
    print test_data()

