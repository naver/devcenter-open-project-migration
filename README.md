# 네이버 개발자센터 오픈 프로젝트 마이그레이션
[네이버 개발자센터의 오픈 프로젝트](http://dev.naver.com/projects)를 GitHub로 마이그레이션하는 CLI(Comamnd Line Interface) 프로그램입니다.

## 마이그레이션 스펙
* 오픈 프로젝트에서 가져온 이슈/게시판/댓글, 첨부파일등은 모두 **nForge/open_project/프로젝트명** 에 저장됩니다.

### 프로젝트 홈/위키
* 프로젝트 홈에 있는 문서 및 작성하신 위키는 Markdown(.md) 파일로 변환되어 GitHub Wiki에 저장됩니다. 원본파일에서 확장자만 바꾼 것이므로 기본적으로 Markdown을 사용하는 GitHub Wiki에서 글을 확인할 때 렌더링이 잘못 되어 보일 수 있습니다.
* 프로젝트 정보 및 로고 마이그레이션은 지원하지 않습니다. 개발자 명단을 옮기는 것은 현재 개발중입니다.

### 마일스톤
* 마일스톤 명단은 GitHub 이슈의 마일스톤으로 옮겨집니다.
* 마일스톤이 어느 이슈에 링크되었는지 여부는 아직 지원하지 않습니다.

### 게시판/이슈
* 모두 GitHub issue로 옮겨집니다. GitHub Label을 통해 이슈/게시판 분류를 확인할 수 있습니다. 해결/닫힘인 이슈들은 closed 이슈, 해결중인 이슈들은 open 이슈로 분류됩니다.
* 아래와 같은 형식으로 이슈/게시판/댓글 이 옮겨집니다.
 ```markdown
 This (issue/comment) created by **(작성자)** and assigned to **(담당자)** | (작성시간)

 ------
 (이슈 본문)
 -----
 ### Attachments
 * (첨부파일명)

 	![(첨부파일명)]((첨부파일링크))
 	...
 ```
* 이슈/게시판의 첨부파일은 GitHub 위키 저장소에 저장됩니다.

### 코드
* 프로젝트의 git/SVN 저장소가 GitHub로 옮겨집니다.
* GitHub는 SVN 방식의 디렉토리 구조를 따르지 않으므로 GitHub에서 저장소 구조가 조금 달라보일 수 있습니다.
* [GitHub에서 SVN 클라이언트 이용하기](https://help.github.com/articles/support-for-subversion-clients/)

### 다운로드
* GitHub의 Release로 옮겨집니다.
* 버전 라벨이 원래 프로젝트와 조금 다를 수 있지만 순서는 일치합니다.

## Dependencies
* Python 2.7 이상
  * [Windows에서 Python 설치법](https://wikidocs.net/8)
  * Unix 계열(Linux, OSX): 기본적으로 Python이 제공됩니다.

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


## 사전 준비 및 프로그램 설치
* [GitHub](https://github.com) 계정이 필요합니다. 회원가입을 해주세요. **[참고](https://help.github.com/articles/signing-up-for-a-new-github-account/)**
* 마이그레이션이 수행될 저장소(Repository)를 만들어주세요. **[참고](https://help.github.com/articles/create-a-repo/)**
* 위에서 만든 저장소의 위키를 만들어주세요. **[참고](https://help.github.com/articles/adding-wiki-pages-via-the-online-interface/)**
* 본 프로젝트를 git clone 혹은 다운로드 해주세요.
* 압축을 풀어주세요.(git clone 하셨을 경우 필요 없음)
* [이곳을 참고하셔서](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) Personal Access Token을 생성하신 후 프로젝트 디렉토리에 **data**라는 디렉토리를 만드시고 **github_ACCESS_TOKEN**이라는 파일에 토큰을 넣어주세요. (파일을 만들지 않으시면 프로그램에서 토큰을 물어보는데 이때 토큰을 입력해주세요)
* **윈도우 사용자 필독!!** 현재 XML 파싱을 위해 [lxml](http://lxml.de/)을 사용하고 있습니다. 윈도우 사용자 분들은 *반드시 [이 링크](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)로 가셔서* 적절한 lxml whl 파일을 다운로드 해주시고 나서 터미널에서 pip로 설치해주시면 됩니다.

 ``` sh
 $ virtualenv venv # python2 및 윈도우 사용자
 $ pyvenv venv # python3 사용자
 $ . venv/bin/activate # *nix 계열
 $ . venv\Scripts\activate # Windows
 $ pip install lxml_파일명 # Windows 사용자만 해당, 아래 참고
 $ pip install --editable .
 ```

* *npa --help* 명령어를 입력하셨을 때 아래 옵션들이 보이시면 잘 설치된 겁니다.

    ```sh
    Usage: npa [OPTIONS]

      Command line interface for parsing Nforge project.

  Options:
    --project_name TEXT  nFORGE project name
    --dev_code           Is DevCode project
    --help               Show this message and exit.
    ```
* 혹시 프로그램 설치에 문제점이 있으시다면 [이슈](https://oss.navercorp.com/communication-service/open-project-migration/issues)를 남겨주세요.

## 마이그레이션 진행
* 터미널에서 *npa* 명령어를 실행합니다. nForge 프로젝트를 파싱해서 파일로 만들어주는 명령어입니다.
*
  ```sh
  $ npa
  Project name: Nforge # 프로젝트 이름 입력
  Dev code [y/N]: n # Devcode의 프로젝트인지 유무
  # 자동으로 파싱이 진행됨
  Now making 4372.xml of CodeReview:   8%|███▎    | 12/144 [00:04<00:45,  2.93it/s]
  ```

* XML, JSON 생성, 파일 다운로드가 자동으로 진행됩니다. 프로젝트의 크기에 따라 오래 걸릴 수 있습니다.
* 동작이 끝나면 *ghm* 명령어를 실행합니다. 파싱된 nForge 프로젝트를 GitHub로 마이그레이션 하는 명령어입니다.

 ``` sh
 $ ghm
 Open project [y/N]: n # 마이그레이션 할 프로젝트가 오픈 프로젝트인지 유무
 아래 목록에서 Migration 할 프로젝트의 번호를 입력하세요
 번호를 입력하세요 0: jindo : 0 # 지금까지 파싱한 프로젝트를 보여줌, 번호를 입력할 것
 위키를 만드셨나요(y/n): n
 # 저장소의 위키를 생성했는지 유무,
 # 위키를 생성하지 않았다면 자동으로 웹브라우저가 실행되며 이때 Create page 버튼을 누르면 된다.
 ```

## 주의 사항
* 빠른 시간 내에 많은 GitHub 마이그레이션을 수행하면 [Abuse Rate Limits](https://developer.github.com/v3/#abuse-rate-limits)가 발생해 일시적으로 GitHub API를 호출할 수 없게 됩니다. 새로운 토큰을 발급하시거나 몇분 후에 다시 시도해주세요.
