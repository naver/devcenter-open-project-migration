#!env python
# -*- coding: utf-8 -*-
import logging
import os
import threading
import time
import webbrowser

import click
import migration.github_auth
from .issue_migration import issue_migration
from .helper import set_encoding
from .project import Project
from .repo_migration import repo_migration

set_encoding()
print_lock = threading.Lock()

cur_dir = os.getcwd()
logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'),
                    level=logging.DEBUG)


@click.command()
@click.option('--github_repo', prompt=True, help='Name of github repo used for migration')
@click.option('--naver_repo', prompt=True, help='Name of naver project to migrate')
@click.option('--naver_id', prompt=True, help='NAVER username')
@click.password_option('--naver_pw', help='NAVER password')
def cli(github_repo, naver_repo, naver_id, naver_pw):
    os.chdir(cur_dir)
    token = migration.github_auth.confirm_token_file()
    gh = migration.github_auth.create_session(token)
    github_id = gh.user().login
    repo = gh.repository(owner=github_id, repository=github_repo)

    if not repo:
        repo = gh.create_repo(github_repo)

    # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
    wiki_create_page_url = 'https://github.com/{0}/{1}/wiki/_new'.format(github_id, github_repo)

    if webbrowser.open(wiki_create_page_url):
        click.echo('Save Page 버튼을 눌러주세요!')

    # 올바른 프로젝트인지 검증
    click.echo('프로젝트 파싱 중')
    project = Project(naver_repo, 'http://staging.dev.naver.com')

    issue_thread = threading.Thread(target=issue_migration,
                                    kwargs=dict(
                                        project=project
                                    ))
    repo_thread = threading.Thread(target=repo_migration,
                                   kwargs=dict(project=project,
                                               github_session=gh,
                                               github_repository=repo,
                                               username=naver_id,
                                               password=naver_pw)
                                   )

    issue_thread.start()
    repo_thread.start()

if __name__ == '__main__':
    cli()
