# NAVER Open Project migration
## 개요
[네이버 오픈 프로젝트](http://dev.naver.com/projects)를 Github로 migration 하는 모듈입니다. python으로 개발되었고 터미널에서 쉽게 실행할 수 있습니다. 아래와 같은 기능을 지원합니다.

## 기능
1. 게시판, 이슈의 글과 댓글들을 GitHub 이슈로 옮기기. (첨부파일 포함)
2. 다운로드의 게시물과 파일들을 GitHub 릴리즈로 옮기기
3. Git/SVN 소스코드 저장소 옮기기

## 사용법
1. 유효한 GitHub, NAVER 계정을 준비해주세요.
2. python3.5 이상과 (2는 조만간 지원 예정) git을 설치해주세요.
3. 아래의 명령을 실행해주세요.
  ```sh
  $ pyvenv venv
  $ . venv/bin/activate
  $ pip install --editable .
  $ migration
  ```
4. 프로그램에 지시에 따라서 옵션을 입력해주시면 자동으로 migration 이 진행됩니다.
5. *중요!! 위키의 첫 페이지를 만들지 않으시면 첨부파일이 옮겨지지 않습니다!!*
> 프로그램 실행 후 반드시 https://github.com/{계졍명}/{저장소명}/wiki 로 들어가셔서 위키의 첫 페이지를 만들어주세요!!
