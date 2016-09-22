# 네이버 개발자센터 오픈 프로젝트 마이그레이션
[네이버 개발자센터의 오픈 프로젝트](http://dev.naver.com/projects)를 다운로드한 후 GitHub로 마이그레이션하는 CLI(Comamnd Line Interface) 프로그램입니다. 또한 직접 마이그레이션을 수행하는 파이썬 스크립트를 작성하실 수 있습니다.

## 마이그레이션 스펙
### 주의사항
* 비공개 프로젝트의 경우는 오픈 프로젝트 설정에서 각 항목을 공개로 바꿔주시거나 로그인 하신 후 쿠키를 이용해서 마이그레이션 동작이 가능합니다. (아래 안내 참고)
* 빠른 시간 내에 많은 GitHub 마이그레이션을 수행하면 [Abuse Rate Limits](https://developer.github.com/v3/#abuse-rate-limits)가 발생해 일시적으로 GitHub API를 호출할 수 없게 됩니다. 새로운 토큰을 발급하시거나 몇 분 후에 다시 시도해주세요.
* 만일 위키를 만들지 않으시고 마이그레이션을 수행하셨거나 첨부파일이 제대로 보이지 않을 경우에는 `Nforge/open_project/{프로젝트명}/issues/raw` 로 가셔서 `git push -f origin master` 명령어를 실행하셔서 강제로 첨부파일들을 업로드해주세요.

### 프로젝트 홈/위키
* 프로젝트 홈에 있는 문서 및 작성하신 위키는 마크다운(.md) 파일로 변환되어 [GitHub Wiki](https://help.github.com/articles/about-github-wikis/)에 저장됩니다. 원본파일에서 확장자만 바꾼 것이므로 기본적으로 마크다운을 사용하는 GitHub 위키에서 글을 확인할 때 렌더링이 잘못 되어 보일 수 있습니다.
* 프로젝트 정보 및 로고 마이그레이션은 지원하지 않습니다.
* 개발자 명단을 옮기는 것은 현재 개발중입니다.

### 게시판/이슈
* 모두 [GitHub Issue](https://guides.github.com/features/issues/)로 옮겨집니다. 라벨을 통해 이슈/게시판 분류를 확인할 수 있습니다. 해결/닫힘인 이슈들은 `closed` 이슈, 해결중인 이슈들은 `open` 이슈로 분류됩니다.
* 아래와 같은 형식(마크다운)으로 이슈/게시판/댓글 이 옮겨집니다.
 ```markdown
 This {issue OR comment} created by **{작성자}** and assigned to **{담당자}** | {작성시간}

 ------
 {이슈 본문}
 -----
 ### Attachments
 * {첨부파일명}

 	![{첨부파일명}]({첨부파일링크})
 	...
 ```
* 이슈/게시판의 첨부파일은 GitHub 위키 저장소에 저장됩니다.

#### 마일스톤
* 마일스톤 명단은 GitHub 이슈의 마일스톤으로 옮겨집니다.
* 마일스톤이 어느 이슈에 링크되었는지 여부는 아직 지원하지 않습니다.

### 코드
* **비공개 프로젝트 일 경우 직접 옮겨 주셔야 합니다(공개 전환 후 가능함)**
* 프로젝트의 git/SVN 저장소가 GitHub로 옮겨집니다.
* GitHub는 SVN 방식의 디렉토리 구조를 따르지 않으므로 GitHub에서 저장소 구조가 조금 달라보일 수 있습니다.
* [GitHub에서 SVN 클라이언트 이용하기](https://help.github.com/articles/support-for-subversion-clients/)

### 다운로드
* 반드시 소스 코드 저장소 마이그레이션 후 수행하셔야 합니다.
* [GitHub의 Releases](https://help.github.com/articles/about-releases/)로 옮겨집니다.
* 버전 라벨이 원래 프로젝트와 조금 다를 수 있지만 순서는 일치합니다.

## Dependencies
* Python 2.7 이상
  * [Windows에서 Python 설치법](https://wikidocs.net/8)
  * Unix 계열(Linux, OSX): 기본적으로 Python이 제공됩니다.

    > python --version

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

## 프로그램 설치
* 터미널을 켜주세요.
* **윈도우 사용자 필독!!** XML 파싱을 위해 [lxml](http://lxml.de/)을 사용하고 있습니다. 윈도우 사용자 분들은 *반드시 [이 링크](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)로 가셔서* 자신의 플랫폼에 맞는 `whl` 파일을 다운로드 해주시고 나서 아래와 같이 터미널에서 pip로 설치해주시면 됩니다.
> pip install lxml-3.6.4-cp35-cp35m-win32.whl

* Quick & Easy
 > pip install nforge_migration

* For development

  ```
  $ git clone https://oss.navercorp.com/communication-service/open-project-migration.git
  $ cd open-project-migration
  $ pip install -e .
   ```

* `npa --help` 명령어를 입력하셨을 때 아래와 같은 화면이 보이면 설치가 완료된 것 입니다.

  ```sh
  Usage: npa [OPTIONS]

    Command line interface for parsing Nforge project.

  Options:
  --project_name TEXT  nFORGE project name
  --dev_code           Is DevCode project
  --help               Show this message and exit.
  ```

## 마이그레이션 사전 준비
* [GitHub](https://github.com) 계정이 필요합니다. 회원가입을 해주세요. **[참고](https://help.github.com/articles/signing-up-for-a-new-github-account/)**
* 마이그레이션이 수행될 저장소(Repository)를 만들어주세요. **[참고](https://help.github.com/articles/create-a-repo/)**
* 위에서 만든 저장소의 위키를 만들어주세요. **[참고](https://help.github.com/articles/adding-wiki-pages-via-the-online-interface/)**
* [이곳을 참고하셔서](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) `Personal Access Token`을 생성하신 후 프로젝트 디렉토리에 `data`라는 디렉토리를 만드시고 `github_ACCESS_TOKEN` 이라는 파일에 토큰을 넣어주세요. (파일을 만들지 않으시면 프로그램에서 토큰을 물어보는데 이때 토큰을 입력해주세요)
* 비공개 프로젝트 사용자께서는 프로젝트를 공개로 전환해 주시거나 쿠키 파일을 만들어주셔야 합니다.
* 또한 비공개 프로젝트의 경우는 소스코드 저장소를 수동으로 옮겨주셔야 합니다. 그 다음 다운로드 마이그레이션을 수행하셔야 합니다.

### 쿠키 파일 만들기 (비공개 프로젝트)
* [오픈 프로젝트](http://dev.naver.com/projects)에 로그인 해주세요.
* 웹브라우저 주소창에 `javascript:document.cookie` 라고 입력하면 화면에서 쿠키를 확인할 수 있습니다.
* `NID_SES`와 `NID_AUT` 두 쿠키를 복사해주세요.
* `프로젝트 폴더/data` 에 `COOKIES` 라는 파일을 만들어주세요.
* 아래와 같은 형식으로 `COOKIES` 파일을 채워주시고 저장하세요. (순서는 상관없음, 맨마지막 세미콜론은 지울 것)
```
NID_SES={쿠키값}
NID_AUT={쿠키값}
```

## 마이그레이션 진행
### 오픈 프로젝트 다운로드하기
* npa 명령어를 실행하면 아래와 같이 옵션을 입력하는 프롬프트가 나오게 됩니다.

  ```sh
  $ npa
  Project name: nforge
  Private [y/N]: y
  ```
* 비공개 프로젝트라면 `Private` 옵션은 `y` 아니라면 `n`을 입력해주세요.
* Progress bar 가 출력되면서 프로젝트 다운로드가 수행됩니다.
* `Nforge/open_project/프로젝트 이름` 에 프로젝트들이 다운로드 되며, 폴더는 아래와 같은 구조로 구성되어 있습니다.

    ```
    Nforge
    └── open_project
        └── 프로젝트 이름
            ├── code_info.json # 소스 코드 저장소 정보가 담긴 파일
            ├── developers.txt # 개발자들의 네이버 아이디
            ├── downloads # 다운로드 저장 폴더
            │   ├── json
            │   ├── raw # 첨부파일
            │   └── xml
            ├── issues # 이슈/게시판 저장 폴더
            │   ├── json
            │   ├── raw # 첨부파일
            │   └── xml
            │       ├── forum # 게시판 XML
            │       └── issue # 이슈 XML
            └── milestones # 마일스톤 XML
    ```

### GitHub로 마이그레이션 (공개 프로젝트만)
* ghm 명령어를 실행하면 아래와 같이 옵션을 입력하는 프롬프트가 나오게 됩니다.

    ```sh
    Repo name: nforge
    Private[y/N]: n
    Please input number of project that you want to migrate to GitHub
    Please input number 0: nforge : 1
    405a49d88436e2873dcd2aaab5495fa84fd8c699 is valid token
    Did you made a wiki?(y/n): y
    ```

* `Nforge/open_project` 에 있는 프로젝트들 중 하나를 골라 마이그레이션을 수행하게 됩니다. 출력되는 번호들 중 하나를 입력해주세요. 없는 번호를 고르시면 프로그램이 종료됩니다.
* 프로젝트를 고른 후 위에서 만든 토큰 파일을 검증합니다.
* 다음 위키를 만드셨다면 `y` 아니라면 `n`을 입력해주세요. 위키를 만들지 않으셨다면 자동으로 웹브라우저가 실행됩니다. 빠르게 하단의 `Save Page`를 눌러주세요.

### 비공개 프로젝트 GitHub 마이그레이션
* 먼저 [GitHub 로 가셔서](https://help.github.com/articles/importing-a-repository-with-github-importer/) 소스 코드 저장소를 import 해주시길 바랍니다.
* `Old clone URL` 에는 `오픈 프로젝트->코드` 탭에서 확인할 수 있는 `git clone` URL 혹은 `svn`의 URL을 입력하세요.
* 저장소 이름과 비공개 여부를 체크하고 마이그레이션을 시작하게 되면 몇 초후 아이디와 비밀번호를 입력하는 폼이 보입니다. 이때 네이버 아이디와 비밀번호를 입력해주세요.
* 진행 상황이 보이는 페이지로 넘어가면 이제 위키의 첫 페이지를 만들어주세요.
* 소스 코드 저장소 마이그레이션이 끝나면 GitHub에 등록해놓은 메일로 완료 안내가 갑니다.
* 메일을 받고 나면 `ghm` 명령어를 실행시키시고 `Private` 옵션은 `y`로 입력하세요.
* 이후 프롬프트는 공개 프로젝트일 때의 안내처럼 입력하시면 됩니다.
