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
import os
import re
import unittest

from migration.helper import making_soup
from migration.nforge_parser import NforgeParser


class TestNforgeParser(unittest.TestCase):
    path = os.path.join('Nforge', 'open_project', 'd2coding')
    nfp = NforgeParser(path)

    with open(os.path.join(path, 'issues', 'xml', 'issue', '98590.xml')) as f:
        soup = making_soup(f.read(), 'xml')

    items = soup.attachments.findAll('item')
    nfp.make_issue_json()

    def test_attach_links(self):
        attach_link = self.nfp.attach_links(items=self.items, content_id='98590')
        m = re.findall('\(\{0\}/wiki/attachFile.*\)', attach_link)
        self.assertTrue(len(m) > 0)

if __name__ == '__main__':
    unittest.main()
