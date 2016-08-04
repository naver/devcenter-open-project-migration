# -*- coding: utf-8 -*-
import os
import re

__version__ = '0.11-dev'

API_URLS = ['https://api.github.com/', 'https://oss.navercorp.com/api/v3/']
TOKEN_FILE_NAMES = ['GITHUB_ACCESS_TOKEN', 'ENTERPRISE_ACCESS_TOKEN']
REPO_LIST_FILE_NAMES = ['GITHUB_REPO_LIST', 'ENTERPRISE_REPO_LIST']
DATA_DIR = 'data'
PARSING_OUTPUT_DIR = 'parsing_output'
# 소스 코드 저장소 마이그레이션 완료 동안 기다리는 시간
WAIT_TIME = 5
WIKI_DIR = 'wiki_repo'
COOKIE_FILE = 'COOKIES'
COOKIE_PATH = os.path.join(DATA_DIR, COOKIE_FILE)
ASSET_DIR = 'files'
CODE_INFO_FILE = 'code_info.json'

DOWNLOADS_DIR = 'downloads'
ISSUES_DIR = 'issues'
ISSUE_ATTACH_DIR = 'attachFile'
MILESTONES_DIR = 'milestones'

FILE_NAMES = dict(token=TOKEN_FILE_NAMES, repo=REPO_LIST_FILE_NAMES)

MODES = dict(
    QUIT='Q',
    MAKE_REPO='M',
    REMOVE_REPO='R',
    LINK_REPO='L',
    NORMAL='N'
    )

ok_code = re.compile('20\d')


def get_file_path(file_type, enterprise):
    return os.path.join(DATA_DIR, FILE_NAMES[file_type][enterprise])
