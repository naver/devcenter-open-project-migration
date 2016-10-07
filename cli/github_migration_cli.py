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
import os

import click
from cli import CUR_DIR, DIRS
from migration.github import GitHubMigration, InvalidTokenError


@click.command()
@click.option('--token', help='토큰 직접 입력')
@click.option('--repo_name', prompt=True, help='GitHub 저장소 이름')
@click.option('--enterprise', help='GitHub 엔터프라이즈 저장소 여부', is_flag=False, default=False)
@click.option('--public', help='오픈 프로젝트 공개 저장소 여부', prompt=True, is_flag=True, default=True)
@click.option('--dev_code', help='DevCode 프로젝트인지', is_flag=True, prompt=False, default=False)
def github_migration_cli(dev_code, enterprise, repo_name, token, public):
    """ GitHub migration management """

    # Change current directory to root directory
    os.chdir(CUR_DIR)

    # get path of nforge parsed data
    nforge_type = 'open_project' if not dev_code else 'dev_code'
    nforge_path = os.path.join(os.path.join(DIRS[2], nforge_type))

    try:
        output_dirs = os.listdir(nforge_path)
    except EnvironmentError:
        click.echo('Please parse at lease one %s ...' % nforge_type)
        exit(-1)
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
                exit(-1)

            project_path = os.path.join(nforge_path, project_name)

            try:
                ghm = GitHubMigration(token=token, enterprise=enterprise, repo_name=repo_name,
                                      project_path=project_path)
            except InvalidTokenError as e:
                click.echo(click.style(e.token + ' is a invalid token!!', fg='red'))
                exit(-1)
            else:
                click.echo(ghm.token + click.style(' is valid token', fg='blue'))

                if not ghm.issues_migration():
                    click.echo('Issue and board migration has failed')

                # Only open project and GitHub repo do repo and downloads migration.
                if not (dev_code or enterprise or not public):
                    if not ghm.repo_migration():
                        click.echo('Source code repository migration has failed')

                # Private project only executes download migration after import repo manually!!
                if not enterprise:
                    if not ghm.downloads_migration():
                        click.echo('Download migration has failed.')

if __name__ == '__main__':
    github_migration_cli()
