# -*- coding: utf-8 -*-
#!/usr/bin/env python
import platform
from bs4 import BeautifulSoup

# python 2.* 버전일 경우 인코딩을 강제로 정해줘야 함
# 각 파일마다 동작시킬 것
def set_encoding():
    if platform.python_version()[0] is '2':
        reload(sys)
        sys.setdefaultencoding('utf-8')

making_soup = lambda content,type: BeautifulSoup(content,'lxml' if type is 'html' else 'xml')
