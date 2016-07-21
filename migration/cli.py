#!env python
# -*- coding: utf-8 -*-
import logging
import os
import time
import webbrowser
import threading


import click
import migration.github_auth
from .helper import set_encoding
from .naver import Naver
from .project import Project

set_encoding()

logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'),
                    level=logging.DEBUG)


def issue_migration():
    print('issue_migration')


def repo_migration():
    print('repo_migration')



@click.command()
@click.option('--github_repo', prompt=True, help='Name of github repo used for migration')
@click.option('--naver_repo', prompt=True, help='Name of naver project to migrate')
@click.option('--naver_id', prompt=True, help='NAVER username')
@click.password_option('--naver_pw', help='NAVER password')
@click.option('--vcs', prompt=True, help='Version control system of open project')
def cli(github_repo, naver_repo, naver_id, naver_pw, vcs):
    """
    :param github_repo: Name of github repo used for migration
    :param naver_repo: Name of naver project to migrate
    :param naver_id: NAVER username
    :param naver_pw: NAVER password
    :param vcs: Version control system of open project
    :return: None
    """

    token = migration.github_auth.confirm_token_file()
    gh = migration.github_auth.create_session(token)

    github_id = gh.user().login
    #gh.create_repo(github_repo)

    # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
    wiki_create_page_url = 'https://github.com/{0}/{1}/wiki/_new'.format(github_id, github_repo)

    #if webbrowser.open(wiki_create_page_url):
    #    click.echo('Save Page 버튼을 눌러주세요!')

    # 올바른 프로젝트인지 검증
    #project = Project(naver_repo, 'http://staging.dev.naver.com')
    #print(project)

    issue_thread = threading.Thread(target=issue_migration)
    repo_thread = threading.Thread(target=repo_migration)

    issue_thread.daemon = True
    issue_thread.start()

    repo_thread.daemon = True
    repo_thread.start()


if __name__ == '__main__':
    cli()
