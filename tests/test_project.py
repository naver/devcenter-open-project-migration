#!env python
# -*- coding: utf-8 -*-
import os
import random
import unittest

from migration.helper import get_random_string
from migration.project import Project, InvalidProjectError


class TestProject(unittest.TestCase):
    valid_projects = dict(
        d2coding=['okgosu', 'openapi'],
        nforge=['junoyoonkr', 'kss', 'nori', 'tiny657', '리쯔', 'Piseth',
                'chanraksmey', 'cheng900', 'darayong', 'manithnoun', 'rathapovkh',
                'wkpark', '졸린눈이'],
        asd=['xowns24']
    )

    front_page = str()
    license = str()

    with open(os.path.join('wiki_repos', 'd2coding_FrontPage')) as f:
        for line in f:
            front_page += line

    with open(os.path.join('wiki_repos', 'd2coding_OpenFontLicense')) as f:
        for line in f:
            license += line

    wiki_pages = dict(
        d2coding=dict(
            FrontPage=front_page,
            OpenFontLicense=license
        )
    )

    naver_api_url = 'http://staging.dev.naver.com'

    project_name = random.choice(list(valid_projects.keys()))
    project = Project(project_name, naver_api_url)

    def test_constructor(self):
        try:
            test_project = Project(self.project_name, self.naver_api_url)
        except InvalidProjectError as e:
            self.fail(e)

        self.assertTrue(isinstance(test_project, Project))
        self.assertEqual(test_project._project_name, self.project_name)

    def test_invalid_project(self):
        with self.assertRaises(InvalidProjectError):
            Project(get_random_string(10), self.naver_api_url)

    def test_get_developers(self):
        self.assertEqual(sorted(self.project._developers),
                         sorted(self.valid_projects.get(
                             self.project._project_name)))

    def test_get_issues(self):
        pass

    def test_get_vcs(self):
        # URL/src 를 making_soup 한 다음
        # soup에서 div code_contents 클래스가 있으면 svn
        # 아니면 git 으로 판단하자
        d2coding = Project('d2coding', self.naver_api_url)
        cubrid = Project('cubrid', self.naver_api_url)
        parkjongkyoung = Project('parkjongkyoung', self.naver_api_url)

        self.assertEqual(d2coding._vcs, 'svn')
        self.assertEqual(cubrid._vcs, 'svn')
        self.assertEqual(parkjongkyoung._vcs, 'git')

    def test_get_wiki(self):
        d2coding = Project('d2coding', self.naver_api_url)
        self.maxDiff = None

        self.assertMultiLineEqual(d2coding.wiki_pages['FrontPage'],
                                  self.wiki_pages['d2coding']['FrontPage'])
        self.assertMultiLineEqual(d2coding.wiki_pages['OpenFontLicense'],
                                  self.wiki_pages['d2coding']['OpenFontLicense'])


if __name__ == '__main__':
    unittest.main()
