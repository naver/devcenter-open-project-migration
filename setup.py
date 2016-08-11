# -*- coding: utf-8 -*-
from migration import __version__
from setuptools import setup

setup(
    name='nForge_migration',
    version=__version__,
    description='Nforge to GitHub migration',
    author='Taehwan Kim',
    author_email='maxtortime@navercorp.com',
    py_modules=['npa', 'ght', 'ghm'],
    install_requires=[
        'Click',
        'BeautifulSoup4',
        'lxml',
        'tqdm',
        'github3.py',
        'requests',
        'requests-toolbelt',
        'grequests'
    ],
    entry_points='''
        [console_scripts]
        npa=cli.nforge_parser_cli:nforge_parser_cli
        ght=cli.github_token_cli:github_token_cli
        ghm=cli.github_migration_cli:github_migration_cli
    ''',
)
