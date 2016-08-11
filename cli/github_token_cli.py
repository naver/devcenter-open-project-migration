# -*- coding: utf-8 -*-
import os

import click
import requests
from cli import API_URLS, DATA_DIR, FILE_NAMES


def get_file_path(file_type, enterprise):
    """
    Get file path by file type and enterprise
    :param file_type: Some file type (token ...)
    :param enterprise: Is GitHub enterprise
    :return: Path of file
    """
    return os.path.join(DATA_DIR, FILE_NAMES[file_type][enterprise])


def confirm_token(token, enterprise):
    """
    Confirm token
    :param token: Github token
    :param enterprise: Is enterprise
    :return: Is github token valid.
    """
    url = API_URLS[enterprise] + 'user?access_token=' + token
    return True if requests.request("GET", url).status_code is 200 else False


def token_to_file(token, file_path, enterprise):
    """
    Save token to file
    :param token: GitHub token
    :param file_path: Path of token file.
    :param enterprise: Is enterprise?
    :return: token
    """

    # Input token while token is valid.
    while not confirm_token(token, enterprise):
        click.echo(click.style(token + ' is a invalid token!!', fg='red'))
        token = click.prompt('Please input new token')

    # Input token to file.
    with open(file_path, 'w') as token_file:
        token_file.write(token)

    return token


def read_token_from_file(file_path, enterprise):
    """
    Read token from file
    :param file_path: Path of token file
    :param enterprise: Is enterprise?
    :return: Token or call other function
    """
    token = str()

    try:
        with open(file_path) as token_file:
            token = token_file.read()

        return token if confirm_token(token, enterprise) else token_to_file(token, file_path, enterprise)
    except FileNotFoundError:
        return token_to_file(token, file_path, enterprise)


@click.command()
@click.option('--token', help='Input token')
@click.option('--enterprise', help='GitHub Enterprise mode', is_flag=True, default=False)
def github_token_cli(token, enterprise):
    """ Managing your GitHub and GitHub ENTERPRISE TOKEN. """
    token_file_path = get_file_path('token', enterprise)

    msg = 'GitHub Enterprise' if enterprise else 'GitHub'

    valid_token = token_to_file(token, token_file_path, enterprise) if token \
        else read_token_from_file(token_file_path, enterprise)
    click.echo(valid_token + click.style(' is valid ' + msg + ' token', fg='blue'))

if __name__ == '__main__':
    github_token_cli()
