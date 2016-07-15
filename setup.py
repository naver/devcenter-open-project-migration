# -*- coding: utf-8 -*-
from setuptools import setup
from migration import __version__

with open('README.rst') as f:
    readme = f.read()

setup(
    name='migration',
    version=__version__
    description='Naver open project migration',
    long_description=readme,
    author='Taehwan Kim',
    author_email='maxtortime@navercorp.com',
    py_modules=['migration'],
    install_requires=[
        'Click',
        'BeautifulSoup4',
        'lxml',
        'overrides',
        'tqdm',
        'github3.py',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        migration=migration.cli:migration
    ''',
)
