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


@click.command()
@click.option('--project_name', type=str, help='오픈 프로젝트 이름', prompt=True)
@click.option('--public', help='오픈 프로젝트 공개 저장소 여부', is_flag=True, prompt=True, default=True)
@click.option('--dev_code', help='DevCode 프로젝트인지', is_flag=True, prompt=False)
def nforge_parser_cli(project_name, dev_code, public):
    """
    Command line interface for parsing Nforge project.
    """
    project = Nforge(project_name, dev_code, public)
    project.developers()
    project.code_info()
    project.wiki()
    project.milestones()
    project.boards_xml()

if __name__ == '__main__':
    nforge_parser_cli()
