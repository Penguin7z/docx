#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: util_datetime.py
# Purpose: PyCharm
#
# Author: 董佳佳(simon.Dong)
#
# Created: 16/12/9 上午00:22
import pytz

from common import pf
import datetime
from datetime import timedelta
import time

utc_0 = int(time.mktime(datetime.datetime(1970, 01, 01).timetuple()))


def time_num():
    """
    年月日时分秒毫秒

    :return:
    """

    datetime_now_china = pf.get_china_time_from_ms(pf.get_utc_millis())
    time_num = '{:%Y%m%d%H%M%S}'.format(datetime_now_china)

    return str(time_num)


def get_next_day_from_ms(ms):
    """
    根据当前时间，取之后的一天
    :param ms:
    :return:
    """
    dt = pf.get_china_time_from_ms(ms)
    dt = dt + datetime.timedelta(days=1)
    return pf.datetime_to_utc_ms(dt)


def get_days_from_ms(ms, days):
    """
    根据当前时间，取之后的一天
    :param ms:
    :param days:
    :return:
    """
    dt = pf.get_china_time_from_ms(ms)
    dt = dt + datetime.timedelta(days=days)
    return pf.datetime_to_utc_ms(dt)


def get_after_x_day_from_ms(ms, days):
    """
    根据当前时间，获取几天后的时间
    :param ms:
    :param days:
    :return:
    """
    dt = pf.get_china_time_from_ms(ms)
    after_time = datetime.timedelta(days=days)
    dt = dt + after_time
    return pf.datetime_to_utc_ms(dt)


def get_day_00_00_00_from_ms(ms):
    """
    根据当前时间，取当天的00：00：00
    :param ms:
    :return:
    """
    dt = pf.get_china_time_from_ms(ms)
    dt_str = pf.get_datetime_str(dt, "%Y-%m-%d")
    return pf.datetime_to_utc_ms(
            pf.str_to_datetime("{} {}".format(dt_str, '00:00:00')))


def get_next_day_00_00_00_from_ms(ms):
    """
    根据当前时间，取下一天的00：00：00
    :param ms:
    :return:
    """
    ms = get_next_day_from_ms(ms)
    dt = pf.get_china_time_from_ms(ms)
    dt_str = pf.get_datetime_str(dt, "%Y-%m-%d")
    return pf.datetime_to_utc_ms(
            pf.str_to_datetime("{} {}".format(dt_str, '00:00:00')))


def get_day_23_59_59_from_ms(ms):
    """
    根据当前时间，取当天的23：59：59
    :param ms:
    :return:
    """
    dt = pf.get_china_time_from_ms(ms)
    dt_str = pf.get_datetime_str(dt, "%Y-%m-%d")
    return pf.datetime_to_utc_ms(
            pf.str_to_datetime("{} {}".format(dt_str, '23:59:59')))


def cut_after_min_from_ms(ms):
    """
    把毫秒数的分钟之后的部分cut掉
    :param ms:
    :return:
    """
    dt_china = pf.get_china_time_from_ms(ms)
    # 只取到分钟数
    tmp_dt = datetime.datetime(dt_china.year, dt_china.month, dt_china.day, dt_china.hour, dt_china.minute,
                               tzinfo=dt_china.tzinfo)
    return pf.datetime_to_utc_ms(tmp_dt)


def cut_after_hour_min_second_from_ms(ms):
    """
    把毫秒数的时分秒后的部分cut掉
    :param ms:
    :return:
    """
    dt_china = pf.get_china_time_from_ms(ms)

    tmp_dt = datetime.datetime(dt_china.year, dt_china.month, dt_china.day, tzinfo=dt_china.tzinfo)
    return pf.datetime_to_utc_ms(tmp_dt)


def get_period_begin_and_end_date(from_day, end_day):
    """
    根据开始日期和结束日期，求得开始账期日和结束账期日
    :param from_day:
    :param end_day:
    :return:
    """

    payment_first_weekday = 0  # 周一
    payment_second_weekday = 3  # 周四

    if not (from_day and end_day):
        return False, False
    # 计算账单开始日期
    from_day_mo = get_previous_x_day_from_date(payment_first_weekday, from_day)
    from_day_th = get_previous_x_day_from_date(payment_second_weekday, from_day)
    payment_from_day = from_day_th if from_day_mo < from_day_th else from_day_mo

    # 计算账单结束日期
    end_day_mo = get_previous_x_day_from_date(payment_first_weekday, end_day)
    end_day_th = get_previous_x_day_from_date(payment_second_weekday, end_day)
    payment_end_day = end_day_th if end_day_mo < end_day_th else end_day_mo

    final_from_datetime = datetime.datetime.combine(payment_from_day, datetime.datetime.min.time())
    final_end_datetime = datetime.datetime.combine(payment_end_day, datetime.datetime.min.time())

    return final_from_datetime, final_end_datetime


def get_previous_x_day_from_date(x_day, from_date):
    """
    获取 from_date 之前的 某一天(某周几)
    x_day->weekdays
    0->mo 1->tu 2->we 3->th 4->fr 5->sa 6->su
    :param x_day:
    :param from_date:
    :return:
    """
    if not from_date:
        return False

    x_day = pf.str2int(x_day)
    if x_day < 0 or x_day > 6:
        return False

    offset_x_day = (from_date.weekday() - x_day) % 7
    last_x_day_date = from_date - timedelta(days=offset_x_day)

    return last_x_day_date


def get_payment_period_date_list(begin_ms, end_ms):
    pass


def datetime_to_utc_ms(dt):
    """
    转化为utc的毫秒数
    :param dt:
    :return:
    """
    return int((time.mktime(dt.utctimetuple()) - utc_0) * 1000) + int(dt.microsecond / 1000)


def str_to_datetime(str_date, style='%Y-%m-%d %H:%M:%S', tzstr='Asia/Shanghai'):
    """
    style:格式字符串是python的标准日期格式码，例如：
        %Y-%m-%d %H:%M:%S
        %Y-%m-%d
    """
    dt = datetime.datetime.strptime(str_date, style)
    dt = pytz.timezone(tzstr).localize(dt)
    return dt


if __name__ == "__main__":
    pass


