# -*- coding: utf-8 -*-
import logging
import os
import re
import time

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
PARSING_OUTPUT_DIR = 'Nforge'
