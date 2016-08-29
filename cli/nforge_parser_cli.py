# -*- coding: utf-8 -*-

import click

from migration.nforge import Nforge


@click.command()
@click.option('--project_name', type=str, help='nFORGE project name', prompt=True)
@click.option('--dev_code', help='Is DevCode project', is_flag=True, prompt=True)
def nforge_parser_cli(project_name, dev_code):
    """
    Command line interface for parsing Nforge project.
    """
    project = Nforge(project_name, dev_code)
    project.developers()
    project.code_info()
    project.wiki()
    project.milestones()
    project.boards_xml()

if __name__ == '__main__':
    nforge_parser_cli()
