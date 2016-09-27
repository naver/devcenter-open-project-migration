# -*- coding: utf-8 -*-

import click

from migration.nforge import Nforge


@click.command()
@click.option('--project_name', type=str, help='오픈 프로젝트 이름', prompt=True)
@click.option('--private', help='비공개 프로젝트인지', is_flag=True, prompt=True)
@click.option('--dev_code', help='DevCode 프로젝트인지', is_flag=True, prompt=False)
def nforge_parser_cli(project_name, dev_code, private):
    """
    Command line interface for parsing Nforge project.
    """
    project = Nforge(project_name, dev_code, private)
    project.developers()
    project.code_info()
    project.wiki()
    project.milestones()
    project.boards_xml()

if __name__ == '__main__':
    nforge_parser_cli()
