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
        npa=cli.nforge_parser:nforge_parser
        ght=cli.github_token:github_token
        ghm=cli.github_migration:github_migration
    ''',
)
