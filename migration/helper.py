# -*- coding: utf-8 -*-
import random
import string
import sys

from bs4 import BeautifulSoup


def making_soup(content, doc_type):
    return BeautifulSoup(content, 'lxml' if doc_type is 'html' else 'xml')


def get_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


# python 2.* 버전일 경우 인코딩을 강제로 정해줘야 함
# 각 파일마다 동작시킬 것
def set_encoding():
    reload(sys)
    sys.setdefaultencoding('utf-8')


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