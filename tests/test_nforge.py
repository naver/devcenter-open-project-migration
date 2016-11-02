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
import hashlib
import unittest

from migration.exception import NoSrcError
from migration.nforge import InvalidProjectError
from migration.nforge import Nforge


class TestNforge(unittest.TestCase):
    valid_pr_name = 'd2coding'
    test_d2coding = Nforge(project_name=valid_pr_name, dev_code=False, private=False)
    # sha1 hash file
    d2coding_wiki_docs = {'FrontPage': 'fc1ede112bc7f117dc5d4f89db6478a2d13c06a8',
                          'OpenFontLicense': 'e4575441fb9b826e243d7a76622686d7923835cb'}
    invalid_name = '!245sad'

    def test_invalid_project_error(self):
        with self.assertRaises(InvalidProjectError):
            invalid_pr = Nforge(project_name=self.invalid_name, dev_code=False, private=False)
            self.assertIsNone(invalid_pr)

        self.assertIsInstance(self.test_d2coding, cls=Nforge)

        d2coding = Nforge(project_name=self.valid_pr_name, dev_code=False, private=False)
        self.assertIsInstance(d2coding, cls=Nforge)

    def test_wiki(self):
        wiki = self.test_d2coding.wiki()

        for name, doc in self.d2coding_wiki_docs.items():
            wiki_doc = wiki[name]
            self.assertEqual(hashlib.sha1(wiki_doc.encode('utf-8')).hexdigest(), doc)


if __name__ == '__main__':
    unittest.main()
