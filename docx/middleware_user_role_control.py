from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth import logout
import pytz
from util import util_datetime

local_tz = pytz.timezone('Asia/Shanghai')


class AdminRoleVerifyMiddleware(object):
    """
    This middleware lets you match a specific url and redirect the request to a
    new url.

    You keep a tuple of url regex pattern/url redirect tuples on your site
    settings, example:

    URL_REDIRECTS = (
        (r'www\.example\.com/hello/$', 'http://hello.example.com/'),
        (r'www\.example2\.com/$', 'http://www.example.com/example2/'),
    )
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        self.reset_filter(request)

        path = request.path
        cookie_age = getattr(settings, 'SESSION_COOKIE_AGE', 300)
        if datetime.now(tz=local_tz) - request.session.get_expiry_date(
                tz=local_tz) < timedelta(seconds=cookie_age):
            request.session.set_expiry(
                datetime.now(tz=local_tz) + timedelta(seconds=cookie_age))
        else:
            request.session["login_name", ""] = ""
            logout(request=request)
        if path == "/login" or path == "/login/":
            return None
        else:
            if len(request.session.get("login_name", "")) > 0:
                if path == "/index" or path == "/index/":
                    return None
                return None
            else:
                return HttpResponseRedirect("/login")

    def reset_filter(self, request):
        if request.method == "POST":
            select_hour_duration = request.POST.get("select-hour-duration",
                                                    "00:00-00:00")
            date_duration = request.POST.get("date-duration", "")
            date_begin_str = ""
            date_end_str = ""
            hour_begin_str = ""
            select_hour_duration_list = select_hour_duration.split("-")
            date_duration_list = date_duration.split("-")
            if len(date_duration_list) == 2:
                date_begin_str = date_duration_list[0]
                date_end_str = date_duration_list[1]
            if len(select_hour_duration_list) == 2:
                hour_begin_str = select_hour_duration_list[0]
            if date_begin_str and date_end_str:
                date_begin = util_datetime.str_to_datetime(date_begin_str,
                                                           style='%Y/%m/%d')
                date_end = util_datetime.str_to_datetime(date_end_str,
                                                         style='%Y/%m/%d')
                date_begin_ms = util_datetime.get_days_from_ms(
                    util_datetime.datetime_to_utc_ms(date_begin), -1)
                date_end_ms = util_datetime.datetime_to_utc_ms(date_end)
                doc_filter = {
                    "date_duration": date_duration,
                    "select_hour_duration": select_hour_duration,
                    "date_begin_ms": date_begin_ms,
                    "date_end_ms": date_end_ms,
                    "hour_str": hour_begin_str,
                }
                request.session["doc_filter"] = doc_filter
