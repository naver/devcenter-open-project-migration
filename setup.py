# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='nforge_migration',
    version='1.0.0',
    description='Migrate nForge project to GitHub',
    author='Taehwan Kim',
    author_email='maxtortime@navercorp.com',
    py_modules=['npa', 'ghm'],
    packages=find_packages(exclude=['tests*']),
    data_files=['Nforge', 'data'],
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
