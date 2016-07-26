# -*- coding: utf-8 -*-
"""
github_auth.py : GitHub 인증을 담당함
"""
import os
import random

import click
import github3
import requests


class InvalidTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return repr(self.token)


class InvalidEnterPriseUrlError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return repr(self.url)


def create_session(token, enterprise_url):
    if not enterprise_url:
        return github3.login(token=token)
    else:
        return github3.GitHubEnterprise(enterprise_url, token=token)


# 토큰을 검증
# 그 토큰으로 /user 에게 요청을 날려서 200이 뜨나
# T migration 모듈로 넘어감 / F UnvalidTokenError 내며 죽기
def confirm_token(token, enterprise_url, file_name):
    if not enterprise_url:
        user_request_url = 'https://api.github.com/user?access_token=' + token
    else:
        user_request_url = '{0}/api/v3/user?access_token={1}'.format(enterprise_url, token)

    if requests.request("GET", user_request_url).status_code is 200:
        return write_token_to_file(token, file_name)
    elif requests.request("GET", user_request_url).status_code is 404:
        if not enterprise_url:
            input_credentials(enterprise_url, file_name)
        raise InvalidEnterPriseUrlError(enterprise_url)
    else:
        if not enterprise_url:
            input_credentials(enterprise_url, file_name)
        raise InvalidTokenError(token)


# ID/PW 입력
# T 엑세스 토큰 만들고 검증 / F 입력 반복
def input_credentials(enterprise_url, file_name, github_id=None, github_pw=None):
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

    confirm_token(auth.token, enterprise_url, file_name)


def write_token_to_file(token, file_name):
    with open(file_name, 'w') as f:
        f.write(token)

    return token


# GITHUB_ACCESS_TOKEN 파일이 현재 디렉토리에 있는지 검증
# T 토큰을 검증 / F ID/PW 입력
def confirm_token_file(file_name, enterprise_url):
    if os.path.exists(os.path.join(file_name)):
        with open(file_name) as f:
            token = f.read()
    else:
        token = click.prompt('Token 을 입력하세요', type=str)

    return confirm_token(token, enterprise_url, file_name)
