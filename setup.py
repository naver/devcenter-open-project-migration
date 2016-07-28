# -*- coding: utf-8 -*-
from migration import __version__
from setuptools import setup

setup(
    name='migration',
    version=__version__,
    description='Naver open project migration',
    author='Taehwan Kim',
    author_email='maxtortime@navercorp.com',
    py_modules=['migration'],
    install_requires=[
        'Click',
        'BeautifulSoup4',
        'lxml',
        'tqdm',
        'github3.py',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        parser=migration.parser_cli:parser_cli
        token=migration.token_manage:token_manage
        repo=migration.repo_manage:repo_manage
    ''',
)
