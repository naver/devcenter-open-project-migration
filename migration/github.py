# -*- coding: utf-8 -*-
import glob
import json
import mimetypes
import os
import subprocess
import time
from urllib.parse import urlparse

import click
import github3
import grequests
import requests
from github3.exceptions import GitHubError
from .helper import get_fn, chunks
from migration import WAIT_TIME, CODE_INFO_FILE, ok_code, ISSUES_DIR, DOWNLOADS_DIR
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def exception_handler(request, exception):
    print(exception)


class GitHubSession:
    urls = ['https://github.com', 'https://oss.navercorp.com']

    def __init__(self, token, enterprise, repo_name, path):
        self.url = self.urls[enterprise]
        self.token = token
        self.enterprise = enterprise
        self.path = path
        self.cur_dir = os.path.abspath(os.curdir)

        self.session = github3.login(token=token) \
            if not enterprise else github3.GitHubEnterprise(self.url, token=token)

        self.api_url = self.session.__dict__['_session'].__dict__['base_url']

        self.username = self.session.user().login
        self.repo = self.session.repository(owner=self.username, repository=repo_name)

        if not self.repo:
            self.repo = self.session.create_repo(repo_name)

        self.repo_name = repo_name

    def make_github_info(self):
        with open(os.path.join(self.path, 'github_info.json'), 'w') as github_info:
            json.dump(dict(
                enterprise=self.enterprise,
                token=self.token,
                repo_name=self.repo_name
            ), github_info)


class GithubMigration(GitHubSession):
    header_basis = {
        'authorization': "token ",
        'content-type': "application/json",
    }

    def __init__(self, **kwargs):
        # 헤더 정의
        session = kwargs.get('session')

        if not session:
            token = kwargs.get('token')
            enterprise = kwargs.get('enterprise')
            repo_name = kwargs.get('repo_name')
            path = kwargs.get('path')

            super(GithubMigration, self).__init__(token, enterprise, repo_name, path)
        else:
            for k, v in session.__dict__.items():
                self.__dict__[k] = v

        self.header_basis['authorization'] += self.token

        self.basic_header = self.header_basis.copy()
        self.issue_header = self.header_basis.copy()
        self.repo_header = self.header_basis.copy()

        self.basic_header['Accept'] = 'application/vnd.github.v3+json'
        self.issue_header['Accept'] = 'application/vnd.github.golden-comet-preview'
        self.repo_header['Accept'] = 'application/vnd.github.barred-rock-preview'

        self.basis_repo_url = '{0}/repos/{1}/{2}'.format(self.api_url, self.username, self.repo_name)
        self.import_repo_url = self.basis_repo_url + '/import'
        self.import_issue_url = self.import_repo_url + '/issues'

        self.issues = self.read_issue_json()
        self.downloads = self.read_downloads()

    def read_issue_json(self):
        files = []

        path = os.path.join(self.path, ISSUES_DIR, 'json', '*.json')
        json_list = glob.glob(path)

        for fn in json_list:
            with open(fn) as json_text:
                read_file = json_text.read()
                files.append(read_file)

        return files

    def read_downloads(self):
        downloads_path = os.path.join(self.path, DOWNLOADS_DIR)
        json_path = os.path.join(downloads_path, 'json', '*.json')
        raw_path = os.path.join(downloads_path, 'raw')

        downloads = dict()

        for file_path in glob.glob(json_path):
            download_id = get_fn(file_path, 0)
            downloads[download_id] = dict()

            with open(file_path) as json_text:
                downloads[download_id]['json'] = json.loads(json_text.read())

        for download_id in os.listdir(raw_path):
            downloads[download_id]['raw'] = list()

            for file_path in glob.glob(os.path.join(raw_path, download_id, '*.*')):
                file_name = get_fn(file_path)
                ext = get_fn(file_path, 1)

                try:
                    content_type = mimetypes.types_map[ext]
                except KeyError:
                    content_type = 'multipart/form-data'

                with open(file_path, 'rb') as raw_file:
                    downloads[download_id]['raw'].append(dict(
                        name=file_name,
                        raw=raw_file.read(),
                        content_type=content_type
                    ))

        return downloads

    def issues_migration(self):
        issue_split = list(chunks(self.issues, 30))

        for issues in issue_split:
            irs = (grequests.post(self.import_issue_url, data=issue, headers=self.issue_header) for issue in issues)
            import_issues = grequests.map(irs, exception_handler=exception_handler)

            for response in import_issues:
                if not ok_code.match(str(response.status_code)):
                    return False

        self.upload_issue_attach()
        return True

    def upload_issue_attach(self):
        github = urlparse(self.url).netloc
        push_wiki_git = 'https://{0}:{1}@{3}/{0}/{2}.wiki.git'.format(self.username, self.token, self.repo_name, github)

        os.chdir(os.path.join(self.path, ISSUES_DIR, 'raw'))

        git_commands = [
            ['git', 'init'],
            ['git', 'add', '--all'],
            ['git', 'commit', '-m', 'all asset commit'],
            ['git', 'remote', 'add', 'origin', push_wiki_git],
            ['git', 'pull', '-f', push_wiki_git, 'master'],
            ['git', 'push', '-f', push_wiki_git, 'master']
        ]

        for command in git_commands:
            subprocess.call(command)

        os.chdir(self.cur_dir)

    def repo_migration(self):
        with open(os.path.join(self.path, CODE_INFO_FILE)) as code_info:
            r = requests.request("PUT", self.import_repo_url, data=code_info.read().encode('utf-8'),
                                 headers=self.repo_header)

        return True if ok_code.match(str(r.status_code)) else False

    def check_repo_migration(self):
        import_confirm = requests.request('GET', self.import_repo_url, headers=self.repo_header)
        status = import_confirm.json()['status']

        return True if status == 'complete' else False

    def downloads_migration(self):
        while not self.check_repo_migration():
            click.echo('%d초마다 Repo migration 상태를 체크합니다' % WAIT_TIME)
            time.sleep(WAIT_TIME)

        for download_dict in self.downloads.values():
            description = download_dict['json']
            files = download_dict['raw']

            tag_name = description['tag_name']
            target_commitish = description['target_commitish']
            name = description['name']
            body = description['body']
            draft = description['draft']
            prerelease = description['prerelease']

            try:
                release = self.repo.create_release(tag_name, target_commitish, name, body,
                                                   draft, prerelease)

                for file in files:
                    release.upload_asset('multipart/form-data', file['name'], file['raw'])

            except GitHubError as e:
                click.echo(e)
                return False

        return True
