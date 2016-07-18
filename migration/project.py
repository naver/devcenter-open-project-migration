# -*- coding: utf-8 -*-
#!/usr/bin/env python

from requests import request
from .helper import making_soup

class InvalidProjectError(Exception):
     def __init__(self, pr_name):
         self.pr_name = pr_name
     def __str__(self):
         not_found_project_msg = '{0}는 없는 프로젝트입니다.'.format(self.pr_name)
         return not_found_project_msg

# html 을 파싱해서 최대한 정보를 뺴와야 함
class Project:
    # 프로젝트 이름 ok
    # 개발자 정보
    # 위키 현황 -> 수동으로 해야 할듯
    # 게시판 종류
    # 이슈 종류
    # 다운로드 종류
    # 마일스톤 있는지
    # 사용하는 vcs 종류
    def __init__(self,project_name,url):
        self._naver_api_url = url
        self.__check_valid_project(project_name)

        self._project_name = project_name
        self._developers = self.__get_developers()

    def __check_valid_project(self,pr_name):
        project_url = '{0}/projects/{1}'.format(self._naver_api_url,pr_name)
        r = request("GET",project_url)
        self.__html = making_soup(r.content,'html')

        title = self.__html.title.get_text()
        assert title is not None

        if '오류' in title:
            raise InvalidProjectError(pr_name)

    def __get_developers(self):
        class_name = 'developer_info_list'
        dev_info_list = self.__html.find('div',class_name).ul.find_all('li')

        developers = [li.a.get_text().replace(' ','') for li in dev_info_list]

        return developers
