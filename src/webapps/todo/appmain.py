# -*- coding: utf-8 -*-
import web
from .models.todos import Todo, TodoTag
db = web.extensions.db

app_jslink = '<script src="/static/sea-modules/seajs/1.3.0/sea-debug.js" data-main="/todo/static/todo-main"></script>'
app_desc = '待办列表'

db.create_all()

urls = [
        "/todos", Todo,
        "/todos/([^/]+)", Todo,
        "/tags", TodoTag,
        "/tags/([^/]+)", TodoTag,
        ]
