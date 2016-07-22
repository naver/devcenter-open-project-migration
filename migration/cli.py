#!env python
# -*- coding: utf-8 -*-
import logging
import os
import time
import webbrowser

import click
import migration.github_auth

from .helper import set_encoding
from .issue_migration import issue_migration
from .project import Project
from .repo_migration import repo_migration, pool

set_encoding()

cur_dir = os.getcwd()
logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'),
                    level=logging.DEBUG)


@click.command()
@click.option('--github_repo', prompt=True, help='GitHub 레포지토리 이름')
@click.option('--naver_repo', prompt=True, help='네이버 프로젝트 이름')
def cli(github_repo, naver_repo):
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

    issue_result = pool.apply_async(issue_migration,
                                    kwds=dict(
                                        project=project
                                    ))
    repo_result = pool.apply_async(repo_migration,
                                   kwds=dict(project=project, github_session=gh, github_repository=repo)
                                   )

    issue_migration_success = issue_result.get()
    repo_migration_success = repo_result.get()

    if not issue_migration_success:
        click.echo('Issue migration failed...')

    if not repo_migration_success:
        click.echo('Repo migration failed...')


if __name__ == '__main__':
    cli()
