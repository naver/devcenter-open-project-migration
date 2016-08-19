# -*- coding: utf-8 -*-
import os
import webbrowser

import click
from cli import CUR_DIR, PARSING_OUTPUT_DIR
from migration.github import GitHubMigration, InvalidTokenError


@click.command()
@click.option('--token', help='Input token')
@click.option('--repo_name', prompt=True, help='GitHub repository name')
@click.option('--enterprise', help='Is it Github enterprise repository?', is_flag=True, default=False)
@click.option('--open_project', help='Is DevCode project', is_flag=True, prompt=True)
def github_migration_cli(open_project, enterprise, repo_name, token):
    """ GitHub migration management """

    # Change current directory to root directory
    os.chdir(CUR_DIR)

    is_open_project = open_project
    nforge_type = 'open_project' if is_open_project else 'dev_code'
    nforge_path = os.path.join(os.path.join(PARSING_OUTPUT_DIR, nforge_type))

    try:
        output_dirs = os.listdir(nforge_path)
    except EnvironmentError:
        click.echo('Please parse at lease one %s project...' % nforge_type)
        exit()
    else:
        click.echo(click.style('Please input number of project that you want to migrate to GitHub', fg='green'))
        menu = 'Please input number '

        for idx in range(len(output_dirs)):
            menu += '{0}: {1} '.format(str(idx), output_dirs[idx])

        project_name = str()

        while not project_name:
            idx = click.prompt(menu, type=int)

            try:
                project_name = output_dirs[idx]
            except IndexError:
                click.echo('%d is not valid number' % idx)

            project_path = os.path.join(nforge_path, project_name)

            try:
                ghm = GitHubMigration(token=token, enterprise=enterprise, repo_name=repo_name,
                                      project_path=project_path)
            except InvalidTokenError:
                click.echo(click.style(token + ' is a invalid token!!', fg='red'))
                exit()
            else:
                click.echo(ghm.token + click.style(' is valid token', fg='blue'))
                is_wiki = click.prompt('Did you made a wiki?(y/n)', type=bool)

                if not is_wiki:
                    wiki_create_page_url = '{2}/{0}/{1}/wiki/_new'.format(ghm.username, ghm.repo_name, ghm.url)

                    # 위키 페이지를 만들 수 있도록 자동으로 웹 브라우저를 열어줌
                    if webbrowser.open(wiki_create_page_url):
                        click.echo('Please click the ' + click.style('Save Page', fg='green') +
                                   ' button for creating wiki page!')
                    else:
                        click.echo(click.style('We failed for opening web browser', fg='red'))
                        click.echo('Please go to ' + click.style(wiki_create_page_url +
                                                                 'and click save page button', fg='green'))

                if not ghm.issues_migration():
                    click.echo('Issue and board migration has failed')

                # Only open project and GitHub repo do repo and downloads migration.
                if is_open_project and not enterprise:
                    if not ghm.repo_migration():
                        click.echo('Source code repository migration has failed')

                    if not ghm.downloads_migration():
                        click.echo('Download migration has failed.')

if __name__ == '__main__':
    github_migration_cli()
