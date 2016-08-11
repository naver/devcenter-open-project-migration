# -*- coding: utf-8 -*-
import logging
import os

import time

__version__ = '0.11-dev'

CUR_DIR = os.getcwd()
logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'), level=logging.ERROR)
PARSING_OUTPUT_DIR = 'Nforge'
API_URLS = ['https://api.github.com/', 'https://oss.navercorp.com/api/v3/']
TOKEN_FILE_NAMES = ['GITHUB_ACCESS_TOKEN', 'ENTERPRISE_ACCESS_TOKEN']
REPO_LIST_FILE_NAMES = ['GITHUB_REPO_LIST', 'ENTERPRISE_REPO_LIST']
DATA_DIR = 'data'
FILE_NAMES = dict(token=TOKEN_FILE_NAMES, repo=REPO_LIST_FILE_NAMES)

