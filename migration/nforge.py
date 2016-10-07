# -*- coding: utf-8 -*-
"""
   Copyright 2016 NAVER Corp.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import hashlib
import logging
import mimetypes
import os
import time

import requests
import json
from builtins import str, open
from cli import DIRS
from future.moves.urllib.parse import urlparse, urljoin
from migration import CODE_INFO_FILE, ok_code, DOWNLOADS_DIR, ISSUES_DIR, ISSUE_ATTACH_DIR
from migration.exception import InvalidCookieError, InvalidProjectError, NoSrcError
from migration.helper import making_soup, make_dirs, get_fn
from tqdm import tqdm


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


class Nforge:
    cookies = None
    SUB_DIRS = ('raw', 'xml', 'json')
    NFORGE_URLS = ('http://dev.naver.com', 'http://devcode.nhncorp.com/')
    ID_TAGS = ('artifact_id', 'release_id')

    COOKIE_FILE = 'COOKIES'
    COOKIE_PATH = os.path.join(DIRS[0], COOKIE_FILE)

    print_type = "%Y/%m/%d %H:%M:%S"
    github_type = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, project_name, dev_code, public):
        self.name = project_name
        self.url = self.NFORGE_URLS[dev_code]
        self.dev_code = dev_code

        self.project_url = '{0}/projects/{1}'.format(self.url, self.name)

        if dev_code or not public:
            # Get cookies from COOKIES file
            self.cookies = dict()

            try:
                with open(self.COOKIE_PATH) as f:
                    cookie_list = [cookie for cookie in f]

                for cookie in cookie_list:
                    cookie_split = cookie.split('=')
                    self.cookies[cookie_split[0]] = cookie_split[1].replace('\n', '')
            except EnvironmentError:
                raise InvalidCookieError

        request_main_html = requests.get(self.project_url, cookies=self.cookies)

        self.project_main_html = request_main_html.content
        self.project_main_soup = making_soup(self.project_main_html, 'html')

        self.check_valid_project()

        project_type = 'dev_code' if dev_code else 'open_project'

        self.path = os.path.join(Nforge.__name__, project_type, project_name)
        self.issues_path = os.path.join(self.path, ISSUES_DIR)
        self.downloads_path = os.path.join(self.path, DOWNLOADS_DIR)
        self.attach_path = os.path.join(self.issues_path, 'raw', ISSUE_ATTACH_DIR)

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

        # get version control system information
        src_request = requests.get(self.project_url + '/src', cookies=self.cookies)
        src_soup = making_soup(src_request.content, 'html')
        src_title = src_soup.find('title').get_text()

        # if cannot find all related div tags, it raises NoSrcError
        if src_soup.find('div', class_='code_contents'):
            self.vcs = 'svn'
        elif '로그인' in src_title or '오류' in src_title:
            raise NoSrcError
        else:
            self.vcs = 'git'

        self.urls = self.create_url()

    def __str__(self):
        return self.name

    def create_url(self):
        urls = dict()
        types = ['issue', 'forum', 'download']

        for parse_type in types:
            # Board and issue list
            url = '{0}/{1}'.format(self.project_url, parse_type)
            r = requests.get(url, cookies=self.cookies)

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
        title = self.project_main_soup.title.get_text()
        assert title is not None

        if '오류' in title:
            raise InvalidProjectError(self.name)
        elif self.name not in title and self.dev_code:
            raise InvalidCookieError(self.cookies)

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

        code_info = json.dumps(dict(
            vcs=vcs,
            vcs_url=vcs_url,
            vcs_username=vcs_username,
            vcs_password=vcs_password
        ))

        with open(os.path.join(self.path, CODE_INFO_FILE), 'w', encoding='utf-8') as code_info_json:
            code_info_json.write(str(code_info))

        return code_info

    def wiki(self):
        wiki_path = os.path.join(self.path, ISSUES_DIR, self.SUB_DIRS[0])
        attach_file_path = os.path.join(wiki_path, ISSUE_ATTACH_DIR)

        if not os.path.exists(attach_file_path):
            os.mkdir(attach_file_path)

        project_news_item = self.project_main_soup.find('ul', class_='tab-small').findAll('ul')
        wiki_pages = dict()

        for a_tag in project_news_item[2].findAll('a'):
            url = self.url + a_tag['href'] + '?action=edit'
            wiki_request = requests.get(url, cookies=self.cookies).content
            doc_name = a_tag['title']

            # Except error for private wiki
            # Private wiki cannot get text area tag
            try:
                wiki_content = making_soup(wiki_request, 'html').textarea.get_text()
            except AttributeError:
                wiki_request = requests.get(self.url + a_tag['href'], cookies=self.cookies).content
                wiki_content = making_soup(wiki_request, 'html').find('div', id='mycontent')

            wiki_pages[doc_name] = str(wiki_content)

            with open(os.path.join(wiki_path, doc_name) + '.md', 'w') as wiki_doc:
                wiki_doc.write(str(wiki_content))

        return wiki_pages

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
        milestone_xml = requests.get(milestone_url, cookies=self.cookies).content
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
        for board, url in self.urls.items():
            is_download = board == 'download'

            get_board_request = requests.get(url, cookies=self.cookies)
            parsed_board = making_soup(get_board_request.content, 'xml')
            doc_ids = [id_tag.get_text() for id_tag in parsed_board.findAll(self.ID_TAGS[is_download])]

            progress_bar = tqdm(doc_ids)

            xml_path = os.path.join(self.paths[is_download], self.SUB_DIRS[1], board if not is_download else '')

            if not os.path.exists(xml_path) and not is_download:
                os.mkdir(xml_path)

            for doc_id in progress_bar:
                progress_bar.set_description('Now making {0}.xml and {0}.json of {1}'.format(doc_id, board))

                fn = doc_id + '.xml'

                doc_req_url = '{0}/{1}/{2}.xml'.format(self.project_url, board, doc_id)
                doc_requests = requests.get(doc_req_url, cookies=self.cookies)

                if not ok_code.match(str(doc_requests.status_code)):
                    logging.error('{0} HAS REQUEST ERROR {1}'.format(doc_id, doc_requests.status_code))
                    continue

                # Precaution of xml encoding error
                xml_bytes = doc_requests.content.decode('utf-8', 'replace')
                parsed_xml = xml_bytes.replace('&#13;', '\n')

                with open(os.path.join(xml_path, fn), 'w', encoding='utf-8') as xml_file:
                    xml_file.write(parsed_xml)

                soup = making_soup(parsed_xml, 'xml')

                if not is_download:
                    self.make_issue(board, soup)
                else:
                    self.make_download(doc_id, soup)

    def make_issue(self, doc_type, issue):
        issue_id_tag = issue.find('artifact_id')
        author_tag = issue.find('author')
        assignee_tag = issue.find('assignee')
        title_tag = issue.find('title')
        body_tag = issue.find('description')
        open_date_tag = issue.find('open_date')
        close_date_tag = issue.find('close_date')
        attachments_tag = issue.find('attachments')

        issue_id = '0' if not issue_id_tag else issue_id_tag.get_text()
        author = 'No author' if not author_tag else author_tag.get_text().replace(' ', '')
        assignee = 'No assignee' if not assignee_tag else assignee_tag.get_text().replace(' ', '')
        title = 'No title' if not title_tag else title_tag.get_text()
        body = 'No body' if not body_tag else body_tag.get_text()
        open_date_str = '0' if not open_date_tag else open_date_tag.get_text()
        close_date = '0' if not close_date_tag else close_date_tag.get_text()

        open_date = time.strftime(self.print_type, time.localtime(int(open_date_str)))
        create_date = time.strftime(self.github_type, time.localtime(int(open_date_str)))
        closed_date = time.strftime(self.github_type, time.localtime(int(close_date)))

        closed = False if close_date == '0' else True

        items = attachments_tag.findAll('item') if attachments_tag else None
        attachments_link = self.attach_links(items, issue_id)

        comments = issue.find('comments')

        assignee_text = 'and assigned to **{0}**'.format(assignee) if assignee != 'Nobody' else ''
        description = "This {0} created by **{1}** {2} | {3}\n\n------\n\n{4}{5}".format(
            doc_type,
            author,
            assignee_text,
            open_date,
            body,
            attachments_link)

        comment_list = self.make_comments(comments)

        issue_json = json.dumps(
            dict(
                issue=dict(
                    title=title,
                    body=description,
                    closed=closed,
                    labels=[doc_type],
                    created_at=create_date,
                    closed_at=closed_date
                ),
                comments=comment_list
            ))

        with open(os.path.join(self.issues_path, 'json', issue_id + '.json'), 'w') as json_file:
            json_file.write(str(issue_json))

    def make_download(self, release_id, soup):
        raw_file_path = os.path.join(self.downloads_path, 'raw', release_id)

        if not os.path.exists(raw_file_path):
            os.mkdir(raw_file_path)

        name_tag = soup.find('name')
        desc_tag = soup.find('description')
        files_tag = soup.find('files')

        name = 'No title' if not name_tag else name_tag.get_text()
        desc = 'No desc' if not desc_tag else desc_tag.get_text()

        version = str(self.get_version(name))

        download_json = dict(
            tag_name=version,
            target_commitish='master',
            name=name, body=desc,
            prerelease=False,
            draft=False
        )

        with open(os.path.join(self.downloads_path, 'json', release_id + '.json'), 'w') as json_file:
            json.dump(str(download_json), json_file, ensure_ascii=False)

        if files_tag:
            for release_file in files_tag.findAll('file'):
                file_id_tag = release_file.find('id')
                file_name_tag = release_file.find('name')
                fid = '0' if not file_id_tag else file_id_tag.get_text()

                if file_name_tag:
                    fn = file_name_tag.get_text()
                else:
                    continue

                file_down_url = '{0}/frs/download.php/{1}/{2}'.format(self.url, fid, fn)
                file_raw = requests.get(file_down_url, stream=True, cookies=self.cookies).content

                with open(os.path.join(raw_file_path, fn), 'wb') as raw_file:
                    raw_file.write(file_raw)

    def attach_links(self, items, content_id):
        attach_markdown = ''

        if items and content_id:
            for item in items:
                # Sometimes length of items is zero.
                if items.index(item) == 0:
                    attach_markdown = '\n\n-----\n### Attachments\n'

                link_tag = item.find('link')
                id_tag = item.find('id')

                if not link_tag or link_tag == -1:
                    return ''
                else:
                    link = link_tag.get_text()

                fn = link.split('/')[-1]
                ext = get_fn(fn, 1)
                fn_md5 = hashlib.md5(fn.encode('utf-8')).hexdigest() + ext
                fid = 'No file id' if not id_tag else id_tag.get_text()

                # Download files
                down_url = urljoin(self.url, link)
                down_path = os.path.join(self.attach_path, content_id, fid)

                if not os.path.exists(down_path):
                    downloaded = requests.get(down_url, stream=True, cookies=self.cookies)

                    if not os.path.exists(down_path):
                        os.makedirs(down_path)

                    with open(os.path.join(down_path, fn_md5), 'wb') as f:
                        f.write(downloaded.content)

                file_path = '/{0}/{1}/{2}'.format(content_id, fid, fn_md5)
                github_link = '{0}/wiki/attachFile' + file_path

                mime_type = mimetypes.guess_type(fn)[0]

                if mime_type and mime_type.split('/')[0] == 'image':
                    attach_markdown += '* {0}\n\n\t![{0}]({1})\n\n'.format(fn, github_link)
                else:
                    attach_markdown += '* [{0}]({1})\n\n'.format(fn, github_link)

        return attach_markdown

    def make_comments(self, comments):
        result = []

        if comments:
            for comment in comments.find_all('item'):
                id_tag = comment.find('id')
                description_tag = comment.find('description')
                author_tag = comment.find('author')
                attachments_tag = comment.find('attachments')
                date_tag = comment.find('pubDate')

                id_ = None if not id_tag else id_tag.get_text()
                body = 'No description' if not description_tag else description_tag.get_text()
                author = 'No author' if not author_tag else author_tag.get_text()
                date = '0' if not date_tag else date_tag.get_text()
                items = attachments_tag.findAll('item') if attachments_tag else None

                print_time = time.strftime(self.print_type, time.localtime(int(date)))
                github_time = time.strftime(self.github_type, time.localtime(int(date)))

                attach_links = self.attach_links(items, id_)

                c_body = "This comment created by **{0}** | {1}\n\n------\n\n{2}{3}".format(author, print_time, body,
                                                                                            attach_links)

                result.append({
                    "created_at": github_time,
                    "body": c_body
                })

        return result

    def get_version(self, title):
        temp = title.upper().replace(self.name.upper(), '')

        try:
            result = int(temp)

            if result < 0:
                return abs(result)
        except ValueError:
            return temp.replace(' ', '')
