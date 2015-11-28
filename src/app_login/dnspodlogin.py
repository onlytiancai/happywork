# -*- coding: utf-8 -*-
import web
import json

from . import account
from . import config
from .oauth import OAuth

dnspodOAuth = OAuth(
    name='dnspod',
    client_id=config.dnspod_app_id,
    client_secret=config.dnspod_app_key,
    base_url='https://www.dnspod.cn/Api/',
    access_token_url='https://www.dnspod.cn/OAuth/Access.Token',
    authorize_url='https://www.dnspod.cn/OAuth/Authorize')


class dnspodlogin(object):
    def GET(self):
        url = dnspodOAuth.get_authorize_url(response_type='code',
                                        redirect_uri=config.dnspod_callback,
                                        )
        return web.redirect(url)


class dnspodcallback(object):
    def get_access_token(self, code):
        result = dnspodOAuth.get_access_token('GET',
                                          code=code,
                                          grant_type='authorization_code',
                                          redirect_uri=config.dnspod_callback)
        result = json.loads(result)
        return result['access_token']

    def get_openid(self, access_token):
        result = dnspodOAuth.request('POST', 'User.Detail', access_token=access_token, format='json')
        result = json.loads(result)
        return result['info']['user']['id']

    def get_nickname(self, access_token, openid):
        result = dnspodOAuth.request('POST', 'User.Detail', access_token=access_token, format='json')
        result = json.loads(result)
        return result['info']['user']['nick']

    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        code = web.input().code

        if code:
            access_token = self.get_access_token(code)
            openid = self.get_openid(access_token)
            nickname = self.get_nickname(access_token, openid)

            if account.account_exists(username=openid, usertype='dnspod'):
                result = account.direct_login(username=openid, nickname=nickname, usertype='dnspod')
            else:
                result = account.register_account(username=openid, password=None, nickname=nickname, usertype='dnspod')
            
            if result['code'] != 200:
                raise web.Forbidden()

            return web.redirect('/')
