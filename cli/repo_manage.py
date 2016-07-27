# -*- coding: utf-8 -*-
import click


@click.command()
@click.option('--repo_name', help='GitHub Repository name', type=str)
@click.option('--enterprise', help='GitHub Enterprise mode', is_flag=True, default=False)
def repo_manage(repo_name, enterprise):
    """ Managing your GitHub repository. """
    pass


if __name__ == '__main__':
    repo_manage()
