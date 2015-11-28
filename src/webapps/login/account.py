# -*- coding: utf-8 -*-

import uuid
import logging
from datetime import datetime
import web
import json
from sqlalchemy import Column, Integer, String, DateTime

db = web.extensions.db


class User(db.ApiMixin, db.Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(128), index=True, nullable=False)
    usertype = Column(String(32), nullable=False)
    nickname = Column(String(128), nullable=False)
    password = Column(String(128))
    userdata = Column(String(8000), nullable=False)
    createtime = Column(DateTime, nullable=False)
    lastlogintime = Column(DateTime, nullable=False)
    lastloginip = Column(String(32))


class Session(db.ApiMixin, db.Base):
    __tablename__ = 'sessions'
    
    sessionid = Column(String(128), primary_key=True, nullable=False)
    activetime = Column(DateTime, nullable=False)
    data = Column(String(8000), nullable=False)

db.create_all()


def _setsession(sessionid, data):
    db_session = db.Session()
    user_session = Session(sessionid=sessionid, activetime=datetime.now(), data=json.dumps(data))
    db_session.add(user_session)
    db_session.commit()


def _getsession(sessionid):
    db_session = db.Session()
    user_session = db_session.query(Session).filter_by(sessionid=sessionid).first()
    return web.storage(json.loads(user_session.data))


def _delsession(sessionid):
    db_session = db.Session()
    user_session = db_session.query(Session).filter_by(sessionid=sessionid).first()
    if user_session:
        db_session.delete(user_session)


def _createaccount(username, usertype, nickname, password):
    db_session = db.Session()
    user = User(username=username, usertype=usertype, nickname=nickname, password=password,
                createtime=datetime.now(), lastlogintime=datetime.now(), lastloginip=web.ctx.ip,
                userdata='')
    db_session.add(user)
    db_session.commit()


def _getaccount(username, usertype):
    db_session = db.Session()
    user = db_session.query(User).filter_by(username=username, usertype=usertype).first()
    return user


def _touchaccount(username, usertype):
    db_session = db.Session()
    user = db_session.query(User).filter_by(username=username, usertype=usertype).first()
    user.lastlogintime = datetime.now()
    user.lastloginip = web.ctx.ip
    db_session.commit()


def _setaccountdata(username, usertype, userdata):
    db_session = db.Session()
    user = db_session.query(User).filter_by(username=username, usertype=usertype).first()
    user.userdata = json.dumps(userdata)
    db_session.commit()


def _getaccountdata(username, usertype, userdata):
    db_session = db.Session()
    user = db_session.query(User).filter_by(username=username, usertype=usertype).first()
    return web.storage(json.loads(user.userdata))


class LoginException(Exception):
    '''登录失败的异常'''
    pass


def _save_session(username, nickname, usertype):
    '''保存session'''
    sessionid = str(uuid.uuid1())
    web.setcookie('sessionid', sessionid, 60 * 60 * 24 * 365)
    web.setcookie('nickname', nickname, 60 * 60 * 24 * 365)
    _setsession(sessionid, dict(username=username, nickname=nickname, usertype=usertype))


def _check_session():
    '''检查session，未登录会抛出异常'''
    sessionid = web.cookies().get('sessionid')
    if not sessionid:
        raise LoginException('sessionid not found in cookies')
    if not _getsession(sessionid):
        raise LoginException('sessionid not found in sessions')
    session = _getsession(sessionid)
    return sessionid, session.username, session.usertype


def account_exists(username, usertype='me'):
    '''账户是否存在'''
    return bool(_getaccount(username, usertype))


def register_account(username, password, nickname, usertype='me'):
    '''注册新账户'''
    _createaccount(username=username, usertype=usertype, nickname=nickname, password=password)
    _save_session(username=username, nickname=nickname, usertype=usertype)
    return dict(code=200, message='register ok')


def login(username, password, nickname):
    '''登录'''
    usertype = 'me'
    account = _getaccount(username, usertype)
    if account.password != password:
        return dict(code=401, message='password invalid')

    return direct_login(username, nickname, usertype)

def direct_login(username, nickname, usertype):
    _touchaccount(username, usertype)
    _save_session(username=username, nickname=nickname, usertype=usertype)
    return dict(code=200, message='login ok')


def logout():
    '''退出登录'''
    try:
        sessionid, username, usertype = _check_session()
        web.setcookie('sessionid', sessionid, -1)
        web.setcookie('username', sessionid, -1)
        _delsession(sessionid)
        return dict(code=200, message='logout ok')
    except LoginException, le:
        return dict(code=400, message=le.message)


def is_login():
    '''是否登录'''
    sessionid = web.cookies().get('sessionid')
    logging.debug('is_login:sessionid=%s', sessionid)
    if not sessionid:
        return False
    if not _getsession(sessionid):
        return False
    return True


def get_userinfo():
    '''获取用户信息'''
    try:
        sessionid, username, usertype = _check_session()
        userinfo = _getaccount(username, usertype)
        userinfo.password = ''  # 防止密码被下发到客户端
        return dict(code=200, message='ok', data=userinfo.as_dict())
    except LoginException, le:
        return dict(code=400, message=le.message)


def update_userinfo(data):
    '''更新用户信息'''
    try:
        sessionid, username, usertype = _check_session()
        userinfo = _getaccount(username, usertype)
        userinfo.update(data)
        _setaccountdata(username, usertype, userinfo)
        return dict(code=200, message='ok', data=userinfo)
    except LoginException, le:
        return dict(code=400, message=le.message)
