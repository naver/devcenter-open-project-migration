# -*- coding: utf-8 -*-
import os

import click
import requests
from migration import API_URLS, DATA_DIR, get_file_path


def confirm_token(token, enterprise):
    url = API_URLS[enterprise] + 'user?access_token=' + token
    return True if requests.request("GET", url).status_code is 200 else False


def token_to_file(token, file_path, enterprise):
    # 토큰이 유효하지 않으면 맞을 때까지 입력

    while not confirm_token(token, enterprise):
        click.echo(click.style(token + ' 토큰이 잘못되었습니다!!', fg='red'))
        token = click.prompt('새 토큰을 입력하세요')

    # 토큰을 파일로 입력
    with open(file_path, 'w') as token_file:
        token_file.write(token)

    return token


def read_token_from_file(file_path, enterprise):
    token = str()

    try:
        with open(file_path) as token_file:
            token = token_file.read()

        return token if confirm_token(token, enterprise) else token_to_file(token, file_path, enterprise)
    except FileNotFoundError:
        return token_to_file(token, file_path, enterprise)


@click.command()
@click.option('--token', help='토큰 입력')
@click.option('--enterprise', help='GitHub Enterprise mode', is_flag=True, default=False)
def token_manage(token, enterprise):
    """ Managing your GitHub and GitHub ENTERPRISE TOKEN. """
    token_file_path = get_file_path('token', enterprise)

    msg = 'GitHub Enterprise' if enterprise else 'GitHub'

    valid_token = token_to_file(token, token_file_path, enterprise) if token \
        else read_token_from_file(token_file_path, enterprise)
    click.echo(valid_token + click.style(' 은 유효한 ' + msg + ' 토큰입니다', fg='blue'))

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    token_manage()
