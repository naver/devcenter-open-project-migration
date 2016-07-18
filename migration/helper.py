# -*- coding: utf-8 -*-
#!/usr/bin/env python
import platform
from bs4 import BeautifulSoup
from requests import request
import sys

making_soup = lambda content,type: BeautifulSoup(content,'lxml' if type is 'html' else 'xml')

# python 2.* 버전일 경우 인코딩을 강제로 정해줘야 함
# 각 파일마다 동작시킬 것
def set_encoding():
    if platform.python_version()[0] is '2':
        reload(sys)
        sys.setdefaultencoding('utf-8')


def check_validate_project_name(pr_name):
    assert type(pr_name) is str

    project_url = 'http://staging.dev.naver.com/projects/{0}'.format(pr_name)
    r = request("GET",project_url)
    soup = BeautifulSoup(r.content,'lxml')

    title = soup.title.get_text()
    assert title is not None

    return False if '오류' in title else True
