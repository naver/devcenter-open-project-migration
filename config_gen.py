#!/usr/bin/env python3
"""
배포를 쉽게 하기 위해 config.py를 알아서 만들어주는 스크립트
"""
import json
import os
from github3 import authorize
from getpass import getuser, getpass

if not os.path.exists('./logs'):
    os.mkdir('logs')
if not os.path.exists('./xml_output'):
    os.mkdir('xml_output')

assert os.path.exists('config.py') is False, "config.py is already exist!!"

username = str(input("GitHub 아이디를 입력해주세요> "))
password = ''
while not password:
    password = getpass('Password for {0}: '.format(username))

note = 'NAVER-open-project-migration'
note_url = 'https://developers.naver.com/main'
scopes = ['repo']
auth = authorize(username, password, scopes, note, note_url)
access_token = auth.token

with open('config.py','w') as f:
    try:
        f.write("XML_EXTENSION = '.xml'\n")
        f.write("HEADERS = " + json.dumps({
            'NAVER' : {
                'cache-control': 'no-cache'
            },
            'GITHUB' : {
                'Accept': "application/vnd.github.golden-comet-preview+json",
                'authorization': "token " + access_token,
                'content-type': "application/json",
                'cache-control': "no-cache",
                'User-Agent': 'postman-test'
            }
        }) + '\n')

        encoding = str(input('기본 인코딩을 입력해주세요> '))
        f.write("ENCODING = '" + encoding + "'\n")
        debug = str(input('디버그 모드(y/n)> '))
        f.write("DEBUG = True\n" if debug is 'y' else "DEBUG = False\n")

        test = str(input('유닛테스트 모드(y/n)> '))
        f.write("TEST = True\n" if test is 'y' else "TEST = False\n")

        xml_output = str(input('XML 파일 출력(y/n)> '))
        f.write("XML_OUTPUT = True\n" if xml_output is 'y' else "XML_OUTPUT = False\n")

        repo_name = str(input('GitHub 저장소 이름을 알려주세요> '))

        github_url = 'https://api.github.com/repos/{0}/{1}/'.format(username,repo_name)

        f.write("GITHUB_URL = '" + github_url + "'\n")
        """
        TODO:
        차후에 저장소를 만들고 오픈 프로젝트의 있는 걸 migration 하는 것까지 추가해야함
        """
    except KeyboardInterrupt:
        os.remove('config.py')
