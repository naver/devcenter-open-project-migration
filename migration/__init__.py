# -*- coding: utf-8 -*-
import re

__version__ = '0.11-dev'

# 소스 코드 저장소 마이그레이션 완료 동안 기다리는 시간
WAIT_TIME = 5
ASSET_DIR = 'files'
CODE_INFO_FILE = 'code_info.json'
DOWNLOADS_DIR = 'downloads'
ISSUES_DIR = 'issues'
ISSUE_ATTACH_DIR = 'attachFile'
MILESTONES_DIR = 'milestones'
ok_code = re.compile('20\d')
