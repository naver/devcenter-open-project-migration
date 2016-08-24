import unittest

import requests
from migration.helper import making_soup


class Nforge:
    NFORGE_URLS = ('http://staging.dev.naver.com/', 'http://devcode.nhncorp.com/')

    def __init__(self, project_name, is_dev_code):
        self.url = self.NFORGE_URLS[is_dev_code] + 'projects/' + project_name

        # parsing main page of project for get title
        soup = making_soup(requests.request('GET', self.url).text, 'html')

        if '오류' in soup.title.get_text() or not soup:
            # It means this project is invalid project
            # Therefore it doesn't create object.
            raise ValueError

        self.wiki = dict(OpenFontLicense='', FrontPage='')


class TestNforge(unittest.TestCase):
    valid_pr_name = 'd2coding'
    d2coding_wiki_docs = ('FrontPage', 'OpenFontLicense')
    invalid_name = '!245sad'

    def test_nforge(self):
        with self.assertRaises(ValueError):
            invalid_pr = Nforge(project_name=self.invalid_name, is_dev_code=False)
            self.assertIsNone(invalid_pr)

        d2coding = Nforge(project_name=self.valid_pr_name, is_dev_code=False)
        self.assertIsInstance(d2coding, cls=Nforge)

        for doc_name in d2coding.wiki.keys():
            self.assertTrue(doc_name in self.d2coding_wiki_docs)

if __name__ == '__main__':
    unittest.main()
