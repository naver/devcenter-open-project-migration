# -*- coding: utf-8 -*-
import json
import mimetypes
import os
import time

import click
import github3
import grequests
import requests
from github3.exceptions import GitHubError
from migration import WAIT_TIME, ASSET_DIR, CODE_INFO_FILE, ok_code, ISSUES_DIR, DOWNLOADS_DIR
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def exception_handler(request, exception):
    print(exception)


class GitHubSession:
    urls = ['https://github.com', 'https://oss.navercorp.com']

    def __init__(self, token, enterprise, repo_name):
        self.url = self.urls[enterprise]
        self.token = token
        self.enterprise = enterprise

        self.session = github3.login(token=token) \
            if not enterprise else github3.GitHubEnterprise(self.url, token=token)

        self.api_url = self.session.__dict__['_session'].__dict__['base_url']

        self.username = self.session.user().login
        self.repo = self.session.repository(owner=self.username, repository=repo_name)

        if not self.repo:
            self.session.create_repo(repo_name)

        self.repo_name = repo_name

    def make_github_info(self, path):
        with open(os.path.join(path, 'github_info.json'), 'w') as github_info:
            github_info.write(json.dumps(dict(
                enterprise=self.enterprise,
                token=self.token,
                repo_name=self.repo_name
            )))


class GithubMigration:
    header_basis = {
        'authorization': "token ",
        'content-type': "application/json",
    }

    def __init__(self, github_session, repo, token, data_path):
        # 헤더 정의
        self.header_basis['authorization'] += token

        self.basic_header = self.header_basis.copy()
        self.issue_header = self.header_basis.copy()
        self.repo_header = self.header_basis.copy()

        self.basic_header['Accept'] = 'application/vnd.github.v3+json'
        self.issue_header['Accept'] = 'application/vnd.github.golden-comet-preview'
        self.repo_header['Accept'] = 'application/vnd.github.barred-rock-preview'

        self.github_api_url = github_session.__dict__['_session'].__dict__['base_url']
        self.github_username = github_session.user().login
        self.repo = repo
        self.repo_name = self.repo.name
        self.basis_repo_url = '{0}/repos/{1}/{2}'.format(self.github_api_url, self.github_username, self.repo_name)
        self.import_repo_url = self.basis_repo_url + '/import'
        self.import_issue_url = self.import_repo_url + '/issues'

        self.data_path = data_path

        self.issues = self.read_issue_json()
        self.downloads = self.read_downloads()

    def read_issue_json(self):
        files = []

        raw_files_dir = 'wiki_repo'
        path = os.path.join(self.data_path, ISSUES_DIR)

        json_list = os.listdir(path)
        json_list.remove(raw_files_dir)

        for fn in json_list:
            ext = os.path.splitext(fn)[1]

            if ext != '.json':
                continue

            with open(os.path.join(path, fn)) as json_text:
                read_file = json_text.read()
                files.append(read_file.encode('utf-8'))

        return files

    def read_downloads(self):
        path = os.path.join(self.data_path, DOWNLOADS_DIR)
        result = dict()

        for fn in os.listdir(path):
            ext = os.path.splitext(fn)[1]
            content_path = os.path.join(path, fn)

            if fn != 'files':
                if ext != '.json':
                    continue

                download_id = os.path.splitext(fn)[0]

                result[download_id] = dict()
                result[download_id][ASSET_DIR] = list()

                with open(content_path) as json_text:
                    result[download_id]['description'] = json.loads(json_text.read())
            else:
                for download_id in os.listdir(content_path):
                    raw_dir_path = os.path.join(content_path, download_id)

                    for raw_fn in os.listdir(raw_dir_path):
                        file_path = os.path.join(raw_dir_path, raw_fn)
                        file_name = os.path.basename(file_path)
                        ext = os.path.splitext(file_name)[1]
                        content_type = mimetypes.types_map[ext]

                        with open(file_path, 'rb') as raw_file:
                            result[download_id]['files'].append(dict(
                                name=file_name,
                                raw=raw_file.read(),
                                content_type=content_type
                            ))

        return result

    def issues_migration(self):
        irs = (grequests.post(self.import_issue_url, data=issue, headers=self.issue_header) for issue in self.issues)
        import_issues = grequests.map(irs, exception_handler=exception_handler)

        for response in import_issues:
            if not ok_code.match(str(response.status_code)):
                return False

        return True

    def repo_migration(self):
        with open(os.path.join(self.data_path, CODE_INFO_FILE)) as code_info:
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
            description = download_dict['description']
            files = download_dict['files']

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
