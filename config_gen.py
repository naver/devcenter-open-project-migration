#!/usr/bin/env python3
"""
배포를 쉽게 하기 위해 config.py를 알아서 만들어주는 스크립트
"""
import os
from github3 import authorize
from getpass import getuser, getpass

trueOrFalse = lambda prompt: True if str(input('{0}(y)> '.format(prompt))) is 'y' else False
makeConfigStr = lambda key, value: "{0} = '{1}'\n".format(key,value)
makeConfig = lambda key, value: "{0} = {1}\n".format(key,value)
inputStr = lambda prompt_msg : str(input('{0}> '.format(prompt_msg)))
CONFIG_FILE_NAME = 'config.py'

def make_dir():
    DIRS = {
        'LOGS': './logs',
        'XMLS': './xml_output',
        'FILES': './file_output',
        'WIKI': './wiki_repos',
    }

    for dir_type, dir_name in DIRS.items():
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    return DIRS

def input_password(username):
    password = ''

    while not password:
        password = getpass('{0} 계정의 비밀번호를 입력하세요: '.format(username))

    return password

def github_login():
    """
    유저당 한 번만 하면 되고 다시 엑세스 토큰을 받고 싶으면
    Github 들어가서 이 이름으로 된 개인 토큰을 삭제해야함
    """
    username = inputStr("GitHub 아이디를 입력해주세요")
    password = input_password(username)
    repo_name = inputStr('GitHub 저장소 이름을 알려주세요')

    note = 'NAVER-open-project-migration'
    note_url = 'https://developers.naver.com/main'
    auth = authorize(username, password, ['repo','user','delete_repo'], note, note_url)
    access_token = auth.token

    url = 'https://api.github.com/repos/{0}/{1}/'.format(username,repo_name)

    return username,repo_name,access_token, note, url


def make_config(str_dict,normal_dict):
    assert os.path.exists(CONFIG_FILE_NAME) is False, "config.py is already exist!!"

    with open(CONFIG_FILE_NAME,'w') as f:
        try:
            for k,v in str_dict.items():
                f.write(makeConfigStr(k,v))

            for k,v in normal_dict.items():
                f.write(makeConfig(k,v))
        except KeyboardInterrupt:
            os.remove(CONFIG_FILE_NAME)

def naver_login():
    return "http://staging.dev.naver.com"

if __name__ == "__main__":
    gh_id,repo,access_token,note,github_url = github_login()
    naver_url = naver_login()

    headers = {
        'NAVER' : {
            'cache-control': 'no-cache'
        },
        'GITHUB' : {
            'Accept': "application/vnd.github.golden-comet-preview+json",
            'authorization': "token " + access_token,
            'content-type': "application/json",
            'cache-control': "no-cache",
            'User-Agent': note
        }
    }

    input_str = dict(
        XML_EXTENSION = '.xml',
        ENCODING = inputStr('기본 인코딩을 입력해주세요'),
        GITHUB_URL = github_url,
        NAVER_URL = naver_url,
        ACCESS_TOKEN = access_token,
        GH_USERNAME = gh_id,
        GH_REPO_NAME = repo
    )

    input_normal = dict(
        DEBUG = trueOrFalse('디버그 모드 활성화'),
        TEST = trueOrFalse('유닛테스트 모드'),
        DIR_LIST = make_dir(),
        HEADERS = headers,
        XML_OUTPUT = trueOrFalse('XML 파일 출력')
        )

    make_config(input_str,input_normal)
