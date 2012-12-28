# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import web
from datetime import datetime

db = web.extensions.db
ensure_login = web.extensions.ensure_login


def _get_userid():
    userid = 0 
    if web.app_extensions.is_login():
        userinfo = web.storage(web.app_extensions.get_userinfo()['data'])
        userid = userinfo.id
    return userid 


class Todo(db.ApiMixin, db.Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, index=True, nullable=False)
    tag = Column(String(32))
    createtime = Column(DateTime, nullable=False)
    donetime = Column(DateTime)
    archivetime = Column(DateTime)

    title = Column(String(256), nullable=False)
    order = Column(Integer, nullable=False)
    done = Column(Boolean)
    archived = Column(Boolean)

    def on_insert(self, data):
        data.update(userid=_get_userid(), createtime=datetime.now())
        return data

    def on_select(self, data):
        data.update(userid=_get_userid())
        return data

    def on_update(self, data):
        data.update(userid=_get_userid())
        return data

    def on_delete(self, data):
        data.update(userid=_get_userid())
        return data


class TodoTag(db.ApiMixin, db.Base):
    __tablename__ = 'todo_tags'
    id = Column(Integer, primary_key=True)
    userid= Column(Integer, index=True, nullable=False)
    tag = Column(String(32))

    def on_insert(self, data):
        data.update(userid=_get_userid())
        return data

    def on_select(self, data):
        data.update(userid=_get_userid())
        return data

    def on_update(self, data):
        data.update(userid=_get_userid())
        return data

    def on_delete(self, data):
        data.update(userid=_get_userid())
        return data
