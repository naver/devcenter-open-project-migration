# -*- coding: utf-8 -*-
import logging
import os
import time

from migration.helper import set_encoding

set_encoding()

CUR_DIR = os.getcwd()
DATA_DIR = 'data'
LOGS_DIR = 'logs'

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'), level=logging.ERROR)
PARSING_OUTPUT_DIR = 'Nforge'
