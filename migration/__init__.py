# -*- coding: utf-8 -*-
import logging
import os
import re
import time

from .helper import set_encoding

set_encoding()
__version__ = '0.11-dev'

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

# TODO: logging.basicConfig shows error at Windows because of log file path
if not os.name == 'nt':
    logging.basicConfig(filename=os.path.join('logs',
                                              time.strftime("%Y-%m-%d %H:%M:%S") + '.log'), level=logging.ERROR)
