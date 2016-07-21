# -*- coding: utf-8 -*-
# !env python
import json
import logging
import os
import threading
import time

from requests import request
from .github_auth import BASIC_TOKEN_FILE_NAME


class RepoMigrationError(Exception):
    def __init__(self, json_text):
        os.remove(BASIC_TOKEN_FILE_NAME)
        self.json = json_text

    def __str__(self):
        return repr(self.json)


def repo_migration(**kwargs):
    project = kwargs.get('project')
    thread_msg = '{0}가 {1}의 소스 코드 마이그레이션 시작'.format(threading.current_thread().name,
                                                    project.project_name)
    logging.debug(thread_msg)
    print(thread_msg)

    gh = kwargs.get('github_session')
    repo = kwargs.get('github_repository')

    with open(BASIC_TOKEN_FILE_NAME) as f:
        token = f.read()

    if project.vcs is 'git':
        username = kwargs.get('username')
        password = kwargs.get('password')
        vcs = 'git'
        url = 'https://{0}@dev.naver.com/{1}/{2}.{1}'.format(username, project.vcs, project.project_name)
    else:
        username = 'anonsvn'
        password = 'anonsvn'
        vcs = 'subversion'
        url = 'https://dev.naver.com/{0}/{1}'.format(project.vcs, project.project_name)

    migration_request_url = '{0}/repos/{1}/{2}/import'.format(gh._github_url,
                                                              gh.user().login,
                                                              repo.name)

    import_headers = {
            'Accept': "application/vnd.github.barred-rock-preview",
            'authorization': "token " + token,
            'content-type': "application/json",
        }

    request_data = json.dumps(
        dict(
            vcs=vcs,
            vcs_url=url,
            vcs_username=username,
            vcs_password=password
        )
    )

    r = request("PUT", migration_request_url, data=request_data, headers=import_headers)

    if r.status_code is 201:
        repo_migration_status = True if r.json()['status'] is 'complete' else False
    else:
        raise RepoMigrationError(r.json())

    while not repo_migration_status:
        import_confirm = request('GET', migration_request_url, headers=import_headers)

        repo_migration_status = True if import_confirm.json()['status'] == 'complete' \
            else False

        print("15초 후 다시 완료 여부를 확인 합니다...")
        time.sleep(15)
