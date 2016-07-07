#!/usr/bin/env python3
from bs4 import BeautifulSoup
from requests import request
from provider import Provider
from overrides import overrides
from tqdm import tqdm
from os.path import exists
from os import makedirs
import xml.etree.ElementTree as ET
import logging, traceback, sys
import time
import json
import re
import requests


# Request Warning 출력 안하게
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

making_html_soup = lambda content: BeautifulSoup(content,'lxml')
making_xml_soup = lambda content: BeautifulSoup(content,'xml')

class Naver(Provider):
    __basic_url = 'http://staging.dev.naver.com/projects'

    def __init__(self,username,password,repo_name):
        super().__init__(username,password,repo_name)

        self.__basic_url = '{0}/{1}'.format(self.__basic_url,self._repo_name)
        self._urls = self.create_url()

    @overrides
    def parsing(self, github_session):
        for board_type,urls in self._urls.items():
            for url in urls:
                r = self.request("GET",url)
                artifacts = making_xml_soup(r.content)

                try:
                    self.parsing_element(artifacts,board_type,github_session)
                except Exception as e:
                    traceback.print_exc(file=sys.stdout)

    def parsing_element(self,artifacts,board_type,gh):
        tag_name = 'artifact_id' if board_type is not 'download' else 'release_id'

        artifact_list = artifacts.find_all(tag_name)
        print(board_type)

        for id_tag in tqdm(artifact_list):
            artifact_id = id_tag.get_text()
            request_url = '{0}/{1}/{2}.xml'.format(self.__basic_url,
                                                   board_type,
                                                   artifact_id)
            r_artifact = self.request("GET",request_url)

            if len(r_artifact.content) is 0:
                print(board_type,artifact_id,"BLANK XML")
                continue

            parsed_artifact = making_xml_soup(r_artifact.content)
            self._json_data, release_files = self.get_json(artifact_id,parsed_artifact,
                                            board_type,gh)

            github_request_url = '{0}/repos/{1}/{2}/'.format(gh._basic_url,
                                                            gh._username,
                                                            gh._repo_name)
            if release_files is not None:
                github_request_url+='releases'
            else:
                github_request_url+='import/issues'

            import_headers = gh._headers
            import_headers['Accept'] = 'application/vnd.github.golden-comet-preview'


            migration_request = request("POST",github_request_url,
                                    data=self._json_data,
                                    headers=import_headers
                                    )

            try:
                if release_files:
                    release_id = migration_request.json()['id']

                    for fname, release_file in release_files.items():
                        d = release_file.headers['content-disposition']

                        release = gh._repo.release(id=release_id)
                        release.upload_asset('application/zip',fname,release_file.content)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)

    @overrides
    def create_url(self):
        urls = dict()

        for parse_type in ['issue','forum','download']:
            urls[parse_type] = list()

            if parse_type != 'download':
                # 게시판 및 이슈 목록
                url = '{0}/{1}'.format(self.__basic_url,parse_type)
                r = request("GET",url)
                soup = making_html_soup(r.content)

                cond_class = 'menu_{0} on selected'.format(parse_type)
                class_list = soup.find(class_=cond_class)

                if class_list is not None:
                    for a in class_list.find_all('a'):
                        name = a['href'].split('/projects/'+self._repo_name + '/')[1]
                        urls[parse_type].append('{0}/{1}.xml'.format(self.__basic_url,name))

                    urls[parse_type] = list(set(urls[parse_type]))
                else:
                    urls[parse_type].append('{0}/{1}.xml'.format(self.__basic_url,parse_type))

            elif parse_type is 'download':
                urls[parse_type].append('{0}/{1}.xml'.format(self.__basic_url,parse_type))

        return urls

    # Version name 을 어떻게든 얻어보고자 고군분투하는 함수
    def get_version(self,title):
        temp = str.upper(title).replace(str.upper(self._repo_name),'')
        try:
            result = int(temp)
            if result < 0:
                return abs(result)
        except:
            return temp.replace(' ','')

    def get_json(self,artifact_id,parsed_xml,board_type,gh):
        parsed = parsed_xml
        id_ = artifact_id
        type_ = board_type
        author = ''
        assignee = ''
        title = ''
        description = ''
        result = ''

        if type_ is not 'download':
            author = parsed.author.get_text().replace(' ','')
            assignee = parsed.assignee.get_text().replace(' ','')

        title = parsed.title.get_text() if type_ is not 'download' \
                                        else parsed.find('name').get_text()

        body = parsed.description.get_text()
        open_date_str = parsed.open_date.get_text() if type_ is not 'download' \
                                        else parsed.release_date.get_text()


        date_type = "%Y/%m/%d %H:%M:%S"
        open_date = time.strftime(date_type,
                                 time.localtime(int(open_date_str)))

        closed = 'download'

        if not board_type is 'download':
            close_date = parsed.find('close_date').get_text()
            closed = False if close_date == '0' else True

            attachments = parsed.attachments
            body_uploaded_link = ''
            attach_links = ''

            if attachments:
                attach_links = '\n\n-----\n### Attachments\n'

                for item in attachments:
                    body_file_link = item.find('link').get_text()
                    body_file_name = item.find('name').get_text()
                    body_file_id = item.find('id').get_text()

                    down_url = "http://staging.dev.naver.com{0}".format(body_file_link)
                    status_code = self.file_download(
                        down_url,
                        body_file_name,
                        id_,
                        body_file_id,gh
                        )

                    if status_code is 200:
                        status = 'GOOD'
                    elif status_code is 304:
                        status = 'EXISTS'
                    else:
                        status = 'FAILED'

                    body_uploaded_link = 'https://github.com/{0}/{1}/wiki/attachFile/{2}/{3}/{4}'.format(gh._username,
                                                  gh._repo_name,
                                                  id_,
                                                  body_file_id,
                                                  body_file_name)


                    attach_links+='* {0}\n\n\t![{0}]({1})\n\n'.format(body_file_name,body_uploaded_link)
                    #print("{0} 's downloading is {1}".format(body_file_name, status))

            if board_type is 'issue':
                description = "This issue created by **{0}** and assigned to **{1}** | {2}\n\n------\n\n{3}{4}".format(author,
                                                     assignee,
                                                     open_date,
                                                     body,
                                                     attach_links)
            elif board_type is 'forum':
                description = "This forum created by **{0}** | {1}\n\n------\n\n{2}{3}".format(author,open_date,body,attach_links)

            comments = parsed.comments
            processed_comment_list = []

            if comments:
                comment_list = comments.find_all('item')
                comment_attach_links = ''

                for comment in comment_list:
                    comment_attachments = comment.attachments

                    if comment.find('pubDate') is None \
                        or comment.find('description') is None \
                        or comment.find('author') is None \
                        or comment.find('id') is None:
                            continue

                    comment_id = comment.find('id').get_text()
                    comment_body = comment.find('description').get_text()
                    comment_author = comment.find('author').get_text()
                    comment_date = comment.find('pubDate').get_text()

                    print_date_type = "%Y/%m/%d %H:%M:%S"
                    comment_time_type = "%Y-%m-%dT%H:%M:%SZ"

                    print_comment_time = time.strftime(print_date_type,
                                         time.localtime(int(comment_date)))
                    comment_time = time.strftime(comment_time_type,
                                         time.localtime(int(comment_date)))

                    if comment_attachments:
                        comment_attach_links = '\n\n-----\n### Attachments\n'
                        comment_items = comment_attachments.find_all('item')

                        for item in comment_items:
                            comment_file_id = item.find('id').get_text()
                            file_link = item.find('link').get_text()
                            file_name = file_link.split('/')[-1]
                            down_url = "http://staging.dev.naver.com{0}".format(file_link)

                            status_code = self.file_download(down_url,
                                                             file_name,
                                                             id_,
                                                             comment_file_id,gh,
                                                             comment_id=comment_id)
                            if status_code is 200:
                                status = 'GOOD'
                            elif status_code is 304:
                                status = 'EXISTS'
                            else:
                                status = 'FAILED'

                            comment_uploaded_link = 'https://github.com/{0}/{1}/wiki/attachFile/{2}/{3}/{4}/{5}'.format(gh._username,
                                                          gh._repo_name,
                                                          id_,
                                                          comment_id,
                                                          comment_file_id,
                                                          file_name)
                            comment_attach_links+='* {0}\n\n\t![{0}]({1})\n\n'.format(file_name,comment_uploaded_link)
                            #print("{0} 's downloading is {1}".format(file_name, status))

                    c_body = "This comment created by **{0}** | {1}\n\n------\n\n{2}{3}".format(
                                comment_author,print_comment_time,comment_body,comment_attach_links
                                )

                    processed_comment_list.append({
                        "created_at" : comment_time,
                        "body" : c_body
                    })

            result = json.dumps(
                    {
                        "issue" :
                        {
                            "title" : title,
                            "body" : description,
                            "closed" : closed,
                            "labels" :
                            [
                                board_type
                            ]
                            },
                        # 댓글 list 를 json 화 한다
                        "comments" : processed_comment_list
                        })
            return result, None
        else:
            description = body
            version = str(self.get_version(title))
            release_files = dict()

            for item in parsed.find_all('file'):
                release_file_id = item.find('id').get_text()
                release_file_name = item.find('name').get_text()
                release_file_down_url = \
                        'http://staging.dev.naver.com/frs/download.php/{0}/{1}'\
                        .format(
                                release_file_id,release_file_name
                                )

                # 파일을 다운로드 함 release_file
                release_file = request("GET",release_file_down_url,stream=True)
                release_files[release_file_name] = release_file

            result = json.dumps({
                "tag_name": version,
                "target_commitish" : "master",
                "name" : title,
                "body" : description,
                "prerelease" : False,
                "draft" : False
                })

            return result, release_files

    def file_download(self,url,file_name,artifact_id,file_id,gh,**kwargs):
        comment_id = kwargs.get('comment_id')
        attachFilePath = gh._attachFilePath

        if not comment_id:
            down_path = '{0}/{1}/{2}/'.format(attachFilePath,
                                             artifact_id,
                                             file_id)
        else:
            down_path = '{0}/{1}/{2}/{3}/'.format(attachFilePath,
                                                 artifact_id,
                                                 comment_id,
                                                 file_id)

        full_path = down_path + file_name

        if not exists(full_path):
            downloaded = request("GET",url,stream=True)

            if not exists(down_path):
                makedirs(down_path)

            with open(full_path,'wb') as f:
                f.write(downloaded.content)

            return int(downloaded.status_code)
        else:
            return 304


if __name__ == '__main__':
    # Testing create_url
    # 현재 각 게시판 목록 받아오기 가능
    project_name = 'd2coding'
    testNforge = Naver('maxtortime','1234',project_name)
    print(testNforge._urls)
