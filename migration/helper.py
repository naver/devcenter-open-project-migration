# -*- coding: utf-8 -*-
import os
import random
import string
import sys

import click
from bs4 import BeautifulSoup
from migration import COOKIE_PATH


def making_soup(content, doc_type):
    return BeautifulSoup(content, 'lxml' if doc_type is 'html' else 'xml')


def get_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def image_ext_check(ext):
    image_extensions = ['bmp', 'jpeg', 'jpg', 'png', 'gif', 'bmp']

    return True if ext.lower() in image_extensions else False


# python 2.* 버전일 경우 인코딩을 강제로 정해줘야 함
# 각 파일마다 동작시킬 것
def set_encoding():
    reload(sys)
    sys.setdefaultencoding('utf-8')


def get_cookies():
    cookies = dict()
    nss_tok = 'nssTok'

    try:
        with open(COOKIE_PATH) as f:
            cookie_list = [cookie for cookie in f]

        for cookie in cookie_list:
            cookie_split = cookie.split(' ')
            cookies[cookie_split[0]] = cookie_split[1].replace('\n', '')
    except FileNotFoundError:
        cookies[nss_tok] = str(input(nss_tok + ' : '))

        with open(COOKIE_PATH, 'w') as f:
            f.write(nss_tok + ' ' + cookies[nss_tok])

    return cookies


# Version name 을 어떻게든 얻어보고자 고군분투하는 함수
def get_version(repo_name, title):
    # temp = str.upper(title).replace(str.upper(self.,  _repo_name),'')
    temp = title.upper().replace(repo_name.upper(), '')
    try:
        result = int(temp)
        if result < 0:
            return abs(result)
    except:
        return temp.replace(' ', '')


def print_green(text):
    click.echo(click.style(text, fg='green'))


def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
