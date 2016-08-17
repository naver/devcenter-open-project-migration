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
