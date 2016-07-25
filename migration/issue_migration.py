#!env python
# -*- coding: utf-8 -*-
import json
import logging
import os
import subprocess
import time
from urllib.parse import urlparse

import click
import requests
from config import WIKI_DIR_NAME, BASIC_TOKEN_FILE_NAME
from tqdm import tqdm

from .helper import making_soup


def upload_asset_by_git(user_name, project_name, repo_name, token):
    click.echo('첨부파일 업로드를 시작합니다')
    push_wiki_git = 'https://{0}:{1}@github.com/{0}/{2}.wiki.git'.format(user_name, token, repo_name)

    curdir = os.getcwd()
    os.chdir(os.path.join(curdir, 'wiki_repos', project_name))

    git_commands = [
        ['git', 'init'],
        ['git', 'add', '--all'],
        ['git', 'commit', '-m', 'all asset commit'],
        ['git', 'remote', 'add', 'origin', push_wiki_git],
        ['git', 'pull', push_wiki_git, 'master'],
        ['git', 'push', '-f', push_wiki_git, 'master']
    ]

    for command in git_commands:
        subprocess.call(command)

    os.chdir(curdir)


def file_download(attach_path, url, file_name, artifact_id, file_id, **kwargs):
    comment_id = kwargs.get('comment_id')

    if not comment_id:
        down_path = '{0}/{1}/{2}/'.format(attach_path,
                                          artifact_id,
                                          file_id)
    else:
        down_path = '{0}/{1}/{2}/{3}/'.format(attach_path,
                                              artifact_id,
                                              comment_id,
                                              file_id)

    full_path = down_path + file_name

    if not os.path.exists(full_path):
        downloaded = requests.request("GET", url, stream=True)

        if not os.path.exists(down_path):
            os.makedirs(down_path)

        with open(full_path, 'wb') as f:
            f.write(downloaded.content)

        status_code = int(downloaded.status_code)
    else:
        status_code = 304

    return status_code


def milestone_migration(project, gh, repo_name, token):
    milestones = project.milestones
    milestone_post_url = '{0}/repos/{1}/{2}/milestones?access_token={3}'.format(gh._github_url, gh.user().login,
                                                                                repo_name, token)
    for milestone in milestones:
        requests.request("POST", milestone_post_url, data=str(milestone))


def get_attach_links(attachments, download_path, api_url, github_username, repo_name, artifact_id, github_url):
    attach_links = ''

    for item in attachments:
        body_file_link = item.find('link').get_text()
        body_file_name = item.find('name').get_text()
        body_file_id = item.find('id').get_text()

        down_url = "{0}{1}".format(api_url, body_file_link)
        file_download(download_path, down_url, body_file_name, artifact_id, body_file_id)

        body_uploaded_link = 'https://{5}/{0}/{1}/wiki/attachFile/{2}/{3}/{4}'.format(
            github_username,
            repo_name,
            artifact_id,
            body_file_id,
            body_file_name,
            github_url)

        attach_links += '* {0}\n\n\t![{0}]({1})\n\n'.format(body_file_name, body_uploaded_link)

    return attach_links


def get_comments(comments, api_url, attach_download_path, artifact_id, github_username, repo_name):
    result = []
    comment_list = comments.find_all('item')
    attach_links = ''

    for comment in comment_list:
        attachments = comment.attachments

        if comment.find('pubDate') is None \
                or comment.find('description') is None \
                or comment.find('author') is None \
                or comment.find('id') is None:
            continue

        id_ = comment.find('id').get_text()
        body = comment.find('description').get_text()
        author = comment.find('author').get_text()
        date = comment.find('pubDate').get_text()

        print_date_type = "%Y/%m/%d %H:%M:%S"
        github_time_type = "%Y-%m-%dT%H:%M:%SZ"

        print_time = time.strftime(print_date_type, time.localtime(int(date)))
        github_time = time.strftime(github_time_type, time.localtime(int(date)))

        if attachments:
            attach_links = '\n\n-----\n### Attachments\n'
            items = attachments.find_all('item')

            for item in items:
                file_id = item.find('id').get_text()
                file_link = item.find('link').get_text()
                file_name = file_link.split('/')[-1]
                down_url = "{0}{1}".format(api_url, file_link)

                file_download(attach_download_path, down_url, file_name, artifact_id, file_id, comment_id=id_)

                uploaded_link = 'https://github.com/{0}/{1}/wiki/attachFile/{2}/{3}/{4}/{5}'.format(
                    github_username,
                    repo_name,
                    artifact_id,
                    id_,
                    file_id,
                    file_name)
                attach_links += '* {0}\n\n\t![{0}]({1})\n\n'.format(file_name, uploaded_link)

        c_body = "This comment created by **{0}** | {1}\n\n------\n\n{2}{3}".format(author, print_time, body,
                                                                                    attach_links)

        result.append({
            "created_at": github_time,
            "body": c_body
        })

    return result


