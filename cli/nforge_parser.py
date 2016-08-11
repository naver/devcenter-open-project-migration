# -*- coding: utf-8 -*-
import os

import click
from cli import DATA_DIR
from cli.github_token import read_token_from_file, get_file_path
from migration.github import GitHubSession
from migration.nforge import Nforge
from migration.nforge_parser import NforgeParser


@click.command()
@click.option('--project_name', type=str, help='nFORGE 프로젝트 이름', prompt=True)
@click.option('--dev_code', help='DevCode 유무', is_flag=True, prompt=True)
@click.option('--repo_name', prompt=True, help='GitHub 저장소 이름 입력')
@click.option('--enterprise', help='GitHub 엔터프라이즈 여부', is_flag=True, default=False)
def nforge_parser(project_name, dev_code, repo_name, enterprise):
    """
    NForge 프로젝트를 JSON으로 파싱하는 모듈
    """

    # 데이터(쿠키, 토큰) 등이 담기는 디렉토리 생성
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    # 폴더 만들기
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
    nforge_parser()
