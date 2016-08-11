# -*- coding: utf-8 -*-
import json
import os
import webbrowser

import click
from cli import CUR_DIR, PARSING_OUTPUT_DIR
from migration.github import GitHubSession, GithubMigration


@click.command()
@click.option('--open_project', help='DevCode 프로젝트인지', is_flag=True, prompt=True)
def github_migration(open_project):
    """ GitHub Repository management """

    # 현재 디렉토리를 프로젝트 루트로
    os.chdir(CUR_DIR)

    is_open_project = open_project
    nforge_type = 'open_project' if is_open_project else 'dev_code'
    output_dirs = ''
    nforge_path = os.path.join(os.path.join(PARSING_OUTPUT_DIR, nforge_type))

    try:
        output_dirs = os.listdir(nforge_path)
    except FileNotFoundError:
        click.echo('%s 아직 프로젝트를 파싱하지 않았습니다...' % nforge_type)
        exit()

    click.echo(click.style('아래 목록에서 Migration 할 프로젝트의 번호를 입력하세요', fg='green'))
    menu = '번호를 입력하세요 '

    for idx in range(len(output_dirs)):
        menu += '{0}: {1} '.format(str(idx), output_dirs[idx])

    idx = click.prompt(menu, type=int)
    project_name = output_dirs[idx]
    project_path = os.path.join(nforge_path, project_name)

    with open(os.path.join(project_path, 'github_info.json')) as github_info:
        project_info = json.load(github_info)

    token = project_info['token']
    repo_name = project_info['repo_name']
    enterprise = project_info['enterprise']

    gh = GitHubSession(token, enterprise, repo_name, project_path)

    is_wiki = click.prompt('위키를 만드셨나요(y/n)', type=bool)

    if not is_wiki:
        wiki_create_page_url = '{2}/{0}/{1}/wiki/_new'.format(gh.username, gh.repo_name, gh.url)

        # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
        if webbrowser.open(wiki_create_page_url):
            click.echo('첫 위키 페이지를 만들기 위해 ' + click.style('Save Page', fg='green') + ' 버튼을 눌러주세요!')
        else:
            click.echo(click.style('웹 브라우저를 여는데 실패 했습니다!!', fg='red'))
            click.echo(click.style(wiki_create_page_url + 'Save Page 버튼을 눌러주세요!', fg='green'))

    gm = GithubMigration(session=gh)

    # dev_code 가 프로젝트 이름에 있거나 enterprise 면 이슈 및 게시판 마이그레이션 만 수행
    if not gm.issues_migration():
        click.echo('이슈 및 게시판 마이그레이션 실패')

    if is_open_project and not enterprise:
        if not gm.repo_migration():
            click.echo('소스코드 저장소 마이그레이션 실패')

        if not gm.downloads_migration():
            click.echo('다운로드 마이그레이션 실패')

if __name__ == '__main__':
    github_migration()
