#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: gmfun.py


import gearman
import traceback
import logging
from threading import Timer
from gearman.errors import GearmanError

import config as cfg
import pf
import const
from define.resinfo import ResBase

log = logging.getLogger(cfg.g_log)


def send_only(job_name, job_data):
    gm = None
    try:
        gm = gearman.GearmanClient(cfg.g_gearman)
        job_json = pf.to_json(job_data)
        gm.submit_job(str(job_name), job_json, background=True, wait_until_complete=False)
    except GearmanError:
        err_msg = traceback.format_exc()
        log.error(err_msg)
    finally:
        if gm:
            gm.shutdown()


def send_only_for_log(job_name, job_data):
    gm = None
    try:
        # 这里用的是es_log的gearman
        gm = gearman.GearmanClient(cfg.g_gearman_log)
        job_json = pf.to_json(job_data)
        gm.submit_job(str(job_name), job_json, background=True, wait_until_complete=False)
    except GearmanError:
        err_msg = traceback.format_exc()
        log.error(err_msg)
    finally:
        if gm:
            gm.shutdown()


def send_sleep_200ms(job_name, job_data):
    # 读写分离的情况下,预留200ms给集群数据同步
    Timer(0.2, send_only, (job_name, job_data)).start()


def send_sleep(job_name, job_data, seconds):
    Timer(seconds, send_only, (job_name, job_data)).start()


def log_to_es(job_name, in_dict, out_obj, usi=None):
    """
    记录日志到elastic search
    :param job_name:
    :param st:
    :param in_dict:
    :param out_obj:
    :return:
    """
    log_map = dict()
    log_map['fun'] = job_name
    log_map['et'] = pf.get_utc_millis()
    log_map['in'] = in_dict

    out_dict = dict()
    out_dict['ip'] = cfg.g_ip

    if isinstance(out_obj, ResBase):
        out_dict['status'] = out_obj.status
        out_dict['msg'] = out_obj.msg
    elif type(out_obj) is dict:
        out_dict['status'] = out_obj['status']
        out_dict['msg'] = out_obj['msg']
    else:
        out_dict['status'] = 200
        out_dict['msg'] = "ok"

    log_map['out'] = out_dict

    if usi and usi.id > 0:
        log_map['usi'] = {'id': usi.id, 'name': usi.name, 'role': usi.role}

    send_only_for_log('es_idx_log', log_map)


def log_error_to_es_with_fun(fun_name, in_dict, err_msg, usi=None):
    """
    记录日志到elastic search
    :param fun_name:
    :param in_dict:
    :param err_msg:
    :param usi:
    :return:
    """
    log_map = dict()
    log_map['fun'] = fun_name
    log_map['et'] = pf.get_utc_millis()
    log_map['in'] = in_dict

    out_dict = dict()
    out_dict['ip'] = cfg.g_ip
    out_dict['status'] = const.EXCEPTION_CODE
    out_dict['msg'] = err_msg

    log_map['out'] = out_dict

    if usi and usi.id > 0:
        log_map['usi'] = {'id': usi.id, 'name': usi.name}

    send_only_for_log('es_idx_log', log_map)


def log_error_to_es(err_msg, usi=None):
    """
    记录日志到elastic search
    :param job_name:
    :param st:
    :param in_dict:
    :param out_obj:
    :return:
    """
    log_map = dict()
    log_map['fun'] = "error"
    log_map['et'] = pf.get_utc_millis()
    log_map['in'] = {'seqnum': pf.get_utc_millis()}

    out_dict = dict()
    out_dict['ip'] = cfg.g_ip
    out_dict['status'] = const.EXCEPTION_CODE
    out_dict['msg'] = err_msg

    log_map['out'] = out_dict

    if usi and usi.id > 0:
        log_map['usi'] = {'id': usi.id, 'name': usi.name}

    send_only_for_log('es_idx_log', log_map)


def send_then_wait(job_name, job_data):
    try:
        seqnum = pf.get_default_val(job_data, "seqnum", pf.get_utc_millis())
        job_data['seqnum'] = seqnum
        job_data['web_st'] = pf.get_utc_millis()

        job_json = pf.to_json(job_data)

        gm = gearman.GearmanClient(cfg.g_gearman)
        job = gm.submit_job(str(job_name), job_json, poll_timeout=30)
        if job.complete:
            rtn = job.result
            rtnmap = pf.json_to_map(rtn)

            # 日志记录到elastic search
            log_map = dict()
            log_map['fun'] = job_name
            log_map['et'] = pf.get_utc_millis()
            log_map['in'] = job_data
            log_map['out'] = rtnmap

            send_only_for_log('es_idx_log', log_map)

            pf.del_map_safe(rtnmap, 'ip')

            return rtnmap
        else:
            tmp = "{}: timeout".format(job_name)
            return pf.build_error_res(const.STATUS_TIMEOUT, seqnum, tmp)
    except Exception as e:
        log.error(e)
    finally:
        gm.shutdown()
