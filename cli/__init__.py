# -*- coding: utf-8 -*-
import logging
import os

import time

CUR_DIR = os.getcwd()
DATA_DIR = 'data'
LOGS_DIR = 'logs'

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'), level=logging.ERROR)
PARSING_OUTPUT_DIR = 'Nforge'
API_URLS = ['https://api.github.com/', 'https://oss.navercorp.com/api/v3/']
TOKEN_FILE_NAMES = ['GITHUB_ACCESS_TOKEN', 'ENTERPRISE_ACCESS_TOKEN']
REPO_LIST_FILE_NAMES = ['GITHUB_REPO_LIST', 'ENTERPRISE_REPO_LIST']

FILE_NAMES = dict(token=TOKEN_FILE_NAMES, repo=REPO_LIST_FILE_NAMES)

