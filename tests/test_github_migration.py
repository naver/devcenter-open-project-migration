import re
import unittest

import requests
from future.backports.urllib.parse import urljoin
from migration.github import GitHubMigration, InvalidTokenError


class TestGitHubMigration(unittest.TestCase):
    test_token_file_names = ('data/GITHUB_ACCESS_TOKEN.backup', 'data/ENTERPRISE_ACCESS_TOKEN.backup')
    valid_tokens = list()
    invalid_token = 'This is a invalid token'
    repo_name = 'testing'
    project_path = 'Nforge/open_project/d2coding'

    # read token from backup token files
    for fn in test_token_file_names:
        with open(fn) as test_token_file:
            valid_tokens.append(test_token_file.read())

    def test_GitHubMigration(self):
        for ent in range(len(self.valid_tokens)):
            valid_managers = (GitHubMigration(enterprise=ent, token=self.valid_tokens[ent], repo_name=self.repo_name,
                                              project_path=self.project_path),
                              GitHubMigration(enterprise=ent, repo_name=self.repo_name, project_path=self.project_path))

            for valid_manager in valid_managers:
                self.assertIsNotNone(valid_manager)
                self.assertTrue(valid_manager.token, self.valid_tokens[valid_manager.enterprise])
                self.assertEqual(valid_manager.username, 'maxtortime')
                self.assertEqual(valid_manager.repo_name, self.repo_name)

                # Should get repository on github
                repo_get_rq = requests.request('GET', urljoin(valid_manager.url,
                                                              valid_manager.username + '/' + valid_manager.repo_name))
                self.assertEqual(repo_get_rq.status_code, 200)

            with self.assertRaises(InvalidTokenError):
                invalid_gm = GitHubMigration(enterprise=ent, token=self.invalid_token, repo_name=self.repo_name,
                                             project_path=self.project_path)
                # Raised exception also invalid_gm is NoneType object.
                self.assertIsNone(invalid_gm)

    def test_read_json(self):
        # testing only has attachments
        ghm = GitHubMigration(enterprise=False, token=self.valid_tokens[False], project_path=self.project_path,
                              repo_name=self.repo_name)

        for each_file in ghm.issues:
            if re.match('### Attachments', each_file):
                m = re.findall('\(https://github.com/maxtortime/d2coding-testing/wiki/attachFile.*\)', each_file)
                print(m)
                self.assertTrue(len(m) > 0)
            else:
                continue

    def test_download_migration(self):
        ghm = GitHubMigration(enterprise=True, token=self.valid_tokens[True], project_path=self.project_path,
                              repo_name='asd')

        self.assertFalse(ghm.downloads_migration())

if __name__ == '__main__':
    unittest.main()
