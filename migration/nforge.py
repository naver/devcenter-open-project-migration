# -*- coding: utf-8 -*-
import json
import logging
import os
import time

import requests
from builtins import input
from future.moves.urllib.parse import urlparse
from requests import request
from tqdm import tqdm

from cli import DATA_DIR
from migration import CODE_INFO_FILE, ok_code, DOWNLOADS_DIR, ISSUES_DIR, ISSUE_ATTACH_DIR
from migration.helper import making_soup, make_dirs


class Milestone:
    def __init__(self, milestone):
        self.id = milestone.id.get_text()
        self.group_artifact_id = milestone.group_artifact_id.get_text()
        self.features = milestone.features.get_text()
        self.due_date = milestone.duedate.get_text()
        self.status = milestone.status.get_text()

        status = 'open' if self.status is 'PROGRESS' else 'closed'

        self.json = json.dumps(
            dict(
                title=self.features,
                state=status,
                description=self.features,
                due_on=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(self.due_date)))
            )
        )

    def __str__(self):
        return self.json


class InvalidProjectError(Exception):
    def __init__(self, pr_name):
        self.pr_name = pr_name

    def __str__(self):
        not_found_project_msg = '{0} does not exist.'.format(self.pr_name)
        return not_found_project_msg


class Nforge:
    cookies = None
    SUB_DIRS = ['raw', 'xml', 'json']
    NFORGE_URLS = ['http://staging.dev.naver.com', 'http://devcode.nhncorp.com/']
    ID_TAGS = ['artifact_id', 'release_id']

    COOKIE_FILE = 'COOKIES'
    COOKIE_PATH = os.path.join(DATA_DIR, COOKIE_FILE)

    def __init__(self, project_name, dev_code):
        project_type = 'dev_code' if dev_code else 'open_project'
        self.path = os.path.join(Nforge.__name__, project_type, project_name)
        self.issues_path = os.path.join(self.path, ISSUES_DIR)
        self.downloads_path = os.path.join(self.path, DOWNLOADS_DIR)

        self.paths = [self.issues_path, self.downloads_path]

        # 폴더 구조 생성
        make_dirs(self.issues_path)
        make_dirs(self.downloads_path)

        for sub_dir in self.SUB_DIRS:
            issue_data = os.path.join(self.issues_path, sub_dir)
            download_data = os.path.join(self.downloads_path, sub_dir)

            if not os.path.exists(issue_data):
                os.mkdir(issue_data)
            if not os.path.exists(download_data):
                os.mkdir(download_data)

        if dev_code:
            # Get cookies from COOKIES file
            self.cookies = dict()
            nss_tok = 'nssTok'

            try:
                with open(self.COOKIE_PATH) as f:
                    cookie_list = [cookie for cookie in f]

                for cookie in cookie_list:
                    cookie_split = cookie.split(' ')
                    self.cookies[cookie_split[0]] = cookie_split[1].replace('\n', '')
            except EnvironmentError:
                self.cookies[nss_tok] = str(input(nss_tok + ' : '))

                with open(self.COOKIE_PATH, 'w') as f:
                    f.write(nss_tok + ' ' + self.cookies[nss_tok])

        self.url = self.NFORGE_URLS[dev_code]
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
            # Board and issue list
            url = '{0}/{1}'.format(self.project_url, parse_type)
            r = request("GET", url, cookies=self.cookies)

            # HTML parsing
            soup = making_soup(r.content, 'html')

            # Get selected class by each parse_type
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

        # Cannot migrate if url starts with staging.
        if self.vcs is 'git':
            vcs_username = 'nobody'
            vcs_password = 'nobody'
            vcs = 'git'
            # git must use https protocol
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
        wiki_path = os.path.join(self.path, ISSUES_DIR, self.SUB_DIRS[0])
        attach_file_path = os.path.join(wiki_path, ISSUE_ATTACH_DIR)

        if not os.path.exists(attach_file_path):
            os.mkdir(attach_file_path)

        project_news_item = self.project_main_soup.find('ul', class_='tab-small').findAll('ul')
        wiki_pages = dict()

        for a_tag in project_news_item[2].findAll('a'):
            url = self.url + a_tag['href'] + '?action=edit'
            wiki_request = request("GET", url, cookies=self.cookies).content
            doc_name = a_tag['title']

            # Except error for private wiki
            # Private wiki cannot get text area tag
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
            doc_ids = [id_tag.get_text() for id_tag in parsed_board.findAll(self.ID_TAGS[is_download])]

            progress_bar = tqdm(doc_ids)

            xml_path = os.path.join(self.paths[is_download], self.SUB_DIRS[1], board if not is_download else '')

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

                # Precaution of xml encoding error
                xml_bytes = doc_requests.content.decode('utf-8', 'replace')
                parsed_xml = xml_bytes.replace('&#13;', '\n')
                xml_lists[is_download].append(parsed_xml)

                with open(os.path.join(xml_path, fn), 'w') as xml_file:
                    xml_file.write(parsed_xml)

        return xml_lists
