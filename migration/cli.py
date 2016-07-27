# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys
import time
import webbrowser

import click
import migration.github_auth

from .helper import set_encoding, print_green
from .issue_migration import issue_migration
from .project import Project
from .repo_migration import repo_migration, pool

if sys.version_info.major is 2:
    set_encoding()
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

cur_dir = os.getcwd()
logging.basicConfig(filename=os.path.join('logs', time.strftime("%Y-%m-%d %H:%M:%S") + '.log'), level=logging.ERROR)


def upload_asset_by_git(user_name, repo_name, token, github_url):
    click.echo('첨부파일 업로드를 시작합니다')
    url = urlparse(github_url).netloc
    push_wiki_git = 'https://{0}:{1}@{3}/{0}/{2}.wiki.git'.format(user_name, token, repo_name, url)

    os.chdir(os.path.join(cur_dir, 'wiki_repos', repo_name))

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

    os.chdir(cur_dir)


@click.command()
@click.option('--github_repo', prompt=True, help='GitHub 레포지토리 이름')
@click.option('--project_name', prompt=True, help='NFORGE 프로젝트 이름')
@click.option('--api_url', prompt=True, help='NFORGE API URL')
@click.option('--cookies', help='쿠키 이용 여부', is_flag=True, default=False)
@click.option('--enterprise_url', help='GitHub 엔터프라이즈 URL', default=None)
@click.option('--issue_only', help='이슈만 마이그레이션 여부', is_flag=True, default=False)
def cli(github_repo, project_name, api_url, enterprise_url, cookies, issue_only):
    os.chdir(cur_dir)

    token_file_name = 'ENTERPRISE_ACCESS_TOKEN' if enterprise_url else 'GITHUB_ACCESS_TOKEN'

    token = migration.github_auth.confirm_token_file(token_file_name, enterprise_url)
    gh = migration.github_auth.create_session(token, enterprise_url)

    github_url = 'https://github.com' if not enterprise_url else enterprise_url
    wiki_create_page_url = '{2}/{0}/{1}/wiki/_new'.format(gh.user().login, github_repo, github_url)

    github_id = gh.user().login
    repo = gh.repository(owner=github_id, repository=github_repo)

    if not repo:
        repo = gh.create_repo(github_repo)
        print_green('{0} 저장소가 생성되었습니다...'.format(repo.name))
    else:
        print_green('{0} 저장소가 존재합니다...'.format(repo.name))

    # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
    if webbrowser.open(wiki_create_page_url):
        click.echo('첫 위키 페이지를 만들기 위해 ' + click.style('Save Page', fg='green') + ' 버튼을 눌러주세요!')

    # 올바른 프로젝트인지 검증
    click.echo('프로젝트 파싱 중')
    project = Project(project_name, api_url, cookies)

    param = dict(project=project, github_session=gh, github_repository=repo, token_file_name=token_file_name)

    issue_result = pool.apply_async(issue_migration, kwds=param)

    if not issue_only:
        repo_result = pool.apply_async(repo_migration, kwds=param)
        repo_migration_success = repo_result.get()

        if not repo_migration_success:
            click.echo('Repo migration failed...')

    issue_migration_success = issue_result.get()

    if not issue_migration_success:
        click.echo('Issue migration failed...')

    upload_asset_by_git(github_id, repo.name, token, github_url)

if __name__ == '__main__':
    cli()
