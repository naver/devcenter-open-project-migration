#!/usr/bin/env python3
from github import Github
from naver import Naver
from os.path import exists
from os import makedirs
import click
import os
import subprocess

@click.command()
@click.option('--debug/--no-debug',default=False,help='Set debug mode')
@click.option('--encoding',default='utf-8',help='Encoding of files')
@click.option('--github_repo',prompt=True,help='Name of github repo used for migration')
@click.option('--naver_repo',prompt=True,help='Name of naver project to migrate')
@click.option('--github_id',prompt=True,help='Github username')
@click.password_option('--github_pw',help='Github password')
@click.option('--naver_id',prompt=True,help='NAVER username')
@click.password_option('--naver_pw',help='NAVER password')
@click.option('--vcs',prompt=True,help='Version control system of open project')
def migration(debug,encoding,github_repo,naver_repo,github_id,github_pw,
        naver_id,naver_pw,vcs):
    if debug:
        click.echo("DEBUG MODE ON")

    # github 로그인
    gh = Github(github_id,github_pw,github_repo)

    # github_repo 라는 이름의 저장소를 만들기
    gh.create_repo()

    # naver_repo의 소스 코드 저장소를 github_repo 로 migration
    gh.migration_repo(vcs,naver_id,naver_pw,naver_repo)

    naver = Naver(naver_id,naver_pw,naver_repo)
    # naver_repo 에 있는 이슈 게시판 다운로드를 파싱하
    naver.parsing(gh)

    curdir = os.getcwd()
    os.chdir(curdir + '/wiki_repos/'+gh._repo_name)

    subprocess.run(['git','init'])
    subprocess.run(['git','add','--all'])
    subprocess.run(['git','commit','-m','all asset commit'])
    wiki_git = 'https://github.com/{0}/{1}.wiki.git'.format(gh._username,gh._repo_name)
    subprocess.run(['git','remote','add','origin',wiki_git])
    subprocess.run(['git','push','-f','origin','master'])

    os.chdir(curdir)

if __name__ == '__main__':
    migration()
