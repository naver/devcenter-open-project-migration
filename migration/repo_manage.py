# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys
import time
import webbrowser

import click
from migration import get_file_path, DATA_DIR, PARSING_OUTPUT_DIR

from .github_migration import GithubMigration, GitHubSession
from .helper import set_encoding, print_green
from .token_manage import read_token_from_file

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
@click.option('--delete', is_flag=True, default=False, help='GitHub 저장소 삭제')
@click.option('--repo_name', prompt=True, help='GitHub 저장소 이름 입력')
@click.option('--enterprise', help='GitHub 엔터프라이즈 여부', is_flag=True, default=False)
def repo_manage(repo_name, delete, enterprise):
    """ GitHub Repository management """
    # 현재 디렉토리를 프로젝트 루트로
    os.chdir(cur_dir)

    # 데이터(쿠키, 토큰) 등이 담기는 디렉토리 생성
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    token_file_path = get_file_path('token', enterprise)
    token = read_token_from_file(token_file_path, enterprise)

    gh = GitHubSession(token, enterprise, repo_name)

    repo = gh.repo

    if not delete:
        is_wiki = click.prompt('위키를 만드셨나요(y/n)', type=bool)

        if not is_wiki:
            wiki_create_page_url = '{2}/{0}/{1}/wiki/_new'.format(gh.user().login, repo_name, github_url)

            # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
            if webbrowser.open(wiki_create_page_url):
                click.echo('첫 위키 페이지를 만들기 위해 ' + click.style('Save Page', fg='green') + ' 버튼을 눌러주세요!')
            else:
                click.echo(click.style('웹 브라우저를 여는데 실패 했습니다!!', fg='red'))
                click.echo(click.style(wiki_create_page_url + 'Save Page 버튼을 눌러주세요!', fg='green'))

        output_dirs = os.listdir(PARSING_OUTPUT_DIR)
        print_green('아래 목록에서 Migration 할 프로젝트의 번호를 입력하세요')

        menu = '번호를 입력하세요 '

        for idx in range(len(output_dirs)):
            menu += '{0}: {1} '.format(str(idx), output_dirs[idx])

        idx = click.prompt(menu, type=int)
        project_name = output_dirs[idx]
        is_dev_code = 'dev_code' in project_name
        project_dir = os.path.join(PARSING_OUTPUT_DIR, project_name)

        gm = GithubMigration(gh, repo, token, project_dir)

        # dev_code 가 프로젝트 이름에 있거나 enterprise면 이슈 및 게시판 마이그레이션 만 수행
        if not gm.issues_migration():
            click.echo('이슈 및 게시판 마이그레이션 실패')

        if not is_dev_code and not enterprise:
            if not gm.repo_migration():
                click.echo('소스코드 저장소 마이그레이션 실패')

            if not gm.downloads_migration():
                click.echo('다운로드 마이그레이션 실패')
    else:
        gh.repo.delete()

if __name__ == '__main__':
    repo_manage()
