#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import requests
import codecs
import json
import sys
import unittest
import logging
from enum import Enum, unique
from config import *
import time
import io

from github3 import login
from github3.repos.release import Release

from tqdm import tqdm

if DEBUG:
# Request Warning 출력 안하게
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    logging.basicConfig(filename='logs/' + time.strftime("%Y-%m-%d %H:%M:%S")+'.log',level=logging.DEBUG)
else:
    logging.basicConfig(filename='logs/' + time.strftime("%Y-%m-%d %H:%M:%S")+'.log',level=logging.INFO)

gh = login(token=ACCESS_TOKEN)

@unique
class Parse_type(Enum):
    issue = 0
    forum = 1
    download = 2
    comment = 3

@unique
class Tag_type(Enum):
    _id = 0
    _date = 1
    _body = 2
    _author = 3
    _assignee = 4
    _title = 5


class TestGetTagFunc(unittest.TestCase):
    id_tag_list = ['artifact_id', 'artifact_id', 'release_id','id']
    date_tag_list = ['open_date', 'open_date', 'release_date','pubDate']
    body_tag_list = ['description', 'description','description','description']
    # released_by 는 아이디임
    author_tag_list = ['author', 'author', 'released_by','author']
    assignee_tag_list = ['assignee', 'assignee', None, None]
    title_tag_list = ['title', 'title','name', None]
    tag_lists = [id_tag_list, date_tag_list, body_tag_list,
                 author_tag_list, assignee_tag_list, title_tag_list]

    def test_get_id_tag(self):
        for p_type in Parse_type:
            self.assertEqual(get_tag(p_type, Tag_type._id)
                             , self.id_tag_list[p_type.value])

    def test_get_date_tag(self):
        for p_type in Parse_type:
            self.assertEqual(get_tag(p_type, Tag_type._date)
                             , self.date_tag_list[p_type.value])

    def test_get_body_tag(self):
        for p_type in Parse_type:
            self.assertEqual(get_tag(p_type, Tag_type._body)
                             , self.body_tag_list[p_type.value])

    def test_get_author_tag(self):
        for p_type in Parse_type:
            self.assertEqual(get_tag(p_type, Tag_type._author)
                             , self.author_tag_list[p_type.value])

    def test_get_title_tag(self):
        for p_type in Parse_type:
            self.assertEqual(get_tag(p_type, Tag_type._title)
                             , self.title_tag_list[p_type.value])

    def test_get_comment_tag(self):
        for tag_type in Tag_type:
            self.assertEqual(get_tag(Parse_type.comment, tag_type)
                             , self.tag_lists[tag_type.value]
                             [Parse_type.comment.value])

'''
게시물 태그 파싱했을 때 인덱스
     0 artifact_id
     1 priority
     2 open_date
     3 close_date
     4 title
     5 description
     6 assignee_id
     7 assignee
     8 author_id
     9 author
     10 last_modified_date
     11 view_hit
     12 attachments
     13 comments

     이슈 및 게시판 첨부파일 구조
     <attachments>
       <item>
         <id>64095</id>
         <name>스크린샷 2015-11-03 오후 6.51.56.png</name>
         <link>/projects/d2coding/issue/99897/64095/스크린샷 2015-11-03 오후 6.51.56.png</link>
       </item>
     </attachments>

     댓글 첨부파일 구조
     <item>
         <attachment_id>1</attachment_id>
         <id>63291</id>
         <link>/projects/d2coding/forum/98501/63291/d2c_vs2015.png</link>
     </item>
    릴리즈 첨부파일 구조
   <files>
     <file>
       <id>11300</id>
       <name>D2Coding-Ver1.0-TTC-20150911.zip</name>
       <release_date>1441965194</release_date>
       <download_count>12922</download_count>
       <link>/projects/d2coding/files/11300</link>
   </file>
 '''

