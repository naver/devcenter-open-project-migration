# -*- coding: utf-8 -*-
#!/usr/bin/env python
from github3 import authorize,login
from os.path import exists
from os import makedirs
from provider import Provider
from json import dumps
import platform
import random
import sys

if platform.python_version()[0] is '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')

class Github(Provider):
    __access_token_file_name = 'GITHUB_ACCESS_TOKEN'
    _basic_url = 'https://api.github.com'

    def __init__(self, username, password, repo_name):
        Provider.__init__(self,username,password,repo_name)
        self._token = self.make_access_token(username,password)

        if self._token == 'login failed':
            raise Exception('TokenError: make_access_token again')

        self.__session = login(token=self._token)
        self._headers = {
                'Accept': "application/vnd.github.golden-comet-preview+json",
                'authorization': "token " + self._token,
                'content-type': "application/json",
                'cache-control': "no-cache"
        }

    def migration_repo(self,vcs_name,naver_un,naver_pw,naver_pr_name):
        full_vcs_name = ''
        url = ''
        username = ''
        password = ''

        if vcs_name == 'git':
            full_vcs_name = vcs_name
            url = 'https://{0}@dev.naver.com/{1}/{2}.{1}'.format(naver_un,vcs_name,naver_pr_name)
            username,password = naver_un,naver_pw
        else:
            full_vcs_name = 'subversion'
            url = 'https://dev.naver.com/{0}/{1}'.format(vcs_name,naver_pr_name)
            username,password = 'anonsvn','anonsvn'

        request_url = '{0}/repos/{1}/{2}/import'.format(self._basic_url,self._username,self._repo_name)

        import_headers = self._headers
        import_headers['Accept'] = 'application/vnd.github.barred-rock-preview'

        request_data = dumps(
            dict(
                vcs=vcs_name,
                vcs_url=url,
                vcs_username=username,
                vcs_password=password
                )
            )

        r = self.request("PUT",request_url,data=request_data,headers=import_headers)

        try:
            self._import_request_url = r.json()['url']
            self.repo_migration_complete = True if r.json()['status'] is 'complete' else False
        except:
            self._import_request_url = request_url
            self.repo_migration_complete = True

        return self.repo_migration_complete

    def make_access_token(self,username,password):
        if exists(self.__access_token_file_name):
            with open(self.__access_token_file_name,'r') as f:
                return f.read()
        else:
            n = random.choice([i for i in range(1,100)])
            # 랜덤하게 personal access token 을 생성함
            note = 'nopm' + str(n)
            grant = ['repo', 'user', 'delete_repo']

            note_url = 'https://developers.naver.com/main'
            try:
                auth = authorize(username,password,grant,note,note_url)

                with open('GITHUB_ACCESS_TOKEN','w') as f:
                    f.write(auth.token)

                return auth.token
            except:
                return 'login failed'

    def create_repo(self,**kwargs):
        username = self._username
        if kwargs.get('repo_name') is not None:
            self._repo_name = kwargs['repo_name']

        name = self._repo_name
        repo = self.__session.repository(username,name)

        # ./wiki_repos/github_repo/attachFile 이란 폴더를 만든다
        self._attachFilePath = './wiki_repos/{0}/attachFile'.format(name)

        if not exists(self._attachFilePath):
            makedirs(self._attachFilePath)

        if not repo:
            repo = self.__session.create_repo(name)

        self._repo = repo
        return repo

    def delete_repo(self,**kwargs):
        name = ''
        if kwargs.get('repo_name') is not None:
            name = kwargs['repo_name']
        else:
            name = self._repo_name

        repo = self.__session.repository(self._username,name)

        if repo:
            repo.delete()

if __name__ == '__main__':
    pass
