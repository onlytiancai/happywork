# -*- coding: utf-8 -*-

from webserver import app
wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
