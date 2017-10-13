#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: util_xlsx.py
# Purpose: PyCharm
#
# Author: 董佳佳(simon.Dong)
#
# Created: 16/10/8 下午1:36

import xlsxwriter
import StringIO

DATE_FORMAT_EXCEL = '%Y-%m-%d %H:%M:%S'


def new_workbook(**kwargs):
    """
    :return:
    """
    is_download = kwargs.get("is_download", False)
    output = StringIO.StringIO()
    if is_download:
        workbook = xlsxwriter.Workbook(output, {"strings_to_numbers": False,
                                                "strings_to_formulas": False,
                                                "strings_to_urls": False})

        return output, workbook

    workbook = xlsxwriter.Workbook('/Users/e/Documents/test.xlsx')
    return output, workbook


def end_workbook(output, workbook):
    """
    :param output:
    :param workbook:
    :return:
    """
    workbook.close()
    output.seek(0)
    return output


if __name__ == '__main__':
    pass
