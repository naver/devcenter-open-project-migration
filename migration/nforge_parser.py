import glob
import json
import mimetypes
import os
import time
from urllib.parse import urljoin

import requests
from migration import ISSUES_DIR, DOWNLOADS_DIR, ISSUE_ATTACH_DIR
from tqdm import tqdm

from .helper import making_soup, get_fn


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
        self.attach_path = os.path.join(self.issues_dir, 'raw', ISSUE_ATTACH_DIR)

        xml_files = kwargs.get('xml_files')

        if xml_files:
            self.raw_issues = xml_files[0]
            self.raw_downloads = xml_files[1]
        else:
            self.raw_issues, self.raw_downloads = self.read_files()

        self.issues = dict()

        for doc_type, raw_issues in self.raw_issues.items():
            self.issues[doc_type] = list()

            for raw_issue in raw_issues:
                self.issues[doc_type].append(making_soup(raw_issue, 'xml'))

        self.downloads = {
            release_id: making_soup(download, 'xml') for release_id, download in self.raw_downloads.items()
            }

        self.file_link_basis = '{0}/{1}/{2}/wiki/attachFile'.format(github_session.url, github_session.username,
                                                                    github_session.repo_name)

    def make_issue_json(self):
        for doc_type, issues in self.issues.items():
            progress_bar = tqdm(issues)

            for issue in progress_bar:
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

                progress_bar.set_description('Now making {0}.json of {1}'.format(issue_id, doc_type))

                open_date = time.strftime(self.print_type, time.localtime(int(open_date_str)))
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
                            labels=[doc_type]
                        ),
                        comments=comment_list
                    ), ensure_ascii=False)

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

    def attach_links(self, items, content_id):
        attach_markdown = ''

        if items and content_id:
            for item in items:
                # 간혹 item 갯수가 0인 게 있음
                if items.index(item) == 0:
                    attach_markdown = '\n\n-----\n### Attachments\n'

                link_tag = item.find('link')
                id_tag = item.find('id')

                if not link_tag or link_tag == -1:
                    return ''
                else:
                    link = link_tag.get_text()

                fn = link.split('/')[-1]
                fid = 'No file id' if not id_tag else id_tag.get_text()

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
        progress_bar = tqdm(self.downloads.items())

        for release_id, soup in progress_bar:
            raw_file_path = os.path.join(self.downloads_dir, 'raw', release_id)

            if not os.path.exists(raw_file_path):
                os.mkdir(raw_file_path)

            progress_bar.set_description('Now making {0}.json of {1}'.format(release_id, 'download'))

            name_tag = soup.find('name')
            desc_tag = soup.find('description')
            files_tag = soup.find('files')

            name = 'No title' if not name_tag else name_tag.get_text()
            desc = 'No desc' if not desc_tag else desc_tag.get_text()
            files = [] if not files_tag else files_tag

            version = str(self.get_version(name))

            with open(os.path.join(self.downloads_dir, 'json', release_id + '.json'), 'w') as json_file:
                json.dump(dict(
                    tag_name=version, target_commitish='master', name=name, body=desc, prerelease=False, draft=False
                ), json_file, ensure_ascii=False)

            for release_file in files.findAll('file'):
                file_id_tag = release_file.find('id')
                file_name_tag = release_file.find('name')
                fid = '0' if not file_id_tag else file_id_tag.get_text()

                if file_name_tag:
                    fn = file_name_tag.get_text()
                else:
                    continue

                file_down_url = '{0}/frs/download.php/{1}/{2}'.format(self.url, fid, fn)
                file_raw = requests.request('GET', file_down_url, stream=True, cookies=self.cookies).content

                with open(os.path.join(raw_file_path, fn), 'wb') as raw_file:
                    raw_file.write(file_raw)

    def get_version(self, title):
        temp = title.upper().replace(self.pr_name.upper(), '')

        try:
            result = int(temp)

            if result < 0:
                return abs(result)
        except ValueError:
            return temp.replace(' ', '')

    def read_files(self):
        download_files = dict()
        issue_basis_path = os.path.join(self.issues_dir, 'xml')

        doc_types = os.listdir(issue_basis_path)
        issue_files = {doc_type: list() for doc_type in doc_types}

        issue_xml_path = os.path.join(issue_basis_path, '*/*.xml')
        download_xml_path = os.path.join(self.downloads_dir, 'xml') + '/*.xml'

        issue_paths = glob.glob(issue_xml_path)
        download_paths = glob.glob(download_xml_path)

        for issue_fn in issue_paths:
            split_path = issue_fn.replace(issue_basis_path, '').split('/')
            doc_type = split_path[1]

            with open(issue_fn) as f:
                issue_files[doc_type].append(f.read())

        for download_path in download_paths:
            with open(download_path) as f:
                download_files[get_fn(download_path, 0)] = f.read()

        return issue_files, download_files
