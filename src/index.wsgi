# -*- coding: utf-8 -*-

import sae
import logging
logging.getLogger().setLevel(logging.NOTSET)

import webserver
application = sae.create_wsgi_app(webserver.app.wsgifunc())
