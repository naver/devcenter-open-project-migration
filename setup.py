# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='nForge_migration',
    version='0.0.1',
    description='Migrate nForge project to GitHub',
    author='Taehwan Kim',
    author_email='maxtortime@navercorp.com',
    py_modules=['npa', 'ght', 'ghm'],
    packages=[],
    install_requires=[
        'Click',
        'BeautifulSoup4',
        'lxml',
        'tqdm',
        'github3.py',
        'requests',
        'requests-toolbelt',
        'grequests',
        'future'
    ],
    entry_points='''
        [console_scripts]
        npa=cli.nforge_parser_cli:nforge_parser_cli
        ght=cli.github_token_cli:github_token_cli
        ghm=cli.github_migration_cli:github_migration_cli
    ''',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ],
)
