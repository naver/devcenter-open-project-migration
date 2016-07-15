# Open Project Migration
## 개요
[네이버 오픈 프로젝트](http://dev.naver.com/projects)를 GitHub로 migration 하는 CLI(Comamnd Line Interface) 프로그램입니다. 아래와 같은 기능을 갖추고 있습니다. 

## 기능
1. 게시판, 이슈의 첨부파일들을 포함한 글과 댓글들을 GitHub 이슈로 마이그레이션.
2. 다운로드의 게시물과 파일들을 GitHub 릴리즈로 마이그레이션.
3. Git/SVN 소스코드 저장소 마이그레이션.

## Dependencies
* Python 2.7 이상
* Git 2.7 이상

## 사용법
* 유효한 GitHub, NAVER 계정을 준비해주세요.
* Python과 Git을 설치해주세요.
* 이 프로젝트를 다운로드 받아주세요.
* 터미널에서 pip를 이용해 프로그램에 필요한 python 패키지를 설치해주세요.

  > $ pip install --editable .
* 프로그램을 실행시켜주세요

  > $ migration
  
* 이제 프로그램의 지시에 따라 각종 정보를 입력해주시면 자동으로 migration이 진행됩니다.
  ```sh
  $ pyvenv venv
  $ . venv/bin/activate
  $ pip install --editable .
  $ migration # 프로그램 실행 명령
  # 목적지 GitHub 저장소 이름
  Github repo: open-project-migration-test
  # Migration 할 네이버 프로젝트 이름
  Naver repo: test
  # 진짜 Github 계정명 및 비밀번호
  Github id: foo
  Github pw: 1234
  Repeat for confirmation: 1324
  Error: the two entered values do not match
  Github pw: 1234
  Repeat for confirmation: 1234
  # 진짜 네이버 계정명 및 비밀번호
  Naver id: maxtortime
  Naver pw:
  Repeat for confirmation:
  Vcs: svn
  ```
* 혹은 아래의 도움말을 참고하셔서 직접 터미널에 옵션을 입력하는 것도 가능합니다
```sh
$ migration --help
Usage: migration [OPTIONS]

Options:
  --encoding TEXT     Encoding of files
  --github_repo TEXT  Name of github repo used for migration
  --naver_repo TEXT   Name of naver project to migrate
  --github_id TEXT    Github username
  --github_pw TEXT    Github password
  --naver_id TEXT     NAVER username
  --naver_pw TEXT     NAVER password
  --vcs TEXT          Version control system of open project
  --help              Show this message and exit.
```
* 미리 Github 저장소를 만들어주시고 아래 안내를 통해 위키까지 만들어주시면 더욱 편한 사용이 가능합니다.

## 주의사항
* **프로그램 실행 후 반드시 아래 주소로 들어가셔서 위키의 첫 페이지를 만들어주세요!! https://github.com/{계졍명}/{저장소명}/wiki**
![위키 만들기](https://oss.navercorp.com/communication-service/open-project-migration/wiki/위키만들기.png)
* **자신의 오픈 프로젝트가 사용하고 있는 버전 컨트롤 시스템의 종류를 정확히 입력해주세요. (git or svn) 정확하지 않으면 소스코드 저장소 migration이 진행되지 않습니다.**
* **정확한 계정명을 입력하시지 않으면 프로그램이 동작하지 않습니다**
