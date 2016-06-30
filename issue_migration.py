#!/usr/bin/python3
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

logging.basicConfig(filename='logs/' + time.strftime("%Y-%m-%d %H:%M:%S")+'.log',level=logging.INFO)

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
    title_tag_list = ['title', 'title','title', None]
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
 '''

def get_tag(parse_type, tag_type):
    id_tag_list = ['artifact_id', 'artifact_id', 'release_id','id']
    date_tag_list = ['open_date', 'open_date', 'release_date','pubDate']
    body_tag_list = ['description', 'description','description','description']
    # released_by 는 아이디임
    author_tag_list = ['author', 'author', 'released_by', 'author']
    assignee_tag_list = ['assignee', 'assignee', None, None]
    title_tag_list = ['title', 'title','name', None]

    tag_lists = [id_tag_list, date_tag_list, body_tag_list,
                 author_tag_list, assignee_tag_list, title_tag_list]

    return tag_lists[tag_type.value][parse_type.value]

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
    root = ET.fromstring(parsed_xml, parser=parser)

    for article in root:
        assert article.find(id_tag) is not None,"Wrong Parse_type type: %r" % parse_type

        article_id = article.find(id_tag).text

        article_url =  url + _parse_type.name + '/' + article_id + XML_EXTENSION
        r = requests.request("GET", article_url, headers=HEADERS['NAVER'],
                             hooks=dict(response=print_url))
        r.encoding = ENCODING

        # API가 XML 을 못 받아오는 버그로 추정하고 있음
        # https://oss.navercorp.com/communication-service/open-project-migration/issues/2#issuecomment-538527
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
            print(e)
            print(parsed_xml)

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
            print(article_id , comments_list)

        author = article_root.find(get_tag(_parse_type, Tag_type._author)).text

        assignee_tag = get_tag(_parse_type, Tag_type._assignee)
        assignee = article_root.find(assignee_tag).text if assignee_tag is not None else 'Nobody'

        # 이름 중복 제거
        author = author.replace(' ','')
        assignee = assignee.replace(' ','')

        '''
        Assignee 을 지정하려면 github repo 에 그 유저가 collaborator로 등록되어
        있어야 하는데 현재 nFORGE API 상 repo의 멤버들을 얻어올 수 있는 수단이
        없으므로 title 에 두 값을 붙여본다.
        '''

        assignee_str = "->" + assignee if _parse_type.name == 'issue' \
                                        and assignee != 'Nobody' \
                                        else ''
        seperator = ''
        if _parse_type is not Parse_type.download:
            seperator = '[{0}]'.format(str.upper(_parse_type.name))

        title = article_root.find(get_tag(_parse_type, Tag_type._title)).text
        author_assignee = "[" + author + assignee_str + "] "

        """
        Download 의 released_by 태그는 아이디를 알려주는데
        API 로 유저 이름을 얻는 것이 불가능함
        """

        if _parse_type is not Parse_type.download:
            issue_title = seperator + author_assignee + title
        else:
            issue_title = title

        description = article_root.find(get_tag(_parse_type, Tag_type._body)).text

        if not _parse_type is Parse_type.download:
            close_date = article_root.find('close_date').text
            closed = False if close_date is '0' else True

        # logging
        logging.info('id:{0}, title:{1}, closed:{2}\nbody:\n{3}\ncomments:{4}'
                     .format(article_id,issue_title,closed
                             ,description,comments_list))

        issue_json = json.dumps({"issue" : { "title" : issue_title,
                                             "body" : description,
                                             "closed" : closed
                                            },
                                 # 댓글 list 를 json 화 한다
                                 "comments" : [
                                    {
                                        "created_at" :
                                        time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                        time.localtime(int(comment['date']))),
                                        "body" : comment['author'] + '\n' \
                                        + comment['desc']
                                    }
                                 for comment in comments_list]})


        r = requests.request("POST", GITHUB_URL, data=issue_json,
                             headers=HEADERS['GITHUB'],
                             hooks=dict(response=print_url()))

        logging.info('RESULT OF MIGRATION: {0}'.format(r.text))

def print_url(r, *args, **kwargs):
    print(r.url)

if __name__ == '__main__':
    if TEST:
        unittest.main()
    else:
        assert len(sys.argv) >= 3
        create_issue(sys.argv[1], sys.argv[2])
