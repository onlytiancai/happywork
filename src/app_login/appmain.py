# -*- coding: utf-8 -*-

import web
import hashlib
import json
from . import account
from . import qqlogin
from . import weibologin
from . import dnspodlogin


app_jslink = '<script src="/static/sea-modules/seajs/1.3.0/sea-debug.js" data-main="/static/apps/login/login-main"></script>'
jslink = '<script src="/static/apps/login/login.js"></script>'


class login(object):
    def POST(self):
        postdata = web.input()
        username = postdata.username
        nickname = postdata.username
        password = postdata.password
        password = hashlib.sha1(password).hexdigest()

        if account.account_exists(username):
            result = account.login(username=username, password=password, nickname=nickname)
        else:
            result = account.register_account(username, password, nickname)
        return json.dumps(result)


class logout(object):
    def POST(self):
        return json.dumps(account.logout())


class userinfo(object):
    def GET(self):
        result = account.get_userinfo()
        return json.dumps(result)

    def POST(self):
        result = account.update_userinfo(web.input)
        return json.dumps(result)


urls = ["/login", login,
        "/logout", logout,
        "/userinfo", userinfo,
        "/qqlogin", qqlogin.qqlogin,
        "/qqcallback", qqlogin.qqcallback,
        "/weibologin", weibologin.weibologin,
        "/weibocallback", weibologin.weibocallback,
        "/dnspodlogin", dnspodlogin.dnspodlogin,
        "/dnspodcallback", dnspodlogin.dnspodcallback,
        ]
