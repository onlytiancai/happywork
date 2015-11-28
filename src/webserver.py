# -*- coding: utf-8 -*-

import web
import os
import mimetypes
import operator

import config
import extension

web.config.debug = True

curdir = os.path.dirname(__file__)
menus = []                          # 主菜单，动态生成
app_jslinks = {}                    # 每个app单独加载的js
jslinks = []                        # 始终会加载的js

render = web.template.render(os.path.join(curdir, 'templates/'))


def send_file(file):
    print file
    if not os.path.exists(file):
        raise web.notfound()

    content_type, encoding = mimetypes.guess_type(file)
    if content_type is not None:
        web.header('Content-Type', content_type, unique=True)

    with open(file) as f:
        return f.read()


class index(object):
    def GET(self, app=None):
        if not app and hasattr(config, 'default_app'):
            raise web.Redirect('/' + config.default_app + '/index.html')
        model = web.storage(jslinks=jslinks, app_jslink=app_jslinks.get(app, ''), menus=menus, sitename=config.sitename)
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        return render.index(model)


class static(object):
    def GET(self, file):
        return send_file(os.path.join(curdir, 'static', file))


class appstatic(object):
    def GET(self, app, file):
        return send_file(os.path.join(curdir, 'webapps', app, 'static', file))


urls = ["/", 'index',
        "/static/(.*)", 'static',               # 静态文件
        "/([^\/]*)/static/(.*)", 'appstatic',   # app静态文件
        "/([^\/]*)/index.html", 'index',        # app首页
        ]


def load_apps():
    import webapps

    for app in webapps.apps:
        if hasattr(app, 'app_desc'):  # 如果设置了菜单名则注册到菜单
            menus.append(web.storage(name='/%s/index.html' % app.app_name, desc=app.app_desc))

        if hasattr(app, 'app_jslink'):
            app_jslinks[app.app_name] = app.app_jslink

        if hasattr(app, 'jslink'):  # 如果设置了全局js，则添加到全局js
            jslinks.append(app.jslink)

        app_urls = app.urls
        map(lambda i: operator.setitem(app_urls, i, '/%s%s' % (app.app_name, app_urls[i])), range(0, len(app_urls), 2))
        urls.extend(app_urls)

extension.load_extensions()
load_apps()
app = web.application(urls, globals())
