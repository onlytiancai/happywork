# -*- coding: utf-8 -*-
import web
import uuid
import urlparse
import json

from . import account
from . import config
from .oauth import OAuth

weiboOAuth = OAuth(
    name='weibo',
    client_id=config.weibo_app_id,
    client_secret=config.weibo_app_key,
    base_url='https://api.weibo.com',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    authorize_url='https://api.weibo.com/oauth2/authorize')


class weibologin(object):
    def GET(self):
        state = uuid.uuid1()
        web.setcookie('weibostate', state)
        url = weiboOAuth.get_authorize_url(response_type='code',
                                        redirect_uri=config.weibo_callback,
                                        state=state)
        return web.redirect(url)


class weibocallback(object):
    def get_access_token_and_uid(self, code):
        result = weiboOAuth.get_access_token('POST',
                                          code=code,
                                          grant_type='authorization_code',
                                          redirect_uri=config.weibo_callback)
        result = json.loads(result)
        return result['access_token'], result['uid']


    def get_nickname(self, access_token, uid):
        result = weiboOAuth.request('GET', '/2/users/show.json',
                                 access_token=access_token,
                                 uid=uid,
                                 source=config.weibo_app_id)
        result = json.loads(result)
        return result['screen_name']

    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        code = web.input().code
        state = web.input().state
        cookie_state = web.cookies().get('weibostate')
        if state != cookie_state:
            raise web.Forbidden()

        if code:
            access_token, uid = self.get_access_token_and_uid(code)
            nickname = self.get_nickname(access_token, uid)

            if account.account_exists(username=uid, usertype='weibo'):
                result = account.direct_login(username=uid, nickname=nickname, usertype='weibo')
            else:
                result = account.register_account(username=uid, password=None, nickname=nickname, usertype='weibo')
            
            if result['code'] != 200:
                raise web.Forbidden()

            return web.redirect('/')
