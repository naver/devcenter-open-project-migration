# -*- coding: utf-8 -*-
import click
import requests
from cli import API_URLS, TOKEN_FILE_NAMES


def confirm_token(token, enterprise):
    url = API_URLS[enterprise] + 'user?access_token=' + token
    return True if requests.request("GET", url).status_code is 200 else False


def token_to_file(token, enterprise):
    # 토큰이 유효하지 않으면 맞을 때까지 입력
    while not confirm_token(token, enterprise):
        click.echo(click.style(token + ' 토큰이 잘못되었습니다!!', fg='red'))
        token = click.prompt('새 토큰을 입력하세요')

    # 토큰을 파일로 입력
    with open(TOKEN_FILE_NAMES[enterprise], 'w') as token_file:
        token_file.write(token)

    return token


@click.command()
@click.option('--token', help='토큰 입력')
@click.option('--enterprise', help='GitHub Enterprise mode', is_flag=True, default=False)
def token_manage(token, enterprise):
    """ Managing your GitHub and GitHub ENTERPRISE TOKEN. """
    if token:
        valid_token = token_to_file(token, enterprise)
    else:
        try:
            with open(TOKEN_FILE_NAMES[enterprise]) as token_file:
                token = token_file.read()

                if confirm_token(token, enterprise):
                    valid_token = token
                else:
                    valid_token = token_to_file(token, enterprise)
        except FileNotFoundError:
            valid_token = token_to_file(token, enterprise)

    click.echo(valid_token + click.style(' 은 유효한 토큰입니다', fg='blue'))

if __name__ == '__main__':
    token_manage()
