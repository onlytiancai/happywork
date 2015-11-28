# -*- coding: utf-8 -*-
import web


def ensure_login(f):
    def inner(*args, **kargs):
        if not web.extensions.is_login():
            raise web.unauthorized()
        return f(*args, **kargs)
    return inner
