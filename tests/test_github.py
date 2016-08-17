import os
import re
import unittest

from cli.github_token_cli import read_token_from_file, get_file_path
from migration.github import GitHubSession, GithubMigration


class TestGitHub(unittest.TestCase):
    os.chdir('..')
    path = os.path.join('Nforge', 'open_project', 'd2coding')
    enterprise = False
    valid_token = read_token_from_file(get_file_path('token', enterprise), enterprise)

    ghs = GitHubSession(enterprise=enterprise, token=valid_token, path=path, repo_name='d2coding-testing')
    ghm = GithubMigration(session=ghs)

    def test_read_json(self):
        # testing only has attachments
        for each_file in self.ghm.issues:
            if re.match('### Attachments', each_file):
                m = re.findall('\(https://github.com/maxtortime/d2coding-testing/wiki/attachFile.*\)', each_file)
                print(m)
                self.assertTrue(len(m) > 0)
            else:
                continue

if __name__ == '__main__':
    unittest.main()
