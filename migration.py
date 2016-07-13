# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from github import Github
from naver import Naver
from os.path import exists
from os import makedirs
import click
import os
import subprocess

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

    # naver_repo의 소스 코드 저장소를 github_repo 로 migration
    gh.migration_repo(vcs   ,naver_id,naver_pw,naver_repo)

    naver = Naver(naver_id,naver_pw,naver_repo,gh)
    # naver_repo 에 있는 이슈 게시판 다운로드를 파싱하
    naver.parsing()

    curdir = os.getcwd()

    os.chdir(curdir + '/wiki_repos/'+github_repo)

    wiki_git = 'https://github.com/{0}/{1}.wiki.git'.format(github_id,github_repo)
    push_wiki_git = 'https://{0}:{1}@github.com/{0}/{2}.wiki.git'.format(github_id,github_pw,github_repo)
    subprocess.run(['git','init'])
    subprocess.run(['git','remote','add','origin',wiki_git])
    subprocess.run(['git','pull',push_wiki_git, 'master'])
    subprocess.run(['git','add','--all'])
    subprocess.run(['git','commit','-m','all asset commit'])

    subprocess.run(['git','push',push_wiki_git,'master'])

    os.chdir(curdir)

if __name__ == '__main__':
    migration()
