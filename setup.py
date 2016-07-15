# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='migration',
    version='0.0.1',
    py_modules=['migration'],
    install_requires=[
        'Click',
        'BeautifulSoup4',
        'lxml',
        'overrides',
        'tqdm',
        'github3.py'
    ],
    entry_points='''
        [console_scripts]
        migration=migration:migration
    ''',
)
