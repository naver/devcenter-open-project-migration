#!/usr/bin/env python3
from config import NAVER_URL, GH_USERNAME, \
GH_REPO_NAME, ACCESS_TOKEN, DEBUG,HEADERS
from github3 import login
import requests
import logging
from requests import request
from config_gen import inputStr,input_password
import json

repo_url_create = lambda user_name,repo_name: 'https://api.github.com/repos/{0}/{1}/import'.format(user_name,repo_name)

def create_github_repo(gh_session,n_pr_name):
    repo = gh.repository(GH_USERNAME,n_pr_name)

    if not repo:
        repo = gh.create_repo(n_pr_name)
        print("{0} 가 성공적으로 만들어짐".format(repo.name))
    else:
        print("{0} 가 이미 만들어짐".format(repo.name))

    return repo

def create_import_json(vcs_name,n_name,n_pw,n_pr_name):
    full_vcs_name = ''
    url = ''
    username = ''
    password = ''

    if vcs_name == 'git':
        full_vcs_name = vcs_name
        url = 'https://{0}@dev.naver.com/{1}/{2}.{1}'.format(n_name,vcs_name,n_pr_name)
        username,password = n_name,n_pw
    else:
        full_vcs_name = 'subversion'
        url = 'https://dev.naver.com/{0}/{1}'.format(vcs_name,n_pr_name)
        username,password = 'anonsvn','anonsvn'

    return json.dumps(
        dict(
            vcs=full_vcs_name,
            vcs_url=url,
            vcs_username=username,
            vcs_password=password
            )
        )

def delete_repo(gh_session,n_pr_name):
    repo = gh_session.repository(GH_USERNAME,n_pr_name)

    if repo:
        repo.delete()
        print("{0} 가 성공적으로 지워짐".format(repo.name))
    else:
        print("{0} 가 이미 지워짐".format(repo.name))

if __name__ == "__main__":
    # 프로젝트 이름으로 된 GitHub 저장소를 만든다.
    gh = login(token=ACCESS_TOKEN)
    naver_project_name = inputStr("프로젝트 이름을 입력해주세요")
    repo = create_github_repo(gh,naver_project_name)

    # 사용자의 네이버 아이디와 비밀번호를 받는다
    naver_username = inputStr('네이버 아이디를 입력해주세요')
    naver_password = input_password(naver_username)

    # 다른 프로젝트를 마이그레이션 하고 싶으면
    # config.py 의 NAVER_PROJECT_NAME 값을 변경할 것
    # 사용자에게 자신의 프로젝트가 git 을 쓰는지 SVN을 쓰는지 질의
    vcs_name = ''


    while not vcs_name in ['git', 'svn']:
        vcs_name = inputStr("어떤 버전 컨트롤 시스템을 쓰시나요")

    REQUEST_URL = repo_url_create(GH_USERNAME,
                                  naver_project_name)
    REQUEST_DATA = create_import_json(vcs_name,
                                      naver_username,
                                      naver_password,
                                      naver_project_name)

    HEADERS['GITHUB']['Accept'] = 'application/vnd.github.barred-rock-preview'

    repo_import_request = request("PUT",REQUEST_URL,
                                  data=REQUEST_DATA,
                                  headers=HEADERS['GITHUB'])

    # 201
    if repo_import_request.status_code is not 201:
        print("마이그레이션에 실패했습니다. 로그를 봐주세요.")
    else:
        print("마이그레이션이 끝나면 프로젝트로 가서 위키 페이지를 만들어주세요!")