def issue_migration(**kwargs):
    click.echo('이슈 마이그레이션 중...')

    # 기본 변수 정의
    project = kwargs.get('project')
    gh = kwargs.get('github_session')
    repo = kwargs.get('github_repository')
    github_api_url = gh._github_url

    with open(BASIC_TOKEN_FILE_NAME) as f:
        token = f.read()

    header = {
        'Accept': "application/vnd.github.golden-comet-preview",
        'authorization': "token " + token,
        'content-type': "application/json",
    }

    project_name = str(project)
    github_username = gh.user().login

    import_request_url = '{0}/repos/{1}/{2}/import/issues'.format(github_api_url,
                                                                  github_username,
                                                                  repo.name)

    issue_urls = project.urls.copy()
    del issue_urls['download']

    github_parse_url = urlparse(github_api_url)
    github_url = 'github.com' if github_parse_url.netloc == 'api.github.com' \
        else github_parse_url.netloc

    # 마이그레이션 마이그레이션
    milestone_migration(project, gh, repo.name, token)

    # 이슈 마이그레이션
    for board_type, url in issue_urls.items():
        issue_board_r = requests.request("GET", url)
        issue_board_xml = making_soup(issue_board_r.content, 'xml')
        tag_name = 'artifact_id'
        artifacts = issue_board_xml.findAll(tag_name)

        for id_tag in tqdm(artifacts):
            # 본문 파싱
            artifact_id = id_tag.get_text()
            request_url = '{0}/{1}/{2}.xml'.format(project.project_url, board_type, artifact_id)
            artifact_r = requests.request("GET", request_url)

            if not artifact_r.content:
                log_msg = 'BLANK_XML__Repo: {0}, Id: {1}, Type: {2}'.format(project_name, artifact_id, board_type)
                logging.error(log_msg)
                continue

            parsed = making_soup(artifact_r.content, 'xml')

            author = parsed.author.get_text().replace(' ', '')
            assignee = parsed.assignee.get_text().replace(' ', '')
            title = parsed.title.get_text()
            body = parsed.description.get_text()
            open_date_str = parsed.open_date.get_text()

            date_type = "%Y/%m/%d %H:%M:%S"
            open_date = time.strftime(date_type, time.localtime(int(open_date_str)))

            close_date = parsed.find('close_date').get_text()
            closed = False if close_date == '0' else True

            # 첨부파일 파싱
            attach_download_path = os.path.join(WIKI_DIR_NAME, project_name, 'attachFile')

            attachments = parsed.attachments
            attach_markdown = '\n\n-----\n### Attachments\n'

            attach_links = '' if not attachments else get_attach_links(attachments, attach_download_path,
                                                                       project.api_url, github_username, repo.name,
                                                                       artifact_id, github_url)

            attach_markdown = '' if not attach_links else attach_markdown + attach_links

            assignee_text = 'and assigned to **{0}**'.format(assignee) if assignee is not 'Nobody' else ''
            description = "This {0} created by **{1}** {2} | {3}\n\n------\n\n{4}{5}".format(
                board_type,
                author,
                assignee_text,
                open_date,
                body,
                attach_markdown)

            # 코멘트 파싱
            comment_list = [] if not parsed.comments else get_comments(parsed.comments, project.api_url,
                                                                       attach_download_path, artifact_id,
                                                                       github_username, repo.name)

            issue_json = json.dumps(
                dict(
                    issue=dict(
                        title=title,
                        body=description,
                        closed=closed,
                        labels=[board_type]
                    ),
                    comments=comment_list
                )
            )

            requests.request("POST", import_request_url, data=issue_json, headers=header)

    upload_asset_by_git(github_username, project_name, repo.name, token)
    return True
