# -*- coding: utf-8 -*-
import json
import logging
import os
from urllib.parse import urlparse

import requests
from migration import CODE_INFO_FILE, ok_code, DOWNLOADS_DIR, ISSUES_DIR, ISSUE_ATTACH_DIR
from migration.helper import making_soup, get_cookies, make_dirs
from migration.nforge_object import Milestone
from requests import request
from tqdm import tqdm


class InvalidProjectError(Exception):
    def __init__(self, pr_name):
        self.pr_name = pr_name

    def __str__(self):
        not_found_project_msg = '{0}는 없는 프로젝트입니다.'.format(self.pr_name)
        return not_found_project_msg


# html 을 파싱해서 최대한 정보를 뺴와야 함
class Nforge:
    open_project_url = 'http://staging.dev.naver.com'
    dev_code_url = 'http://devcode.nhncorp.com'

    cookies = None
    sub_dirs = ['raw', 'xml', 'json']
    nforge_urls = ['http://staging.dev.naver.com', 'http://devcode.nhncorp.com/']
    id_tags = ['artifact_id', 'release_id']

    def __init__(self, project_name, dev_code):
        """
        Nforge 객체의 생성자
        :param project_name: 프로젝트 이름
        :param dev_code: DevCode 프로젝트인지
        """
        project_type = 'dev_code' if dev_code else 'open_project'
        self.path = os.path.join(Nforge.__name__, project_type, project_name)
        self.issues_path = os.path.join(self.path, ISSUES_DIR)
        self.downloads_path = os.path.join(self.path, DOWNLOADS_DIR)

        self.paths = [self.issues_path, self.downloads_path]

        # 폴더 구조 생성
        make_dirs(self.issues_path)
        make_dirs(self.downloads_path)

        for sub_dir in self.sub_dirs:
            issue_data = os.path.join(self.issues_path, sub_dir)
            download_data = os.path.join(self.downloads_path, sub_dir)

            if not os.path.exists(issue_data):
                os.mkdir(issue_data)
            if not os.path.exists(download_data):
                os.mkdir(download_data)

        if dev_code:
            self.cookies = get_cookies()

        self.url = self.nforge_urls[dev_code]
        self.name = project_name

        self.project_url = '{0}/projects/{1}'.format(self.url, self.name)

        self.project_main_html = requests.request('GET', self.project_url, cookies=self.cookies).content
        self.project_main_soup = making_soup(self.project_main_html, 'html')

        src_soup = making_soup(request("GET", self.project_url + '/src', cookies=self.cookies).content, 'html')
        self.vcs = 'svn' if src_soup.find('div', class_='code_contents') else 'git'
        self.urls = self.create_url()

        with open(os.path.join(self.path, 'project_info.json'), 'w') as pr_info:
            pr_info.write(json.dumps(dict(
                name=project_name,
                url=self.url,
                cookies=self.cookies
            )))

    def __str__(self):
        return self.name

    def create_url(self):
        urls = dict()
        types = ['issue', 'forum', 'download']

        for parse_type in types:
            # 게시판 및 이슈 목록
            url = '{0}/{1}'.format(self.project_url, parse_type)
            r = request("GET", url, cookies=self.cookies)

            # HTML 파싱
            soup = making_soup(r.content, 'html')
            # 각 issue, forum, download 타입에 따라서
            # 선택된 클래스를 받아온다
            cond_class = 'menu_{0} on selected'.format(parse_type)
            class_list = soup.find(class_=cond_class)

            if class_list is not None:
                for a in class_list.ul.find_all('a'):
                    text = a.get_text()
                    name = a['href'].split('/projects/' + self.name + '/')[1]
                    urls[text] = '{0}/{1}.xml'.format(self.project_url, name)
            else:
                urls[parse_type] = '{0}.xml'.format(url)

        return urls

    def check_valid_project(self):
        title = self.project_main_html.title.get_text()
        assert title is not None

        if '오류' in title:
            raise InvalidProjectError(self.name)

    def code_info(self):
        netloc = urlparse(self.url).netloc
        url = netloc.replace('staging.', '')

        # staging. 으로 시작하면 migration 이 되지 않음..
        if self.vcs is 'git':
            vcs_username = 'nobody'
            vcs_password = 'nobody'
            vcs = 'git'
            # git 은 반드시 https 프로토콜로 넘기기!!
            vcs_url = 'https://{3}:{3}@{2}/{0}/{1}.{0}'.format(vcs, self.name, url, vcs_username)
        else:
            vcs_username = 'anonsvn'
            vcs_password = 'anonsvn'
            vcs = 'subversion'
            vcs_url = 'https://{2}/{0}/{1}'.format(self.vcs, self.name, url)

        code_info_json = json.dumps(dict(
            vcs=vcs,
            vcs_url=vcs_url,
            vcs_username=vcs_username,
            vcs_password=vcs_password
        ))

        with open(os.path.join(self.path, CODE_INFO_FILE), 'w') as code_info:
            code_info.write(code_info_json)

        return code_info_json

    def wiki(self):
        wiki_path = os.path.join(self.path, ISSUES_DIR, self.sub_dirs[0])
        attach_file_path = os.path.join(wiki_path, ISSUE_ATTACH_DIR)

        if not os.path.exists(attach_file_path):
            os.mkdir(attach_file_path)

        project_news_item = self.project_main_soup.find('ul', class_='tab-small').findAll('ul')
        wiki_pages = dict()

        for a_tag in project_news_item[2].findAll('a'):
            url = self.url + a_tag['href'] + '?action=edit'
            wiki_request = request("GET", url, cookies=self.cookies).content
            doc_name = a_tag['title']

            # 위키가 비공개라 text area 태그를 받아오지 못하는 경우가 간혹 있음
            try:
                wiki_content = making_soup(wiki_request, 'html').textarea.get_text()
            except AttributeError:
                wiki_request = request("GET", self.url + a_tag['href'], cookies=self.cookies).content
                wiki_content = making_soup(wiki_request, 'html').find('div', id='mycontent')

            wiki_pages[doc_name] = str(wiki_content)

            with open(os.path.join(wiki_path, doc_name) + '.md', 'w') as wiki_doc:
                wiki_doc.write(str(wiki_content))

        return list(wiki_pages.keys())

    def developers(self):
        class_name = 'developer_info_list'
        dev_info_list = self.project_main_soup.find('div', class_name).ul.find_all('li')

        developers = []
        with open(os.path.join(self.path, 'developers.txt'), 'w') as developer_file:
            for li in dev_info_list:
                developer_name = li.a.get_text().replace(' ', '')
                developers.append(developer_name)
                developer_file.write(developer_name + '\n')

        return developers

    def milestones(self):
        milestone_url = self.project_url + '/milestone.xml'
        milestone_xml = request("GET", milestone_url, cookies=self.cookies).content
        xml_soup = making_soup(milestone_xml, 'xml')
        milestones_soup = xml_soup.findAll('milestone')
        milestones_path = os.path.join(self.path, 'milestones')

        if not os.path.exists(milestones_path):
            os.mkdir(milestones_path)

        milestones = list()

        if milestones_soup:
            for milestone in milestones_soup:
                ms = Milestone(milestone)
                ms_json = str(ms)
                milestones.append(ms_json)

                with open(os.path.join(milestones_path, ms.id) + '.json', 'w') as ms_file:
                    ms_file.write(ms_json)

        return milestones

    def boards_xml(self):
        # issue, download
        xml_lists = [list(), list()]

        for board, url in self.urls.items():
            is_download = board == 'download'

            get_board_request = requests.request("GET", url, cookies=self.cookies)
            parsed_board = making_soup(get_board_request.content, 'xml')
            doc_ids = [id_tag.get_text() for id_tag in parsed_board.findAll(self.id_tags[is_download])]

            progress_bar = tqdm(doc_ids)

            xml_path = os.path.join(self.paths[is_download], self.sub_dirs[1], board if not is_download else '')

            if not os.path.exists(xml_path) and not is_download:
                os.mkdir(xml_path)

            for doc_id in progress_bar:
                progress_bar.set_description('Now making {0}.xml of {1}'.format(doc_id, board))

                fn = doc_id + '.xml'

                doc_req_url = '{0}/{1}/{2}.xml'.format(self.project_url, board, doc_id)
                doc_requests = requests.request('GET', doc_req_url, cookies=self.cookies)

                if not ok_code.match(str(doc_requests.status_code)):
                    logging.error('{0} HAS REQUEST ERROR {1}'.format(doc_id, doc_requests.status_code))
                    continue

                xml_bytes = doc_requests.content.decode('utf-8', 'replace')
                parsed_xml = xml_bytes.replace('&#13;', '\n')
                xml_lists[is_download].append(parsed_xml)

                with open(os.path.join(xml_path, fn), 'w') as xml_file:
                    xml_file.write(parsed_xml)

        return xml_lists
