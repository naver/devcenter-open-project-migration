#!env python
# -*- coding: utf-8 -*-
import unittest

from github_auth import input_credentials
from credentials import GITHUB_ID, GITHUB_PW


class TestGithubAuth(unittest.TestCase):
    """
    GITHUB_ACCESS_TOKEN 파일이 현재 디렉토리에 있는지 검증
    T 토큰을 검증 / F ID/PW 입력

    토큰을 검증
    그 토큰으로 로그인이 되나
    migration 모듈로 넘어감 / F UnvalidTokenError 내며 죽기

    ID/PW 입력
    T 엑세스 토큰 만들기 / F 입력 반복
    """
    def test_input_credentials(self):
        self.assertTrue(input_credentials(GITHUB_ID, GITHUB_PW))


if __name__ == '__main__':
    unittest.main()