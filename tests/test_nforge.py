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
import unittest

from nforge import InvalidProjectError
from nforge import Nforge


class TestNforge(unittest.TestCase):
    valid_pr_name = 'd2coding'
    d2coding_wiki_docs = ('FrontPage', 'OpenFontLicense')
    invalid_name = '!245sad'

    def test_nforge(self):
        with self.assertRaises(InvalidProjectError):
            invalid_pr = Nforge(project_name=self.invalid_name, dev_code=False, need_cookies=False)
            self.assertIsNone(invalid_pr)

        d2coding = Nforge(project_name=self.valid_pr_name, dev_code=False, need_cookies=False)
        self.assertIsInstance(d2coding, cls=Nforge)

        for doc_name in d2coding.wiki():
            self.assertTrue(doc_name in self.d2coding_wiki_docs)


if __name__ == '__main__':
    unittest.main()
