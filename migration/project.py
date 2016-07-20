#!env python
# -*- coding: utf-8 -*-
from requests import request
from .helper import making_soup
from .milestone import Milestone


class InvalidProjectError(Exception):
    def __init__(self, pr_name):
        self.pr_name = pr_name

    def __str__(self):
        not_found_project_msg = '{0}는 없는 프로젝트입니다.'.format(self.pr_name)
        return not_found_project_msg


# html 을 파싱해서 최대한 정보를 뺴와야 함
class Project:
    # 프로젝트 이름 O
    # 개발자 정보 O
    # 사용하는 vcs 종류 O
    # 위키 현황 O
    # 마일스톤 있는지
    # 마지막에 wiki로 내용 푸시하기
    # 게시판 종류
    # 이슈 종류
    # 다운로드 종류

    def __init__(self, project_name, url):
        self._naver_api_url = url
        self._project_url = '{0}/projects/{1}'.format(url, project_name)

        self.__check_valid_project(project_name)

        self._project_name = project_name
        self._developers = self.__set_developers()

        src_soup = making_soup(request("GET", self._project_url + '/src').content, 'html')
        self._vcs = 'svn' if src_soup.find('div', class_='code_contents') else 'git'

        self._wiki_pages = self.__set_wiki_pages()
        self._milestones = self.__set_milestones()

    def __str__(self):
        return self._project_name

    def __check_valid_project(self, pr_name):

        r = request("GET", self._project_url)
        self.__html = making_soup(r.content, 'html')

        title = self.__html.title.get_text()
        assert title is not None

        if '오류' in title:
            raise InvalidProjectError(pr_name)

    def __set_developers(self):
        class_name = 'developer_info_list'
        dev_info_list = self.__html.find('div', class_name).ul.find_all('li')

        developers = [li.a.get_text().replace(' ', '') for li in dev_info_list]

        return developers

    def __set_wiki_pages(self):
        project_news_item = self.__html.find('ul', class_='tab-small').findAll('ul')
        wiki_pages = dict()

        for a_tag in project_news_item[2].findAll('a'):
            url = self._naver_api_url + a_tag['href'] + '?action=edit'
            wiki_request = request("GET", url).content
            wiki_content = making_soup(wiki_request, 'html').textarea
            wiki_pages[a_tag['title']] = wiki_content

        return wiki_pages

    def __set_milestones(self):
        milestone_url = self._project_url + '/milestone.xml'
        milestone_xml = request("GET", milestone_url).content
        xml_soup = making_soup(milestone_xml, 'xml')
        milestones_soup = xml_soup.findAll('milestone')

        if not milestones_soup:
            return None

        milestones = [Milestone(milestone) for milestone in milestones_soup]

        return milestones
