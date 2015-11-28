# -*- coding: utf-8 -*-
import web

import config


def ensure_login(f):
    def inner(*args, **kargs):
        if not web.app_extensions.is_login():
            raise web.unauthorized()
        return f(*args, **kargs)
    return inner


def get_conn():
    db_conn = "mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8"
    if config.use_SAE:
        import sae.const
        db_conn = db_conn % dict(db=sae.const.MYSQL_DB,
                                 user=sae.const.MYSQL_USER,
                                 password=sae.const.MYSQL_PASS,
                                 host=sae.const.MYSQL_HOST,
                                 port=int(sae.const.MYSQL_PORT)
                                 )
    else:
        db_conn = db_conn % dict(db=config.dbname,
                                 user=config.dbuser,
                                 password=config.dbpassword,
                                 host=config.dbhost,
                                 port=config.dbport
                                 )
    return db_conn


def load_extensions():
    from common import db
    db.init(get_conn())
    web.extensions = web.storage()
    web.extensions.db = db
    web.extensions.ensure_login = ensure_login

    web.app_extensions = web.storage()
