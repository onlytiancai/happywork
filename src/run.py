# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

import config


def start():
    import webserver
    WSGIServer(config.web_url, webserver.app.wsgifunc()).serve_forever()

if __name__ == '__main__':
    start()
