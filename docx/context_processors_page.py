#!/usr/bin/python
# -*- coding: UTF-8 -*-


def view_page(request):
    path = request.path
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    login_name = request.session.get("login_name", "")
    dic_view_page = {
        "login_name": login_name,
        "current_path": path
    }

    doc_filter = request.session.get("doc_filter", {})

    return {
        "view_page": dic_view_page,
        "doc_filter": doc_filter,
    }
