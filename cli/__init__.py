# -*- coding: utf-8 -*-
import os

from migration.helper import set_encoding

set_encoding()

CUR_DIR = os.getcwd()
DIRS = ('data', 'logs', 'Nforge')

for dir_name in DIRS:
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
