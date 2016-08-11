# -*- coding: utf-8 -*-
import os

import click
from cli import DATA_DIR
from cli.github_token_cli import read_token_from_file, get_file_path
from migration.github import GitHubSession
from migration.nforge import Nforge
from migration.nforge_parser import NforgeParser


@click.command()
@click.option('--project_name', type=str, help='nFORGE project name', prompt=True)
@click.option('--dev_code', help='Is DevCode project', is_flag=True, prompt=True)
@click.option('--repo_name', prompt=True, help='GitHub repository name')
@click.option('--enterprise', help='Is it Github enterprise repository?', is_flag=True, default=False)
def nforge_parser_cli(project_name, dev_code, repo_name, enterprise):
    """
    Command line interface for parsing Nforge project.
    """
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    project = Nforge(project_name, dev_code)
    project.developers()
    project.code_info()
    project.wiki()
    project.milestones()
    project.boards_xml()

    token_file_path = get_file_path('token', enterprise)
    token = read_token_from_file(token_file_path, enterprise)

    gh = GitHubSession(token, enterprise, repo_name, project.path)
    gh.make_github_info()
    parser = NforgeParser(gh)

    parser.make_issue_json()
    parser.make_download_json()

if __name__ == '__main__':
    nforge_parser_cli()