def get_tag(parse_type, tag_type):
    id_tag_list = ['artifact_id', 'artifact_id', 'release_id','id']
    date_tag_list = ['open_date', 'open_date', 'release_date','pubDate']
    body_tag_list = ['description', 'description','description','description']
    # released_by 는 아이디임
    author_tag_list = ['author', 'author', 'released_by', 'author']
    assignee_tag_list = ['assignee', 'assignee', None, None]
    title_tag_list = ['title', 'title','name', None]
    #attachments_tag_list = ['attachments', 'attachments', None, 'files']
    #each_file_tag_list = ['item', 'item', 'file', 'item']

    tag_lists = [id_tag_list, date_tag_list, body_tag_list,
                 author_tag_list, assignee_tag_list, title_tag_list]

    return tag_lists[tag_type.value][parse_type.value]

# 요청 보낸 URL 를 출력하는 함수
def print_url(r, *args, **kwargs):
    print("URL: " + r.url)

# Version name 을 어떻게든 얻어보고자 고군분투하는 함수
def get_version(title, project_name):
    temp = str.upper(title).replace(str.upper(project_name),'')
    try:
        result = int(temp)
        if result < 0:
            return abs(result)
    except:
        return temp.replace(' ','')

def create_issue(project_name, parse_type):
    url = "http://staging.dev.naver.com/projects/" + project_name + '/'
    file_name = parse_type + XML_EXTENSION

    _parse_type = Parse_type[parse_type] # enum 클래스에서 string 값을 찾음

    id_tag = get_tag(_parse_type, Tag_type._id)

    r = requests.request("GET", url + file_name, headers=HEADERS['NAVER'],
                         hooks=dict(response=print_url))
    r.encoding = ENCODING

    if XML_OUTPUT:
        with open('xml_output/' + project_name + '_' + file_name, 'w') as f:
            f.write(r.text)

    # XML 파서가 nbsp 를 잘 파싱하지 못할 때가 있음
    parsed_xml = r.text.replace('&nbsp;',' ')

    parser = ET.XMLParser(encoding=ENCODING)
    main_root = ET.fromstring(parsed_xml, parser=parser)

    for article in tqdm(main_root):
        assert article.find(id_tag) is not None,"Wrong Parse_type type: %r" % parse_type

        article_id = article.find(id_tag).text

        article_url =  url + _parse_type.name + '/' + article_id + XML_EXTENSION
        r = requests.request("GET", article_url, headers=HEADERS['NAVER'],
                             hooks=dict(response=print_url))
        r.encoding = ENCODING

        """
        API가 XML 을 못 받아오는 버그로 추정하고 있음
        https://oss.navercorp.com/communication-service/open-project-migration/issues/2#issuecomment-538527
        """
        if len(r.text) == 0:
            logging.error("XML IS BLANK!!")
            continue

        # XML 파서가 nbsp 를 잘 파싱하지 못할 때가 있음
        parsed_xml = r.text.replace('&nbsp;',' ')

        if XML_OUTPUT:
            with open('xml_output/' + project_name + '_' + article_id
                      + '_' + file_name, 'w') as f:
                f.write(parsed_xml)
        try:
            article_root = ET.fromstring(parsed_xml)
        except ET.ParseError as e:
            logging.error(e)
            logging.error(parsed_xml)

        # 댓글의 comment 배열을 만드는 과정
        comments = article_root.find('comments')
        comments_list = list()

        if comments is not None:
            comment_root = article_root.find('comments')

            for comment in comment_root.findall('item'):
                date_tag = comment.find(get_tag(Parse_type.comment,
                                                Tag_type._date))
                body_tag =  comment.find(get_tag(Parse_type.comment,
                                                 Tag_type._body))
                author_tag = comment.find(get_tag(Parse_type.comment,
                                                  Tag_type._author))

                if date_tag is None or body_tag is None or author_tag is None:
                    continue

                comments_list.append(
                    {
                        'date' : date_tag.text,
                        'desc' : body_tag.text,
                        'author' : author_tag.text
                    }
                )
        else:
            logging.info(article_id + " article doesn't have comments")

        if len(comments_list) > 0 and DEBUG:
            logging.debug(article_id , comments_list)

        author = article_root.find(get_tag(_parse_type, Tag_type._author)).text

        assignee_tag = get_tag(_parse_type, Tag_type._assignee)
        assignee = article_root.find(assignee_tag).text if assignee_tag is not None else 'Nobody'

        # 이름 중복 제거
        author = author.replace(' ','')
        assignee = assignee.replace(' ','')

        title = article_root.find(get_tag(_parse_type, Tag_type._title)).text

        """
        Download 의 released_by 태그는 아이디를 알려주는데
        API 로 유저 이름을 얻는 것이 불가능함
        """

        body = article_root.find(get_tag(_parse_type, Tag_type._body)).text
        open_date_int = article_root.find(get_tag(_parse_type, Tag_type._date)).text
        date_type = "%Y/%m/%d %H:%M:%S"
        open_date = time.strftime(date_type, time.localtime(int(open_date_int)))

        if not _parse_type is Parse_type.download:
            if _parse_type is Parse_type.issue:
                description = "This issue created by **{0}** and assigned to **{1}** | {2}\n\n------\n{3}".format(author,assignee,open_date,body)
            elif _parse_type is Parse_type.forum:
                description = "This forum created by **{0}** | {1}\n\n------\n{2}".format(author,open_date,body)
        else:
            description = body

        closed = 'download'

        if not _parse_type is Parse_type.download:
            close_date = article_root.find('close_date').text
            closed = False if close_date is '0' else True

        if _parse_type is Parse_type.download:
            github_request_url = GITHUB_URL + 'releases'
            version = str(get_version(title, project_name))

            github_request_data = json.dumps({
                "tag_name": version,
                "target_commitish" : "master",
                "name" : title,
                "body" : description,
                "prerelease" : False,
                "draft" : False
            })

            # logging
            logging.info('id:{0}, tag_name:{1}, title:{2}, \nbody:\n{3}'
                         .format(article_id,version,title,description))
        else:
            github_request_url = GITHUB_URL + 'import/issues'
            github_request_data = json.dumps({"issue" : { "title" : title,
                                                 "body" : description,
                                                 "closed" : closed,
                                                 "labels" : [
                                                    _parse_type.name
                                                 ]
                                                },
                                     # 댓글 list 를 json 화 한다
                                     "comments" : [
                                        {
                                            "created_at" :
                                            time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                            time.localtime(int(comment['date']))),
                                            "body" : 'This comment created by **{0}** | {1}\n\n------\n{2}'.format
                                            (
                                                comment['author'],
                                                time.strftime(date_type,time.localtime(int(comment['date']))),
                                                comment['desc'])
                                        }
                                     for comment in comments_list]})

            # logging
            logging.info('id:{0}, title:{1}, closed:{2}\nbody:\n{3}\ncomments:{4}'
                         .format(article_id,title,closed,description,comments_list))

        # Requsting for MIGRATION
        migration_request = requests.request("POST",github_request_url,
                             data=github_request_data,
                             headers=HEADERS['GITHUB']
                             )


        logging.info('RESULT OF ARTICLE MIGRATION:\n{0}'.format(migration_request.text))

        # 파일 업로드 부분
        if _parse_type is Parse_type.download:
            for item in article_root.find('files'):
                file_id = item.find('id').text
                file_name = item.find('name').text
                file_down_url = \
                'http://staging.dev.naver.com/frs/download.php/{0}/{1}'\
                .format(
                    file_id,file_name
                )
                # 파일을 다운로드 함
                release_file = requests.request("GET",
                                                file_down_url,
                                                stream=True
                                                )

                with open(file_name,'wb') as f:
                    f.write(release_file.content)

                logging.info('RESULT OF RELEASE FILE DOWNLOADING:\n{0}'.format(release_file.raw.read(10)))

                headers = {
                    'content-type': "application/zip",
                    'authorization': "token eddd4749028de2cb5617a864c5a65669df29d6be",
                    'cache-control': "no-cache",
                }

                release = gh.repository('maxtortime','open-project-migration-test').release(id=migration_request.json()['id'])

                release.upload_asset('application/zip',file_name,release_file.content)
                logging.info('RESULT OF UPLOADING:\n{0}'.format(release.__dict__))


        logging.info('RESULT OF MIGRATION:\n{0}'.format(r.text))

if __name__ == '__main__':
    if TEST:
        unittest.main()
    else:
        assert len(sys.argv) >= 3
        create_issue(sys.argv[1], sys.argv[2])
