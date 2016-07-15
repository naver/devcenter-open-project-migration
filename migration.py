# -*- coding: utf-8 -*-
#!/usr/bin/env python
from github import Github
from naver import Naver
from os.path import exists
from os import makedirs
import click
import os
import subprocess
import platform
import sys

if platform.python_version()[0] is '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')

@click.command()
@click.option('--encoding',default='utf-8',help='Encoding of files')
@click.option('--github_repo',prompt=True,help='Name of github repo used for migration')
@click.option('--naver_repo',prompt=True,help='Name of naver project to migrate')
@click.option('--github_id',prompt=True,help='Github username')
@click.password_option('--github_pw',help='Github password')
@click.option('--naver_id',prompt=True,help='NAVER username')
@click.password_option('--naver_pw',help='NAVER password')
@click.option('--vcs',prompt=True,help='Version control system of open project')
def migration(encoding,github_repo,naver_repo,github_id,github_pw,
        naver_id,naver_pw,vcs):
    # github login
    gh = Github(github_id,github_pw,github_repo)

    # Making github repository
    gh.create_repo()
    
    try:
        # naver_repo의 소스 코드 저장소를 github_repo 로 migration
        migration_status = gh.migration_repo(vcs,naver_id,naver_pw,naver_repo)

        # 저장소 마이그레이션이 끝나지 않았다면 릴리즈를 마이그레이션 하면 안됨
        if not migration_status:
            print('소스 코드 마이그레이션이 완료되지 않았습니다! 다운로드는 나중에 마이그레이션 합니다')

        naver = Naver(naver_id,naver_pw,naver_repo,gh)
        # naver_repo 에 있는 이슈 게시판 다운로드를 파싱하기
        naver.parsing()
        upload_asset_by_git(github_id,github_pw,github_repo)
    except KeyboardInterrupt:
        print('KeyboardInterrupt will delete repo')
        gh.delete_repo()

def upload_asset_by_git(username,password,repo_name):
    push_wiki_git = 'https://{0}:{1}@github.com/{0}/{2}.wiki.git'.format(username,password,repo_name)
    git_commands = [
        ['git','init'],
        ['git','remote','add','origin',push_wiki_git],
        ['git','pull',push_wiki_git, 'master'],
        ['git','add','--all'],
        ['git','commit','-m','all asset commit'],
        ['git','push',push_wiki_git,'master']
    ]

    curdir = os.getcwd()
    os.chdir(curdir + '/wiki_repos/'+repo_name)

    for command in git_commands:
        subprocess.call(command)

    os.chdir(curdir)


if __name__ == '__main__':
    migration()
