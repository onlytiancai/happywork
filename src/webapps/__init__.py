# -*- coding: utf-8 -*-
import os

apps = []

curdir = os.path.dirname(__file__)
for file in os.listdir(curdir):
    if os.path.isdir(os.path.join(curdir, file)) and not file.startswith('.'):
        eval_str = ("from .%(dirname)s import appmain as %(dirname)s\n"
                    "%(dirname)s.app_name = '%(dirname)s'\n"
                    "apps.append(%(dirname)s)")
        eval_str = eval_str % dict(dirname=file)
        exec eval_str
