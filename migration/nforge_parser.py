import glob
import json
import mimetypes
import os
import time
from urllib.parse import urljoin

import requests
from migration import ISSUES_DIR, DOWNLOADS_DIR, ISSUE_ATTACH_DIR

from .helper import making_soup


class NforgeParser:
    def __init__(self, github_session, project_path, **kwargs):
        self.github_session = github_session
        self.path = project_path
        # self.cookies = get_cookies()

        with open(os.path.join(project_path, 'project_info.json')) as pr_info:
            info = json.load(pr_info)

        self.pr_name = info['name']
        self.url = info['url']

        self.issues_dir = os.path.join(self.path, ISSUES_DIR)
        self.downloads_dir = os.path.join(self.path, DOWNLOADS_DIR)
        self.attach_path = os.path.join(self.issues_dir, ISSUE_ATTACH_DIR)

        xml_files = kwargs.get('xml_files')

        if xml_files:
            self.raw_issues = xml_files[0]
            self.raw_downloads = xml_files[1]
        else:
            self.raw_issues, self.raw_downloads = self.read_files()

        self.issues = [making_soup(issue, 'xml') for issue in self.raw_issues]
        self.downloads = [making_soup(download, 'xml') for download in self.raw_issues]

        self.file_link_basis = '{0}/{1}/{2}/wiki/attachFile'.format(github_session.url, github_session.username,
                                                                    github_session.repo_name)

    def make_issue_json(self):
        date_type = "%Y/%m/%d %H:%M:%S"

        for issue in self.issues:
            issue_id = issue.find('artifact_id').get_text()
            author = issue.find('author').get_text().replace(' ', '')
            assignee = issue.find('assignee').get_text().replace(' ', '')
            title = issue.find('title').get_text()
            body = issue.find('description').get_text()
            open_date_str = issue.find('open_date').get_text()
            close_date = issue.find('close_date').get_text()

            open_date = time.strftime(date_type, time.localtime(int(open_date_str)))
            closed = False if close_date == '0' else True

            attachments = issue.find('attachments')

            attachments_link = self.attach_links(attachments, issue_id)

            print(attachments_link)

    def attach_links(self, attachments, content_id):
        attach_markdown = ''

        if attachments:
            for item in attachments:
                # 간혹 item 갯수가 0인 게 있음
                if attachments.index(item) == 0:
                    attach_markdown = '\n\n-----\n### Attachments\n'

                link = item.find('link').get_text()
                fn = item.find('name').get_text()
                fid = item.find('id').get_text()

                # 파일 다운로드
                down_url = urljoin(self.url, link)
                down_path = os.path.join(self.attach_path, content_id, fid)

                if not os.path.exists(down_path):
                    downloaded = requests.request("GET", down_url, stream=True, cookies=self.cookies)

                    if not os.path.exists(down_path):
                        os.makedirs(down_path)

                    with open(os.path.join(down_path, fn), 'wb') as f:
                        f.write(downloaded.content)

                file_path = '/{0}/{1}/{2}'.format(content_id, fid, fn)
                github_link = self.file_link_basis + file_path

                if mimetypes.guess_type(fn)[0].split('/')[0] == 'image':
                    attach_markdown += '* {0}\n\n\t![{0}]({1})\n\n'.format(fn, github_link)
                else:
                    attach_markdown += '* [{0}]({1})\n\n'.format(fn, github_link)

        return attach_markdown

    def make_download_json(self):
        pass

    def read_files(self):
        issue_files, download_files = list(), list()
        issue_xml_path = os.path.join(self.issues_dir, 'xml') + '/*.xml'
        download_xml_path = os.path.join(self.downloads_dir, 'xml') + '/*.xml'

        issue_paths = glob.glob(issue_xml_path)
        download_paths = glob.glob(download_xml_path)

        for issue_fn in issue_paths:
            with open(issue_fn) as f:
                issue_files.append(f.read())

        for download_fn in download_paths:
            with open(download_fn) as f:
                download_files.append(f.read())

        return issue_files, download_files
