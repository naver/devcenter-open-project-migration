# -*- coding: utf-8 -*-
class InvalidProjectError(Exception):
    def __init__(self, pr_name):
        self.pr_name = pr_name

    def __str__(self):
        not_found_project_msg = '{0} does not exist.'.format(self.pr_name)
        return not_found_project_msg


class InvalidCookieError(Exception):
    def __init__(self, cookies):
        self.cookies = cookies

    def __str__(self):
        msg = 'Please make valid cookies to data/COOKIES'.format(self.cookies)
        return msg


class NoSrcError(Exception):
    def __str__(self):
        return 'Please check is it private project'
