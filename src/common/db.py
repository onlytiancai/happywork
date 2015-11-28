# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query
import sqlalchemy.types
from sqlalchemy.pool import NullPool
import json
import web


Session = sessionmaker()
Base = declarative_base()
engine = None


def json_output(f):
    def inner(*args, **kargs):
        result = f(*args, **kargs)
        if isinstance(result, query.Query):
            result = json.dumps([row.as_dict() for row in result])
        if isinstance(result, ApiMixin):
            result = json.dumps(result.as_dict())
        web.header('Content-Type', 'application/json')
        return result

    return inner


def input(*requireds, **defaults):
    i = web.input(*requireds, **defaults)
    content_type = web.ctx.env.get('CONTENT_TYPE')
    if web.data():
        if content_type is None or content_type.find('json') != -1:
            try:
                json_input = json.loads(web.data())
            except ValueError:
                raise web.NotAcceptable()
            i.update(json_input)

    return i


class ApiMixin(object):
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __mapper_args__ = {'always_refresh': True}

    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(c.type, sqlalchemy.types.DateTime) and value is not None:
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            result[c.name] = value
        return result
    
    def on_insert(data):
        return data

    def on_select(data):
        return data

    def on_update(data):
        return data

    def on_delete(data):
        return data

    @json_output
    def POST(self):
        kargs = self.on_insert(input())
        session = Session()
        todo = self.__class__(**kargs)

        session.add(todo)
        session.commit()
        return todo

    @json_output
    def GET(self, id=None):
        kargs = self.on_select(input())
        session = Session()
        if not id:
            return session.query(self.__class__).filter_by(**kargs)

        todo = session.query(self.__class__).filter_by(id=id, **kargs).first()
        if not todo:
            raise web.notfound()
        return todo

    @json_output
    def PUT(self, id):
        kargs = self.on_update(input())
        session = Session()
        
        del kargs['id']
        todo = session.query(self.__class__).filter_by(id=id).first()
        if not todo:
            raise web.notfound()

        for k, v in kargs.items():
            setattr(todo, k, v)
        
        session.commit()
        return todo

    @json_output
    def DELETE(self, id):
        session = Session()

        todo = session.query(self.__class__).filter_by(id=id).first()
        if not todo:
            raise web.notfound()

        session.delete(todo)
        session.commit()


def init(db_conn):
    global engine
    engine = create_engine(db_conn, connect_args={'charset': 'utf8'}, poolclass=NullPool)
    Session.configure(bind=engine)


def create_all():
    if engine is None:
        raise Exception('engine is not inited')

    Base.metadata.create_all(engine)
