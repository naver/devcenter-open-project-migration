# -*- coding: utf-8 -*-
from requests import request

class Provider:
    def __init__(self, username, password, repo_name):
        self._username = username
        self.__password = password
        self._repo_name = repo_name

    def create_url(self):
        pass

    def parsing(self):
        pass

    def request(self,method, url, **kwargs):
        headers = kwargs.get('headers') if kwargs.get('headers') else None
        data = kwargs.get('data') if kwargs.get('data') else None

        r = request(method, url, headers=headers, data=data)

        r.encoding = 'utf-8'

        return r
