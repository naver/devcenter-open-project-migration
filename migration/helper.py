# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup


def making_soup(content, doc_type):
    return BeautifulSoup(content, 'lxml' if doc_type is 'html' else 'xml')


def get_fn(path, mode=None):
    """
    :param path: 파일의 경로
    :param mode: 인덱스
    :return: mode 가 None이면 풀 파일이름 숫자면 오직 이름 혹은 확장자
    """
    if mode is None:
        return os.path.basename(path)
    else:
        if not type(mode) is int:
            raise ValueError
        else:
            return os.path.splitext(os.path.basename(path))[mode]


# Version name 을 어떻게든 얻어보고자 고군분투하는 함수
def get_version(repo_name, title):
    temp = title.upper().replace(repo_name.upper(), '')
    try:
        result = int(temp)
        if result < 0:
            return abs(result)
    except ValueError:
        return temp.replace(' ', '')


def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
