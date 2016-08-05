# Open Project Migration
## 개요
[네이버 오픈 프로젝트](http://dev.naver.com/projects)를 GitHub로 migration 하는 CLI(Comamnd Line Interface) 프로그램입니다. 아래와 같은 기능을 갖추고 있습니다.

## 기능
1. 게시판, 이슈의 첨부파일들을 포함한 글과 댓글들을 GitHub 이슈로 마이그레이션.
2. 다운로드의 게시물과 파일들을 GitHub 릴리즈로 마이그레이션.
3. Git/SVN 소스코드 저장소 마이그레이션.

## 사전 준비 및 설치
### 준비물
* Python 2.7 이상
  * [Windows에서 Python 설치법](https://wikidocs.net/8)
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

### 설치법
* 본 프로젝트를 git clone 혹은 다운로드 해주세요.
* 압축을 풀고 터미널을 켜주세요.
* **중요!!** 현재 XML 파싱을 위해 [lxml](http://lxml.de/)을 사용하고 있습니다. 윈도우 사용자 분들은 *반드시 [이 링크](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)로 가셔서* 적절한 lxml whl 파일을 다운로드 해주시고 나서 pip로 설치해주시면 되겠습니다.
* 터미널에서 pip 를 이용해 프로그램을 설치해주세요.
  > $ pip install --editable .

* **cli --help** 명령어를 입력하셨을 때 아래 옵션들이 보이시면 잘 설치된 겁니다.

    ```sh
    $ cli --help
    Usage: cli [OPTIONS]
    
    Options:
    --github_repo TEXT     GitHub 레포지토리 이름
    --project_name TEXT    NFORGE 프로젝트 이름
    --api_url TEXT         NFORGE API URL
    --cookies              쿠키 이용 여부
    --enterprise_url TEXT  GitHub 엔터프라이즈 URL
    --issue_only           이슈만 마이그레이션 여부
    --help                 Show this message and exit.
    ```
## 공통 주의 사항
* GitHub 토큰은 **GITHUB_ACCESS_TOKEN**, Enterprise 토큰은 **ENTERPRISE_ACCESS_TOKEN** 에 저장됩니다. 저 두 파일에 유효한 토큰이 저장되어 있지 않으면 프로그램이 동작하지 않습니다. 물론 토큰을 만드는 과정을 프로그램이 수행하게 되지만, 미리 개인 엑세스 토큰을 발급 받으셔서 위 파일 이름으로 저장하시면 편합니다.
* Enterprise migration 시에는 소스코드 저장소는 수동으로 작업하셔야 합니다.
* 프로그램 실행 시 위키의 첫 페이지를 만들기 위해 웹브라우저가 자동으로 실행됩니다. 당황하지 마시고 Save Page 버튼을 눌러주세요.
* Git 저장소를 가진 프로젝트는 네이버 아이디와 비밀번호가 있어야 소스코드 저장소 마이그레이션이 가능합니다. 프로그램에 지시에 따라 입력하시면 됩니다.
* 마이그레이션 도중에 프로그램을 종료하시면 불완전하게 마이그레이션이 끝나게 됩니다. 오래 걸리더라도 조금만 기다려주세요.


## DevCode -> OSS(GitHub Enterprise) migration
devcode.navercorp.com에 프로그램이 접근하기 위해서는 적절한 쿠키가 필요합니다.
로그인 하신 후 nssTok 쿠키를 프로젝트 루트 폴더에 COOKIES 라는 파일로 저장해주세요.
(파일에 '\n' 이 없어야 합니다)
(쿠키 얻는 법은 차후 추가 예정)

다음 아래 형식의 명령어를 실행해주세요.
  > $ cli --cookies --enterprise_url https://oss.navercorp.com --issue_only

실행 하신 후에 프로그램에 지시에 따라서 나머지 옵션도 입력해주시면 마이그레이션이 진행됩니다.
Devcode의 경우 소스코드 저장소 migration 이 불가능합니다.

## 오픈 프로젝트 -> GitHub 마이그레이션
* cli 명령어를 입력하시고 프로그램에 지시에 따라 적절한 옵션을 입력해주세요.
