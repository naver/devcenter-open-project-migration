import glob
import json
import mimetypes
import os
import sys
import time
import traceback
from urllib.parse import urljoin

import requests
from migration import ISSUES_DIR, DOWNLOADS_DIR, ISSUE_ATTACH_DIR, MILESTONES_DIR

from .helper import making_soup


class NforgeParser:
    print_type = "%Y/%m/%d %H:%M:%S"
    github_type = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, github_session, project_path, **kwargs):
        self.github_session = github_session
        self.path = project_path

        with open(os.path.join(project_path, 'project_info.json')) as pr_info:
            info = json.load(pr_info)

        self.pr_name = info['name']
        self.url = info['url']
        self.cookies = info['cookies']

        self.issues_dir = os.path.join(self.path, ISSUES_DIR)
        self.downloads_dir = os.path.join(self.path, DOWNLOADS_DIR)
        self.attach_path = os.path.join(self.issues_dir, ISSUE_ATTACH_DIR)
        self.milestone_dir = os.path.join(self.path, MILESTONES_DIR)

        xml_files = kwargs.get('xml_files')

        if xml_files:
            self.raw_issues = xml_files[0]
            self.raw_downloads = xml_files[1]
            self.raw_milestones = xml_files[2]
        else:
            self.raw_issues, self.raw_downloads, self.raw_milestones = self.read_files()

        self.issues = dict()

        for doc_type, raw_issues in self.raw_issues.items():
            self.issues[doc_type] = list()

            for raw_issue in raw_issues:
                self.issues[doc_type].append(making_soup(raw_issue, 'xml'))

        self.downloads = [making_soup(download, 'xml') for download in self.raw_issues]

        self.file_link_basis = '{0}/{1}/{2}/wiki/attachFile'.format(github_session.url, github_session.username,
                                                                    github_session.repo_name)

    def make_issue_json(self):
        for doc_type, issues in self.issues.items():
            for issue in issues:
                issue_id = issue.find('artifact_id').get_text()
                author = issue.find('author').get_text().replace(' ', '')
                assignee = issue.find('assignee').get_text().replace(' ', '')
                title = issue.find('title').get_text()
                body = issue.find('description').get_text()
                open_date_str = issue.find('open_date').get_text()
                close_date = issue.find('close_date').get_text()

                open_date = time.strftime(self.print_type, time.localtime(int(open_date_str)))
                closed = False if close_date == '0' else True

                attachments = issue.find('attachments')
                attachments_link = self.attach_links(attachments, issue_id)

                comments = issue.find('comments')

                assignee_text = 'and assigned to **{0}**'.format(assignee) if assignee != 'Nobody' else ''
                description = "This {0} created by **{1}** {2} | {3}\n\n------\n\n{4}{5}".format(
                    doc_type,
                    author,
                    assignee_text,
                    open_date,
                    body,
                    attachments_link)
                try:
                    comment_list = self.make_comments(comments)
                except AttributeError as e:
                    print(doc_type, issue_id)
                    traceback.print_exc(file=sys.stdout)

                    continue

                issue_json = json.dumps(
                    dict(
                        issue=dict(
                            title=title,
                            body=description,
                            closed=closed,
                            labels=[doc_type]
                        ),
                        comments=comment_list
                    )
                )

                with open(os.path.join(self.issues_dir, 'json', issue_id + '.json'), 'w') as json_file:
                    json_file.write(issue_json)

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
                attachments = None if not attachments_tag else attachments_tag.get_text()

                print_time = time.strftime(self.print_type, time.localtime(int(date)))
                github_time = time.strftime(self.github_type, time.localtime(int(date)))

                attach_links = self.attach_links(attachments, id_)

                c_body = "This comment created by **{0}** | {1}\n\n------\n\n{2}{3}".format(author, print_time, body,
                                                                                            attach_links)

                result.append({
                    "created_at": github_time,
                    "body": c_body
                })

        return result

    def attach_links(self, attachments, content_id):
        attach_markdown = ''

        if attachments and content_id:
            for item in attachments:
                # 간혹 item 갯수가 0인 게 있음
                if attachments.index(item) == 0:
                    attach_markdown = '\n\n-----\n### Attachments\n'
                link_tag = item.find('link')

                if not link_tag or link_tag == -1:
                    return ''
                else:
                    link = link_tag.get_text()

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
        download_files, milestone_files = list(), list()
        issue_basis_path = os.path.join(self.issues_dir, 'xml')

        doc_types = os.listdir(issue_basis_path)
        issue_files = {doc_type: list() for doc_type in doc_types}

        issue_xml_path = os.path.join(issue_basis_path, '*/*.xml')

        download_xml_path = os.path.join(self.downloads_dir, 'xml') + '/*.xml'
        milestone_xml_path = os.path.join(self.milestone_dir, 'xml') + '/*.xml'

        issue_paths = glob.glob(issue_xml_path)
        download_paths = glob.glob(download_xml_path)
        milestone_paths = glob.glob(milestone_xml_path)

        for issue_fn in issue_paths:
            split_path = issue_fn.replace(issue_basis_path, '').split('/')
            doc_type = split_path[1]

            with open(issue_fn) as f:
                issue_files[doc_type].append(f.read())

        for download_fn in download_paths:
            with open(download_fn) as f:
                download_files.append(f.read())

        for milestone_fn in milestone_paths:
            with open(milestone_fn) as f:
                download_files.append(f.read())

        return issue_files, download_files, milestone_files
