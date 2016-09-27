# -*- coding: utf-8 -*-
"""
nforge_migration
~~~~~~~~~~~~~~~~~~~~~~

nforge 마이그레이션

:copyright: (c) 2016 by Taehwan Kim <maxtortime@navercorp.com>.
:license: None
"""
import re

from .helper import set_encoding

set_encoding()

WAIT_TIME = 5
ASSET_DIR = 'files'
CODE_INFO_FILE = 'code_info.json'
DOWNLOADS_DIR = 'downloads'
ISSUES_DIR = 'issues'
ISSUE_ATTACH_DIR = 'attachFile'
MILESTONES_DIR = 'milestones'
ok_code = re.compile('20\d')
fail_code = re.compile('40\d')
PARSING_OUTPUT_DIR = 'Nforge'
