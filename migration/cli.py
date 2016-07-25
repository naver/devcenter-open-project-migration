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
logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'), level=logging.ERROR)


@click.command()
@click.option('--github_repo', prompt=True, help='GitHub 레포지토리 이름')
@click.option('--project_name', prompt=True, help='NFORGE 프로젝트 이름')
@click.option('--api_url', prompt=True, help='NFORGE API URL')
@click.option('--cookies', help='쿠키 이용 여부', is_flag=True)
@click.option('--enterprise', help='GitHub 엔터프라이즈 여부', is_flag=True)
def cli(github_repo, project_name, api_url, enterprise, cookies):
    os.chdir(cur_dir)

    enterprise_url = '' if not enterprise else click.prompt('GitHub Enterprise URL을 입력하세요', type=str)

    token = migration.github_auth.confirm_token_file(enterprise)
    gh = migration.github_auth.create_session(token, enterprise_url)
    github_url = 'https://github.com' if not enterprise_url else enterprise_url
    wiki_create_page_url = '{2}/{0}/{1}/wiki/_new'.format(gh.user().login, github_repo, github_url)

    github_id = gh.user().login
    repo = gh.repository(owner=github_id, repository=github_repo)

    if not repo:
        repo = gh.create_repo(github_repo)

    click.echo('GitHub 저장소 생성 완료...')

    # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
    if webbrowser.open(wiki_create_page_url):
        click.echo('첫 위키 페이지를 만들기 위해 ' + click.style('Save Page', fg='green') + ' 버튼을 눌러주세요!')

    # 올바른 프로젝트인지 검증
    click.echo('프로젝트 파싱 중')
    project = Project(project_name, api_url, cookies)

    param = dict(project=project, github_session=gh, github_repository=repo)

    issue_result = pool.apply_async(issue_migration, kwds=param)
    repo_result = pool.apply_async(repo_migration, kwds=param)
    issue_migration_success = issue_result.get()
    repo_migration_success = repo_result.get()

    if not issue_migration_success:
        click.echo('Issue migration failed...')

    if not repo_migration_success:
        click.echo('Repo migration failed...')


if __name__ == '__main__':
    cli()
