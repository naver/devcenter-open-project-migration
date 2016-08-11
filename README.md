# Open Project Migration
[네이버 오픈 프로젝트](http://dev.naver.com/projects)를 GitHub로 migration 하는 CLI(Comamnd Line Interface) 프로그램입니다. 아래와 같은 기능을 갖추고 있습니다.

1. 게시판, 이슈의 첨부파일들을 포함한 글과 댓글들을 GitHub 이슈로 마이그레이션.
2. 다운로드의 게시물과 파일들을 GitHub 릴리즈로 마이그레이션.
3. Git/SVN 소스코드 저장소 마이그레이션.

## Dependencies
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

## 공통 주의 사항
* GitHub 토큰은 **data/GITHUB_ACCESS_TOKEN**, Enterprise 토큰은 **data/ENTERPRISE_ACCESS_TOKEN** 에 저장됩니다. 저 두 파일에 유효한 토큰이 저장되어 있지 않으면 프로그램이 동작하지 않습니다. 물론 토큰을 만드는 과정을 프로그램이 수행하게 되지만, 미리 개인 엑세스 토큰을 발급 받으셔서 위 파일 이름으로 저장하시면 편합니다.
* DevCode 마이그레이션 시에는 **data/COOKIES** 라는 파일에 nssTok 쿠키를 입력하셔야 합니다. 이 파일이 존재하지 않는다면 프로그램에서 쿠키를 입력받습니다.
* 빠른 시간 내에 많이 GitHub Migration을 시도하게되면 [Abuse Rate Limits](https://developer.github.com/v3/#abuse-rate-limits)가 일어나서 GitHub API를 호출할 수 없게 됩니다. 새로운 토큰을 발급하시거나 몇분 후에 다시 시도해주세요.

## Install
* 본 프로젝트를 git clone 혹은 다운로드 해주세요.
* 압축을 풀고 터미널을 켜주세요.
* **중요!!** 현재 XML 파싱을 위해 [lxml](http://lxml.de/)을 사용하고 있습니다. 윈도우 사용자 분들은 *반드시 [이 링크](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)로 가셔서* 적절한 lxml whl 파일을 다운로드 해주시고 나서 pip로 설치해주시면 되겠습니다.
* 터미널에서 pip 를 이용해 프로그램을 설치해주세요.
  > $ pip install --editable .

* **ght --help** 명령어를 입력하셨을 때 아래 옵션들이 보이시면 잘 설치된 겁니다.

    ```sh
  Usage: ght [OPTIONS]

    Managing your GitHub and GitHub ENTERPRISE TOKEN.

  Options:
    --token TEXT  토큰 입력
    --enterprise  GitHub Enterprise mode
    --help        Show this message and exit.
    ```

## ght 명령어
GitHub & GitHub Enterprise 의 토큰을 관리해주는 명령어입니다. data/GITHUB_ACCESS_TOKEN, ENTERPRISE_ACCESS_TOKEN에 담긴 토큰이 유효한지 검증해주고 새로운 토큰 파일을 만들어주는 역할을 담당합니다.

```sh
$ ght --token # 새 토큰 파일을 만듭니다.
$ ght --enterprise # 엔터프라이즈 토큰의 유효함을 검증합니다.
$ ght # GithUb 토큰의 유효함을 검증합니다.
```

### GitHub Personal access token 발급받기
1. github.com 혹은 엔터프라이즈에 로그인합니다.
2. 프로필 사진 클릭->Settings 클릭->Personal access tokens 탭 클릭
3. Generate new token 클릭
4. 비밀번호 입력
5. token description은 자유롭게 적고 repo에 체크 후 Genearte token 클릭
6. 토큰을 복사해서 data 폴더에 위의 파일명으로 텍스트 파일을 만든다
```
d9aab86a4ef63b15f48af6dd38590a3195de099f
```
**이 예제 토큰을 사용하지 마세요. 이미 삭제된 토큰입니다. 반드시 새 토큰을 발급 받으세요!**

## npa 명령어
Nforge 프로젝트를 parsing해서 json으로 만들어주는 명령어입니다.

```sh
$ npa
Project name: Nforge # 프로젝트 이름 입력
Dev code [y/N]: n # Devcode의 프로젝트인지 유무
Repo name: nforge-example # 마이그레이션될 GitHub 저장소 입력
# 자동으로 파싱이 진행됨
Now making 4372.xml of CodeReview:   8%|███▎    | 12/144 [00:04<00:45,  2.93it/s]
```

## ghm 명령어
파싱된 json 파일들을 GitHub로 마이그레이션 하는 명령어입니다.
``` sh
$ ghm
Open project [y/N]: n # 마이그레이션 할 프로젝트가 오픈 프로젝트인지 유무
아래 목록에서 Migration 할 프로젝트의 번호를 입력하세요
번호를 입력하세요 0: jindo : 0 # 지금까지 파싱한 프로젝트를 보여줌, 번호를 입력할 것
위키를 만드셨나요(y/n): n
# 저장소의 위키를 생성했는지 유무, 
# 위키를 생성하지 않았다면 자동으로 웹브라우저가 실행되며 이때 Create page 버튼을 누르면 된다.
```
