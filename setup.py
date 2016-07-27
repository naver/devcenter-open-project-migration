# -*- coding: utf-8 -*-
from setuptools import setup
from migration import __version__

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
        tm=cli.token_manage:token_manage
        repom=cli.token_manage:repo_manage
    ''',
)
