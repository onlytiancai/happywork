# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
import web

db = web.extensions.db
app_jslink = '<script src="/static/sea-modules/seajs/1.3.0/sea-debug.js" data-main="/static/apps/todo/todo-main"></script>'
app_desc = '待办列表'


def _get_userid():
    userid = 0
    if web.extensions.is_login():
        userinfo = web.storage(web.extensions.get_userinfo()['data'])
        userid = userinfo.id
    return userid


class Todo(db.ApiMixin, db.Base):
    __tablename__ = 'todos_v2'
    
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, index=True, nullable=False)
    tag = Column(String(32))
    createtime = Column(DateTime, nullable=False)
    donetime = Column(DateTime)
    starttime = Column(DateTime)
    deadlinetime = Column(DateTime)
    archivetime = Column(DateTime)

    title = Column(String(256), nullable=False)
    order = Column(Integer, nullable=False)
    done = Column(Boolean)
    started = Column(Boolean)
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
    userid = Column(Integer, index=True, nullable=False)
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


db.create_all()

urls = [
        "/todos", Todo,
        "/todos/([^/]+)", Todo,
        "/tags", TodoTag,
        "/tags/([^/]+)", TodoTag,
        ]
