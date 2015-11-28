# -*- coding: utf-8 -*-
import web
import uuid
import urlparse
import json

from . import account
from . import config
from .oauth import OAuth

qqOAuth = OAuth(
    name='qq',
    client_id=config.qq_app_id,
    client_secret=config.qq_app_key,
    base_url='https://graph.qq.com',
    access_token_url='https://graph.qq.com/oauth2.0/token',
    authorize_url='https://graph.qq.com/oauth2.0/authorize')


class qqlogin(object):
    def GET(self):
        state = uuid.uuid1()
        web.setcookie('qqstate', state)
        url = qqOAuth.get_authorize_url(response_type='code',
                                        redirect_uri=config.qq_callback,
                                        state=state)
        return web.redirect(url)


class qqcallback(object):
    def get_access_token(self, code):
        result = qqOAuth.get_access_token('GET',
                                          code=code,
                                          grant_type='authorization_code',
                                          redirect_uri=config.qq_callback)
        result = dict(urlparse.parse_qsl(result))
        return result['access_token']

    def get_openid(self, access_token):
        result = qqOAuth.request('GET', '/oauth2.0/me', access_token=access_token)
        result = result.lstrip("callback( ")
        result = result.rstrip(" );\n")
        result = json.loads(result)
        return result['openid']

    def get_nickname(self, access_token, openid):
        result = qqOAuth.request('GET', '/user/get_user_info',
                                 access_token=access_token,
                                 openid=openid,
                                 oauth_consumer_key=config.qq_app_id)
        result = json.loads(result)
        return result['nickname']

    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        code = web.input().code
        state = web.input().state
        cookie_state = web.cookies().get('qqstate')
        if state != cookie_state:
            raise web.Forbidden()

        if code:
            access_token = self.get_access_token(code)
            openid = self.get_openid(access_token)
            nickname = self.get_nickname(access_token, openid)

            if account.account_exists(username=openid, usertype='qq'):
                result = account.direct_login(username=openid, nickname=nickname, usertype='qq')
            else:
                result = account.register_account(username=openid, password=None, nickname=nickname, usertype='qq')
            
            if result['code'] != 200:
                raise web.Forbidden()

            return web.redirect('/')
