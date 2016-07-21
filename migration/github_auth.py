#!env python
# -*- coding: utf-8 -*-
"""
github_auth.py : GitHub 인증을 담당함
"""
import os
import random

import click
import github3
import requests

BASIC_TOKEN_FILE_NAME = 'GITHUB_ACCESS_TOKEN'


class InvalidTokenError(Exception):
    def __init__(self, token):
        os.remove(BASIC_TOKEN_FILE_NAME)
        self.token = token

    def __str__(self):
        return repr(self.token)


def create_session(token):
    return github3.login(token=token)


# 토큰을 검증
# 그 토큰으로 /user 에게 요청을 날려서 200이 뜨나
# T migration 모듈로 넘어감 / F UnvalidTokenError 내며 죽기
def confirm_token(token):
    user_request_url = 'https://api.github.com/user?access_token=' + token

    if requests.request("GET", user_request_url).status_code is 200:
        return token
    else:
        raise InvalidTokenError(token)


# ID/PW 입력
# T 엑세스 토큰 만들고 검증 / F 입력 반복
def input_credentials(github_id=None, github_pw=None):
    auth = None

    if not github_id:
        github_id = click.prompt('GitHub 아이디를 입력해주세요')

    if not github_pw:
        github_pw = click.prompt('GitHub 비밀번호를 입력해주세요',
                                 hide_input=True, confirmation_prompt=True)

    n = random.choice([i for i in range(1, 100)])

    # 랜덤하게 personal access token 을 생성함
    note = 'nopm' + str(n)
    grant = ['repo', 'user', 'delete_repo']

    note_url = 'https://developers.naver.com'

    try:
        auth = github3.authorize(github_id, github_pw, grant, note, note_url)
    except github3.models.GitHubError:
        click.echo('잘못된 아이디와 비밀번호 입니다!!')

    with open(BASIC_TOKEN_FILE_NAME, 'w') as f:
        f.write(auth.token)

    return confirm_token_file()


# GITHUB_ACCESS_TOKEN 파일이 현재 디렉토리에 있는지 검증
# T 토큰을 검증 / F ID/PW 입력
def confirm_token_file(file_name=BASIC_TOKEN_FILE_NAME):
    if os.path.exists(os.path.join(file_name)):
        with open(file_name) as f:
            token = f.read()

        return confirm_token(token)
    else:
        return input_credentials()
