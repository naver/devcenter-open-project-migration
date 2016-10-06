# -*- coding: utf-8 -*-
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
import ast
import glob
import json
import mimetypes
import os
import subprocess
import time
from builtins import open

import github3
import grequests
import requests
from future.moves.urllib.parse import urlparse
from github3.exceptions import GitHubError
from migration import WAIT_TIME, CODE_INFO_FILE, ok_code, ISSUES_DIR, DOWNLOADS_DIR, fail_code
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

from .helper import get_fn, chunks

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def exception_handler(request, exception):
    """This function prints grequests exception

    :param request: grequests' object
    :param exception: request's exception
    :return: null
    """
    print(request.text, exception)


class InvalidTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return repr(self.token)


class GitHubMigration:
    header_basis = {
        'authorization': "token ",
        'content-type': "application/json",
    }

    def __init__(self, enterprise, repo_name, project_path, **kwargs):
        provider = 'oss.navercorp' if enterprise else 'github'

        self.__url = 'https://{0}.com'.format(provider)
        url_parsed = urlparse(self.__url)

        self.__api_url = self.__url + '/api/v3/' if enterprise \
            else url_parsed.scheme + '://api.{0}/'.format(url_parsed.netloc)
        self.__token_file_path = os.path.join('data', '{0}_ACCESS_TOKEN').format(provider)
        self.__enterprise = enterprise
        self.__token = kwargs.get('token')
        self.__repo_name = repo_name
        self.__project_path = project_path
        self.__cur_dir = os.path.abspath(os.curdir)

        # if token passed by parameter write to file after confirming token
        # else read file and confirming that token
        # if token is invalid raise InvalidTokenError
        if self.__token:
            self.confirm_token(self.__token)
            # After confirming token and writing file
            mode = 'w'
        else:
            if not os.path.exists(self.__token_file_path):
                self.__token = str(input('Please input token: '))
                self.confirm_token(self.__token)
                mode = 'w'
            else:
                mode = 'r'

        with open(self.token_file_path, mode) as token_file:
            if mode == 'w':
                token_file.write(self.__token)
            else:
                self.__token = self.confirm_token(token_file.read())

        self.__session = github3.GitHub(token=self.__token) if not enterprise \
            else github3.GitHubEnterprise(self.__url, token=self.__token)

        self.__username = self.__session.user().login
        self.__repo = self.__session.repository(owner=self.__username, repository=self.__repo_name)

        if not self.__repo:
            self.__repo = self.__session.create_repo(self.repo_name)

        self.header_basis['authorization'] += self.token

        self.basic_header = self.header_basis.copy()
        self.issue_header = self.header_basis.copy()
        self.repo_header = self.header_basis.copy()

        self.basic_header['Accept'] = 'application/vnd.github.v3+json'
        self.issue_header['Accept'] = 'application/vnd.github.golden-comet-preview'
        self.repo_header['Accept'] = 'application/vnd.github.barred-rock-preview'

        self.basis_repo_url = '{0}repos/{1}/{2}'.format(self.api_url, self.username, self.repo_name)
        self.import_repo_url = self.basis_repo_url + '/import'
        self.import_issue_url = self.import_repo_url + '/issues'

        self.issues = self.read_issue_json()
        self.downloads = self.read_downloads()

    def confirm_token(self, token):
        # get rid special characters of token
        formatted_token = ''.join(_ for _ in token if _.isalnum())
        confirm_url = self.__api_url + 'user?access_token=' + formatted_token

        if not requests.request("GET", confirm_url).status_code is 200:
            raise InvalidTokenError(formatted_token)
        else:
            return formatted_token

    @property
    def token(self):
        return self.__token

    @property
    def token_file_path(self):
        return self.__token_file_path

    @property
    def enterprise(self):
        return self.__enterprise

    @property
    def url(self):
        return self.__url

    @property
    def api_url(self):
        return self.__api_url

    @property
    def session(self):
        return self.__session

    @property
    def repo_name(self):
        return self.__repo_name

    @property
    def username(self):
        return self.__username

    @property
    def repo(self):
        return self.__repo

    @property
    def project_path(self):
        return self.__project_path

    @property
    def cur_dir(self):
        return self.__cur_dir

    def read_issue_json(self):
        files = []

        path = os.path.join(self.project_path, ISSUES_DIR, 'json', '*.json')
        json_list = glob.glob(path)

        for fn in json_list:
            with open(fn) as json_text:
                files.append(json_text.read().replace('{0}', self.url+'/'+self.username+'/'+self.repo_name))

        return files

    def read_downloads(self):
        downloads_path = os.path.join(self.project_path, DOWNLOADS_DIR)
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

    def issues_migration_parallel(self):
        issue_split = list(chunks(self.issues, 30))

        for issues in tqdm(issue_split):
            irs = (grequests.post(self.import_issue_url, data=issue, headers=self.issue_header) for issue in issues)
            import_issues = grequests.map(irs, exception_handler=exception_handler)

            for response in import_issues:
                if not ok_code.match(str(response.status_code)):
                    print(response.text)
                    continue

        self.upload_issue_attach()
        return True

    def issues_migration(self):
        for issue in tqdm(self.issues):
            r = requests.post(self.import_issue_url, data=issue, headers=self.issue_header)

            if not ok_code.match(str(r.status_code)):
                print(r.text)

        self.upload_issue_attach()
        return True

    def upload_issue_attach(self):
        github = urlparse(self.url).netloc
        push_wiki_git = 'https://{0}:{1}@{3}/{0}/{2}.wiki.git'.format(self.username, self.token, self.repo_name, github)

        os.chdir(os.path.join(self.project_path, ISSUES_DIR, 'raw'))

        git_commands = (
            ('git', 'init'),
            ('git', 'add', '--all'),
            ('git', 'commit', '-m', 'all asset commit'),
            ('git', 'remote', 'add', 'origin', push_wiki_git),
            ('git', 'pull', '-f', push_wiki_git, 'master'),
            ('git', 'push', '-f', push_wiki_git, 'master')
        )

        for command in git_commands:
            subprocess.call(command)

        os.chdir(self.cur_dir)

    def repo_migration(self):
        with open(os.path.join(self.project_path, CODE_INFO_FILE)) as code_info:
            r = requests.request("PUT", self.import_repo_url, data=code_info.read().encode('utf-8'),
                                 headers=self.repo_header)

        return True if ok_code.match(str(r.status_code)) else False

    def check_repo_migration(self):
        import_confirm = requests.request('GET', self.import_repo_url, headers=self.repo_header)
        status = import_confirm.json()['status']

        return True if status == 'complete' else False

    def downloads_migration(self):
        check_commits = requests.get(self.basis_repo_url + '/commits').status_code

        if fail_code.match(str(check_commits)):
            print('Your repository does not have commits')

        while not self.check_repo_migration():
            print('Checking repository migration status every %d seconds.' % WAIT_TIME)
            time.sleep(WAIT_TIME)

        for download_dict in self.downloads.values():
            description = ast.literal_eval(download_dict['json'])
            files = download_dict['raw']

            assert(type(description) is dict)

            tag_name = description['tag_name']
            target_commitish = description['target_commitish']
            name = description['name']
            body = description['body']
            draft = description['draft']
            prerelease = description['prerelease']

            try:
                release = self.repo.create_release(tag_name, target_commitish, name, body, draft, prerelease)

                for file in files:
                    release.upload_asset('multipart/form-data', file['name'], file['raw'])

            except GitHubError as e:
                print(e)
                return False

        return True
