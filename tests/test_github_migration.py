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

import requests
from future.backports.urllib.parse import urljoin
from migration.github import GitHubMigration, InvalidTokenError


class TestGitHubMigration(unittest.TestCase):
    valid_token = os.environ['GITHUB_ACCESS_TOKEN']
    invalid_token = 'This is a invalid token'
    repo_name = 'testing'
    project_path = 'Nforge/open_project/d2coding'

    def test_GitHubMigration(self):
        valid_manager = GitHubMigration(enterprise=False, token=self.valid_token, repo_name=self.repo_name,
                                          project_path=self.project_path)

        self.assertIsNotNone(valid_manager)
        self.assertTrue(valid_manager.token, self.valid_token)
        self.assertEqual(valid_manager.username, 'maxtortime')
        self.assertEqual(valid_manager.repo_name, self.repo_name)

        # Should get repository on github
        repo_get_rq = requests.request('GET', urljoin(valid_manager.url,
                                                      valid_manager.username + '/' + valid_manager.repo_name))
        self.assertEqual(repo_get_rq.status_code, 200)
        with self.assertRaises(InvalidTokenError):
            invalid_gm = GitHubMigration(enterprise=False, token=self.invalid_token, repo_name=self.repo_name,
                                         project_path=self.project_path)
            # Raised exception also invalid_gm is NoneType object.
            self.assertIsNone(invalid_gm)

    def test_read_json(self):
        # testing only has attachments
        ghm = GitHubMigration(enterprise=False, token=self.valid_token, project_path=self.project_path,
                              repo_name=self.repo_name)

        for each_file in ghm.issues:
            if re.match('### Attachments', each_file):
                m = re.findall('\(https://github.com/maxtortime/d2coding-testing/wiki/attachFile.*\)', each_file)
                print(m)
                self.assertTrue(len(m) > 0)
            else:
                continue

    def test_read_downloads(self):
        ghm = GitHubMigration(False, 'd2coding-migration', 'Nforge/open_project/d2coding', token=self.valid_token)

        download = ghm.read_downloads()

        for download_dict in download.values():
            self.assertTrue(type(download_dict) is dict)


    def test_valid_download_migration(self):
        ghm = GitHubMigration(False, 'd2coding-migration', 'Nforge/open_project/d2coding', token=self.valid_token)

        self.assertTrue(ghm.downloads_migration())


if __name__ == '__main__':
    unittest.main()
