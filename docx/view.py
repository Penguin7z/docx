# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
import pytz

import sys

from docx import settings

reload(sys)
sys.setdefaultencoding('utf-8')

# RFC 1123 (ex RFC 822)
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
DATE_FORMAT_DOWNLOAD = '%Y%m%d%H%M%S'
local_tz = pytz.timezone('Asia/Shanghai')


def test_html(request):
    context = {'STATIC_URL': settings.STATIC_URL}
    print settings.STATIC_URL
    return render(request, 'basic_data.html', context)


def index(request):
    context = {'STATIC_URL': settings.STATIC_URL}
    print settings.STATIC_URL
    return render(request, 'index.html', context)


def nav_to_login(request):
    context = {'STATIC_URL': settings.STATIC_URL}
    if request.method == 'GET':
        logout(request)
        request.session["AdminID"] = ''
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            return HttpResponseRedirect('/login')
        if username == "bi_admin" and password == "wehomebi940" or username == "wuhao" and password == "321qwe":
            request.session["login_name"] = username
            return HttpResponseRedirect('/index')
        user = authenticate(username=username, password=password)
        print user
        if not user:
            context["alert_info"] = u"登录失败，用户名或密码错误"
            return render(request, 'login.html', context)
        if user.is_active:
            login(request=request, user=user)
            print "log in success"


def nav_to_log_out(request):
    request.session["login_name"] = None
    context = {'STATIC_URL': settings.STATIC_URL}
    return HttpResponseRedirect('/login')


if __name__ == '__main__':
    pass
