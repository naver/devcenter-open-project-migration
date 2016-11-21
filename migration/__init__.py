# -*- coding: utf-8 -*-
"""
   Copyright 2016 NAVER Corp.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import re

from .helper import set_encoding

set_encoding()

__version__ = '1.1.0.post2'
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
