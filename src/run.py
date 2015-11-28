# -*- coding: utf-8 -*-
import web
import config
from common import db

def load_extensions():
    '''
    加载全局扩展，顺序不能变，有依赖关系
    '''
    web.extensions = web.storage()

    # 1. 初始化db
    conn = "mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8"
    conn = conn % dict(db=config.dbname, user=config.dbuser,
                       password=config.dbpassword, host=config.dbhost,
                       port=config.dbport)

    db.init(conn)
    web.extensions.db = db

    # 2. 挂载登录相关函数
    from app_login import account
    web.extensions.is_login = account.is_login
    web.extensions.get_userinfo = account.get_userinfo

    # 3. 挂载其它工具函数
    import utils
    web.utils = utils

load_extensions()

from webserver import app

wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
