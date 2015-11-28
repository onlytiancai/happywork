# -*- coding: utf-8 -*-
import logging
logging.getLogger().setLevel(logging.NOTSET)

sitename = "Happy Work"
default_app = 'app_todo'
web_url = ('0.0.0.0', 8803)
use_SAE = False
dbname = 'happywork'
dbuser = 'root'
dbpassword = ''
dbhost = ''
dbport = 3306 

def reload_config():
    '加载真实配置'
    try:
        app_config = __import__('config_real')
        items = [(k, v) for k, v in app_config.__dict__.items()
                 if not k.startswith('__')]
        globals().update(dict(items))
    except ImportError:
        pass

reload_config()
