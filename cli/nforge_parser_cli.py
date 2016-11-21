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

import click

from migration.nforge import Nforge
from migration import __version__


@click.command()
@click.option('--name', type=str, help='오픈 프로젝트 이름', prompt=True)
@click.option('--private', help='오픈 프로젝트 비공개 저장소 여부',
              is_flag=True, default=False)
@click.option('--dev_code', help='DevCode 프로젝트인지', is_flag=True,
              default=False)
@click.version_option(version=__version__)
def nforge_parser_cli(name, dev_code, private):
    """
    Command line interface for parsing Nforge project.
    """
    project_name = name
    project = Nforge(project_name, dev_code, private)
    project.developers()

    if not dev_code:
        project.code_info()
    project.wiki()
    project.milestones()
    project.boards_xml()

if __name__ == '__main__':
    nforge_parser_cli()
