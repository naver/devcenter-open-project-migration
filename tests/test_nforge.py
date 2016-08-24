import unittest

from nforge import InvalidProjectError
from nforge import Nforge


class TestNforge(unittest.TestCase):
    valid_pr_name = 'd2coding'
    d2coding_wiki_docs = ('FrontPage', 'OpenFontLicense')
    invalid_name = '!245sad'

    def test_nforge(self):
        with self.assertRaises(InvalidProjectError):
            invalid_pr = Nforge(project_name=self.invalid_name, dev_code=False)
            self.assertIsNone(invalid_pr)

        d2coding = Nforge(project_name=self.valid_pr_name, dev_code=False)
        self.assertIsInstance(d2coding, cls=Nforge)

        for doc_name in d2coding.wiki():
            self.assertTrue(doc_name in self.d2coding_wiki_docs)


if __name__ == '__main__':
    unittest.main()
