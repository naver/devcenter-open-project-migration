# -*- coding: utf-8 -*-
import json
import os
import webbrowser

import click
from cli import CUR_DIR, PARSING_OUTPUT_DIR
from migration.github import GitHubSession, GithubMigration


@click.command()
@click.option('--open_project', help='Is DevCode project', is_flag=True, prompt=True)
def github_migration_cli(open_project):
    """ GitHub Repository management """

    # Change current directory to root directory
    os.chdir(CUR_DIR)

    is_open_project = open_project
    nforge_type = 'open_project' if is_open_project else 'dev_code'
    output_dirs = ''
    nforge_path = os.path.join(os.path.join(PARSING_OUTPUT_DIR, nforge_type))

    try:
        output_dirs = os.listdir(nforge_path)
    except EnvironmentError:
        click.echo('Please parse at lease one %s project...' % nforge_type)
        exit()

    click.echo(click.style('Please input number of project that you want to migrate to GitHub', fg='green'))
    menu = 'Please input number '

    for idx in range(len(output_dirs)):
        menu += '{0}: {1} '.format(str(idx), output_dirs[idx])

    idx = click.prompt(menu, type=int)
    project_name = output_dirs[idx]
    project_path = os.path.join(nforge_path, project_name)

    with open(os.path.join(project_path, 'github_info.json')) as github_info:
        project_info = json.load(github_info)

    token = project_info['token']
    repo_name = project_info['repo_name']
    enterprise = project_info['enterprise']

    gh = GitHubSession(token, enterprise, repo_name, project_path)

    is_wiki = click.prompt('Did you made a wiki?(y/n)', type=bool)

    if not is_wiki:
        wiki_create_page_url = '{2}/{0}/{1}/wiki/_new'.format(gh.username, gh.repo_name, gh.url)

        # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
        if webbrowser.open(wiki_create_page_url):
            click.echo('Please click the ' + click.style('Save Page', fg='green') + ' button for creating wiki page!')
        else:
            click.echo(click.style('We failed for opening web browser', fg='red'))
            click.echo('Please go to ' + click.style(wiki_create_page_url + 'and click save page button', fg='green'))

    gm = GithubMigration(session=gh)

    if not gm.issues_migration():
        click.echo('Issue and board migration has failed')

    # Only open project and GitHub repo do repo and downloads migration.
    if is_open_project and not enterprise:
        if not gm.repo_migration():
            click.echo('Source code repository migration has failed')

        if not gm.downloads_migration():
            click.echo('Download migration has failed.')

if __name__ == '__main__':
    github_migration_cli()
