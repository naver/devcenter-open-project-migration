# -*- coding: utf-8 -*-
"""
   Copyright 2016 NAVER Corp.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='nforge_migration',
    version='1.1.0.post1',
    description='Migrate nForge project to GitHub',
    author='Taehwan Kim',
    author_email='maxtortime@navercorp.com',
    py_modules=['npa', 'ghm'],
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/naver/devcenter-open-project-migration',
    install_requires=required,
    entry_points='''
        [console_scripts]
        npa=cli.nforge_parser_cli:nforge_parser_cli
        ghm=cli.github_migration_cli:github_migration_cli
    ''',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Text Processing :: Markup :: XML",
        "Environment :: Console",
        "Natural Language :: Korean",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='Apache License, Version 2.0',
    keywords='nForge migration github naver open_project'
)
