# NAVER Open Project migration
## 개요
 [네이버 오픈 프로젝트](http://dev.naver.com/projects)를 Github로 migration 하는 모듈입니다.

 1. 게시판 & 이슈의 게시물과 댓글들을 GitHub의 이슈로 migration.
 2. 다운로드를 GitHub releases로 migration.

## 사용법
```sh
# 프로젝트 다운로드 및 python3 설치
$ pip install -r requirements.txt
$ ./config_gen.py
$ ./issue_migration.py {프로젝트 이름} {issue, forum, download}
```
