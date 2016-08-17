# -*- coding: utf-8 -*-
import os
import webbrowser

import click
from cli import CUR_DIR, PARSING_OUTPUT_DIR
from cli.github_token_cli import get_file_path, read_token_from_file
from migration.github import GitHubSession, GithubMigration


@click.command()
@click.option('--repo_name', prompt=True, help='GitHub repository name')
@click.option('--enterprise', help='Is it Github enterprise repository?', is_flag=True, default=False)
@click.option('--open_project', help='Is DevCode project', is_flag=True, prompt=True)
def github_migration_cli(open_project, enterprise, repo_name):
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

    project_name = ''

    while not project_name:
        idx = click.prompt(menu, type=int)

        try:
            project_name = output_dirs[idx]
        except IndexError:
            click.echo('%d is not valid number' % idx)

    project_path = os.path.join(nforge_path, project_name)
    valid_token = read_token_from_file(get_file_path('token', enterprise), enterprise)

    gh = GitHubSession(valid_token, enterprise, repo_name, project_path)

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
