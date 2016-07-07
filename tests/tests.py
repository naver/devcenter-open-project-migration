#!/usr/bin/env python3
import unittest
from migration import get_tag, Parse_type,Tag_type
from migration import github_login

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

    def test_github_login(self):
        self.assertNotEqual(github_login('maxtortime','KQMvoRiY6RgU'),'login failed')

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

if __name__ == '__main__':
    unittest.main()
