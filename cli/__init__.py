# -*- coding: utf-8 -*-
import logging
import os
import time

from migration.helper import set_encoding

set_encoding()

CUR_DIR = os.getcwd()
DIRS = ('data', 'logs', 'Nforge')

for dir_name in DIRS:
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

# TODO: logging.basicConfig shows error at Windows because of log file path
if not os.name == 'nt':
    logging.basicConfig(filename=os.path.join(DIRS[1], time.strftime("%Y-%m-%d %H:%M:%S") + '.log'),
                        level=logging.ERROR)
