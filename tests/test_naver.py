# -*- coding: utf-8 -*-
import unittest
from migration.naver import Naver
from migration.github import Github
from credentials import *

class TestNaver(unittest.TestCase):
    gh = Github(GITHUB_ID,GITHUB_PW,'nforge-test')
    test_inst = Naver(NAVER_ID,NAVER_PW,'nforge',gh)

    nforge_urls = dict(QnA='http://staging.dev.naver.com/projects/nforge/forum.xml',
                       Features='http://staging.dev.naver.com/projects/nforge/feature.xml',
                       Bugs='http://staging.dev.naver.com/projects/nforge/issue.xml',
                       CodeReview='http://staging.dev.naver.com/projects/nforge/review.xml',
                       testing='http://staging.dev.naver.com/projects/nforge/testing.xml',
                       download='http://staging.dev.naver.com/projects/nforge/download.xml')

    def test_create_url(self):
        self.maxDiff = None
        self.assertEqual(self.test_inst.create_url(),self.nforge_urls)


if __name__ == '__main__':
    unittest.main()
