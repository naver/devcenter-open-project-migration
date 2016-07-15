# -*- coding: utf-8 -*-
"""
    tests.github_login
    ~~~~~~~~~~~~~~~~~~~~~
    Tests for github login
    It needs help..
"""

import migration
import unittest

with open('credentials') as f:
    password = f.read()

class TestGitHubLogin(unittest.TestCase):
    def test_vaild_account(self):
        pass

if __main__ == '__name__':
    unittest.main()
