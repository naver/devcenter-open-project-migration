# Open Project Migration
## 개요
[네이버 오픈 프로젝트](http://dev.naver.com/projects)를 GitHub로 migration 하는 CLI(Comamnd Line Interface) 프로그램입니다. 아래와 같은 기능을 갖추고 있습니다.

## 기능
1. 게시판, 이슈의 첨부파일들을 포함한 글과 댓글들을 GitHub 이슈로 마이그레이션.
2. 다운로드의 게시물과 파일들을 GitHub 릴리즈로 마이그레이션.
3. Git/SVN 소스코드 저장소 마이그레이션.

## Dependencies
* Python 2.7 이상
  * [Windows 설치법](https://wikidocs.net/8)
  * Unix 계열: 기본적으로 Python이 제공됩니다.

    > $ python --version

    위 명령어 실행 시 2.7버전 이상이 아니신 분은 [이 자료](http://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_Python_2.7_%EC%BB%B4%ED%8C%8C%EC%9D%BC_%EC%84%A4%EC%B9%98)를 참고하셔서 업그레이드 하시는 걸 권장합니다.

* [Git 1.7.10 이상](https://help.github.com/articles/https-cloning-errors/#check-your-git-version)
> 이 버전 미만일 경우 GitHub에 push가 불가능해서 첨부파일 마이그레이션이 불가능합니다.

  * Windows 에서는 Git 공식 홈페이에서 적절한 Git 설치 파일을 [다운로드](https://git-scm.com/download/win) 받아 설치하시면 잘 동작합니다.
  * 대부분 유닉스 계열에서 Git 1.7.10 이상을 지원합니다.

    ```sh
    $ sudo apt-get install git # 데비안 계열
    $ sudo yum install git # 페도라 계열
    $ brew install git # OSX
    ```
  * 간혹 CentOS 6를 이용하시는 분은 기본 yum 저장소에 있는 Git 버전이 낮아 GitHub에 Push가 안 되는 오류가 일어날 수 있습니다. [이 자료](http://maxtortime.github.io/the-post-6832/)를 참고하셔서 Git 버전을 업그레이드 해주세요.

## 사용법
* 유효한 GitHub, NAVER 계정을 준비해주시고 마이그레이션할 오픈 프로젝트의 이름을 확인해주세요.
* 프로그램이 자동으로 GitHub 저장소를 만들어주지만 미리 만들어주시고 이름을 확인해놓으시면 편하게 이용하실 수 있습니다.
* 만드신 GitHub 저장소로 가셔서 위키의 첫 페이지를 만들어주세요. (위키가 없으면 첨부파일 업로드가 불가능합니다)

  ![위키 만들기](https://oss.navercorp.com/communication-service/open-project-migration/wiki/위키만들기.png)
* 이 프로젝트를 다운로드 받은 후 압축을 풀어주세요.
* 터미널에서 pip를 이용해 프로그램에 필요한 python 패키지를 설치해주세요.

  > $ pip install --editable .

* **중요!!** 현재 XML 파싱을 위해 [lxml](http://lxml.de/)을 사용하고 있습니다. 윈도우 사용자 분들은 *반드시 [이 링크](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)로 가셔서* 적절한 lxml whl 파일을 다운로드 해주시고 나서 pip로 설치해주시면 되겠습니다.
 > $ pip install {방금 다운로드한 파일 이름}.whl
* 프로그램을 실행시켜주세요

  > $ cli

* 이제 프로그램의 지시에 따라 각종 정보를 입력해주시면 자동으로 migration이 진행됩니다.

  ```sh
  $ pyvenv venv
  $ . venv/bin/activate
  $ pip install --editable .
  $ cli # 프로그램 실행 명령
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
* 혹은 아래의 도움말(cli --help 타이핑 하면 확인 가능)을 참고하셔서 직접 터미널에 옵션을 입력하는 것도 가능합니다.

  ```sh
  $ cli --help
  Usage: cli [OPTIONS]

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
* 마이그레이션이 시작되면 자동으로 웹브라우저가 열리면서 위키 페이지를 만들 수 있는 창이 뜹니다. 맨 아래 Save Page 버튼을 누르셔서 위키 페이지를 만들어주세요. 만들고 난 후 웹브라우저는 종료하셔도 됩니다.

## 주의사항
* **프로그램 실행 전 반드시 아래 주소로 들어가셔서 위키의 첫 페이지를 만들어주세요!!     https://github.com/{계졍명}/{저장소명}/wiki**

  ![위키 만들기](https://oss.navercorp.com/communication-service/open-project-migration/wiki/위키만들기.png)
* **자신의 오픈 프로젝트가 사용하고 있는 버전 컨트롤 시스템의 종류를 정확히 입력해주세요. (git or svn) 정확하지 않으면 소스코드 저장소 migration이 진행되지 않습니다.**
* **정확한 계정명을 입력하시지 않으면 프로그램이 동작하지 않습니다**
* **현재 마이그레이션 도중에 프로그램을 종료하시면 이전에 했던 작업에서 이어서 할 수 있는 기능이 없습니다. 정확한 마이그레이션을 원하신다면 저장소를 삭제 후 다시 시도해주세요.**
