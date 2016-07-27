# -*- coding: utf-8 -*-
"""
github_auth.py : GitHub 인증을 담당함
"""
import os

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

    confirm_token_status_code = requests.request("GET", user_request_url).status_code

    if confirm_token_status_code is 200:
        return write_token_to_file(token, file_name)
    elif confirm_token_status_code is 404:
        raise InvalidEnterPriseUrlError(enterprise_url)
    else:
        raise InvalidTokenError(token)


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