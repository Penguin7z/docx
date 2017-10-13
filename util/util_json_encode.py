#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: tbl_fun.py
# Purpose: PyCharm
#
# Author: 董佳佳(simon.Dong)
#
# Created: 16/12/9 上午00:22

import pytz
import datetime

from bson.objectid import ObjectId
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# RFC 1123 (ex RFC 822)
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
# DATE_FORMAT_CUSTOME='%mmon%dday %w %H:%M'
local_tz = pytz.timezone('Asia/Shanghai')


class BaseJSONEncoder(json.JSONEncoder):
    """ Proprietary JSONEconder subclass used by the json render function.
    This is needed to address the encoding of special values.
    """

    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     # convert any datetime to RFC 1123 format
        #     return date_to_str(obj)
        # elif isinstance(obj, (datetime.datetime.time, datetime.datetime.date)):
        #     # should not happen since the only supported date-like format
        #     # supported at dmain schema level is 'datetime' .
        #     return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class MongoJSONEncoder(BaseJSONEncoder):
    """ Proprietary JSONEconder subclass used by the json render function.
    This is needed to address the encoding of special values.
    .. versionadded:: 0.2
    """

    def default(self, obj):
        if isinstance(obj, ObjectId):
            # BSON/Mongo ObjectId is rendered as a string
            return str(obj)
        else:
            # delegate rendering to base class method
            return super(MongoJSONEncoder, self).default(obj)


def date_to_str(date):
    """ Converts a datetime value to the corresponding RFC-1123 string.
    :param date: the datetime value to convert.
    """
    return datetime.datetime.strftime(date, DATE_FORMAT) if date else None


def to_json(doc):
    """
    转换成utf-8的json字符串
    :param doc:
    :return:
    """
    return json.dumps(doc, cls=MongoJSONEncoder)


if __name__ == '__main__':
    pass
