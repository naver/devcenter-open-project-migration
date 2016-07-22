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
    # 마일스톤 있는지 O
    # 게시판 종류
    # 이슈 종류
    # 다운로드 종류

    def __init__(self, project_name, url):
        self.api_url = url
        self.project_url = '{0}/projects/{1}'.format(url, project_name)

        self.__check_valid_project(project_name)

        self.project_name = project_name
        self.developers = self.__set_developers()

        src_soup = making_soup(request("GET", self.project_url + '/src').content, 'html')
        self.vcs = 'svn' if src_soup.find('div', class_='code_contents') else 'git'

        self.wiki_pages = self.__set_wiki_pages()
        self.milestones = self.__set_milestones()

        self.urls = self.create_url()

        # self.issues = self.__get_issues_json(modified_urls)

    def __str__(self):
        return self.project_name

    def __check_valid_project(self, pr_name):

        r = request("GET", self.project_url)
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
            url = self.api_url + a_tag['href'] + '?action=edit'
            wiki_request = request("GET", url).content
            wiki_content = making_soup(wiki_request, 'html').textarea.get_text()
            wiki_pages[a_tag['title']] = wiki_content

        return wiki_pages

    def __set_milestones(self):
        milestone_url = self.project_url + '/milestone.xml'
        milestone_xml = request("GET", milestone_url).content
        xml_soup = making_soup(milestone_xml, 'xml')
        milestones_soup = xml_soup.findAll('milestone')

        if not milestones_soup:
            return None

        return [Milestone(milestone) for milestone in milestones_soup]

    def create_url(self):
        urls = dict()
        types = ['issue', 'forum', 'download']

        for parse_type in types:
            # 게시판 및 이슈 목록
            url = '{0}/{1}'.format(self.project_url, parse_type)
            r = request("GET", url)

            # HTML 파싱
            soup = making_soup(r.content, 'html')
            # 각 issue, forum, download 타입에 따라서
            # 선택된 클래스를 받아온다
            cond_class = 'menu_{0} on selected'.format(parse_type)
            class_list = soup.find(class_=cond_class)

            if class_list is not None:
                for a in class_list.ul.find_all('a'):
                    text = a.get_text()
                    name = a['href'].split('/projects/' + self.project_name + '/')[1]
                    urls[text] = '{0}/{1}.xml'.format(self.project_url, name)
            else:
                urls[parse_type] = '{0}.xml'.format(url)

        return urls
