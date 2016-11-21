# 네이버 오픈 프로젝트 **이슈/게시판** 백업/마이그레이션 모듈
> 본 모듈은 소스코드 백업 기능은 제공하지 않으며, 소스 코드만 로컬PC로 다운 받으실 분은 아래 [소스 코드 로컬 백업 방법](#소스 코드 로컬 백업 방법) 가이드를 따르시길 바랍니다.

[![Build Status](https://travis-ci.org/naver/devcenter-open-project-migration.svg?branch=master)](https://travis-ci.org/naver/devcenter-open-project-migration)
[![PyPI](https://img.shields.io/pypi/dm/nforge-migration.svg)](https://pypi.python.org/pypi/nforge-migration)
[![PyPI](https://img.shields.io/pypi/v/nforge-migration.svg)](https://pypi.python.org/pypi/nforge-migration)
[![PyPI](https://img.shields.io/pypi/l/nforge-migration.svg)](https://pypi.python.org/pypi/nforge-migration)
[![PyPI](https://img.shields.io/pypi/pyversions/nforge-migration.svg)](https://pypi.python.org/pypi/nforge-migration)

네이버 오픈 프로젝트 이슈/게시판 백업 및 마이그레이션을 위한 Python 모듈입니다. 본 모듈은 [네이버 개발자센터의 오픈 프로젝트](http://dev.naver.com/projects) 의 마이그레이션을 위해 2가지 기능을 제공합니다.

1. 네이버 오픈프로젝트 이슈/게시판 백업: 로컬PC에 개인의 오픈 프로젝트 데이터 (이슈/게시판/첨부 파일 포함)를 백업
2. Github로 마이그레이션: 로컬PC에 백업한 데이터를 GitHub의 프로젝트로 마이그레이션


## 소스 코드만 백업
소스코드만 저장하실 분은 본 모듈 설치할 필요 없이 아래의 스텝을 따라해주시길 바랍니다.

### 소스 코드 로컬 백업 방법
- 저장소가 git을 사용할 경우에는 http://dev.naver.com/projects/프로젝트이름/src 에 들어가면 보이는 `git clone` 명령어를 터미널에 입력하시면 됩니다.
- 저장소가 svn을 사용할 경우에는 현재 svn이 설치되어 있을 경우 http://dev.naver.com/projects/프로젝트이름/src 에서 설명하는 것처럼 `svn checkout` 해주시면 되고 svn이 설치되어 있지 않을 경우 `git svn clone` 명령어를 사용해주세요.

  ```sh
  $ git svn clone --username 네이버아이디 https://dev.naver.com/svn/프로젝트이름
  # 이후 프롬프트에서 비밀번호는 http://dev.naver.com/account/ 에 설정한 `코드저장소 비밀번호`를 입력하면 됩니다.
  ```

### 소스 코드 import (코드 저장소가 있으면서, 코드들을 GitHub로 옮기려는 경우만 본 Step을 실행해 주세요.)
- 코드 저장소를 마이그레이션하는 과정입니다.
1. GitHub 저장소 import
   - 다음 링크로 이동 https://github.com/new/import/    
2. GitHub 저장소 import 폼값 입력    
   - `Your old repository’s clone URL` 에는 `오픈 프로젝트->코드` 탭에서 확인할 수 있는 `git clone` URL 혹은 `svn`의 URL을 입력하세요.
   - `Your new repository details` 아래에 `Name`에 생성될 저장소 이름을 입력하세요.
3. Import를 시작하게 되면 몇 초후 GitHub 화면에 아이디와 비밀번호를 입력하는 폼이 보입니다.
    - 오픈 프로젝트가 공개 설정일 경우: 아이디/비밀번호 모두 `anonsvn` 입력
    - 오픈 프로젝트가 비공개 설정일 경우: 네이버 아이디와 비밀번호
4. 코드 저장소 마이그레이션이 끝나면 아래와 같은 메시지가 출력되고, GitHub에 등록하신 메일로 완료 안내가 갑니다.
    -  `Importing complete! Your new repository your-id/your-project-name is ready.`

## 설치/실행 환경
본 모듈은 CLI(Comamnd Line Interface) 형태의 모듈로서 Windows, Mac, Linux OS를 모두 지원합니다.

1. Python 2.7 이상 ( 커맨드 라인에서 Python 버전확인 방법: `$ python --version`)
2. Git 1.7.10 이상  ( 커맨드 라인에서 Git 버전확인 방법: `$ git --version`)
	- 이슈/게시판 첨부파일 업로드에 사용됩니다.
	- 1.7.10 미만일 경우 GitHub에 push가 불가능해서 첨부파일 업로드가 불가능합니다.
3. pip (pip 설치 유무 확인 방법: `$ pip --version`)

위 3가지 프로그램이 없을 경우는 아래의 가이드를 따라 설치해주시길 바랍니다.

### Python 설치
  * [Windows에서 Python 설치법](https://wikidocs.net/8)
  	- 3.5 이상 버전을 권장합니다.
  	- 위 링크대로 설치해주시면 됩니다. (pip 포함 설치 및 `Add Python 3.5 to PATH` 옵션 필수 체크)
  * Mac, Linux: 기본적으로 Python이 제공됩니다. 다만 `python --version` 혹시 2.7 버전 이상이 아니시면 업그레이드 하셔야 합니다.

### Git 설치
- [Git 공식 홈페이지의 설치 자료](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%84%A4%EC%B9%98)를 참고하셔서 설치를 진행하시면 됩니다.
- 설치 완료 후 반드시 [최초 설정](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%B5%9C%EC%B4%88-%EC%84%A4%EC%A0%95)을 해주셔야 첨부파일 업로드가 가능합니다.
- 간혹 CentOS 6를 이용하시는 분은 기본 yum 저장소에 있는 Git 버전이 낮아 GitHub에 Push가 안 되는 오류가 일어날 수 있습니다. [이 자료](http://maxtortime.github.io/the-post-6832/)를 참고하셔서 Git 버전을 업그레이드 해주세요.

### pip 설치
#### Windows
- 위의 설치법을 따라하셨다면 pip가 자동으로 설치되있을 것입니다. 그러나 `pip --version` 을 실행하셨을 때 오류가 발생하신다면 아래 과정을 따라해주세요.
  1. https://bootstrap.pypa.io/get-pip.py 파일을 다운로드하세요.
  2. `cmd`를 켜고 `get-pip.py` 를 다운로드한 곳에서 `$ python get-pip.py` 를 실행하세요.
  3. pip 설치 버전 확인: `$ pip --version`

- 간혹 위 과정을 따라하셨는데도 `pip`를 실행할 수 없는 경우는 시스템 속성의 환경변수 편집하는 곳에서 시스템 변수의 `PATH`에 파이썬 설치 경로를 추가해주세요.

#### Linux/Mac OS
  1. pip 설치 스크립트 다운로드: `$ curl https://bootstrap.pypa.io/get-pip.py > get-pip.py`
  2. pip 설치: `$ sudo python get-pip.py`
  3. pip 설치 버전 확인: `$ pip --version`

## 모듈 설치 방법
- Python 및 pip 설치가 확인되셨다면 사용중인 운영체제에 따라 아래 안내를 따라해 주세요.
- 먼저 작업을 수행할 폴더를 만들어주시고 해당 폴더에서 작업을 수행해주세요. (예: `mkdir backup`)

### virtualenv를 이용한 설치 (권장)
- `virtualenv` 설치 : `$ sudo pip install virtualenv`
- `virtualenv`를 통한 가상환경 폴더 생성 : `$ virtualenv venv`
- 가상환경 활성화
	- Windows :  `$ venv\Scripts\activate`
	- Linux, Mac OS: `$ . venv/bin/activate`
	- 가상환경이 활성화(activate)되고 나면 프롬프트 왼쪽에 `(venv)`가 생기게 됩니다.
		- 예: `(venv) $ ...` (Linux, Mac OS), `(venv) C:\Users\maxto>` (WIndows)
- 가상환경이 활성화 된 후 운영체제에 따라 아래 안내를 따라주세요.

### Windows 사용자
1. Lxml (XML 파서) 설치파일 다운로드
   - http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml 이 곳에서 운영체제와 파이썬 버전에 맞는 파일을  위에서 생성하신 작업 폴더에 다운로드해주세요.
   - 32bit 이신 경우 아래 링크에서 다운로드하시면 됩니다.
     - [Python 2.7](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp27-cp27m-win32.whl)
     - [Python 3.4](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp34-cp34m-win32.whl)
     - [Python 3.5](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/lxml-3.6.4-cp35-cp35m-win32.whl)

2. Lxml (XML 파서) 설치
	- 가상환경이 활성화된 상태에서 `pip install 다운로드된파일명` 실행.

3. 마이그레이션 모듈 설치
	- 가상환경이 활성화된 상태에서 `pip install nforge-migration` 실행.

### Linux, Mac OS
- 가상환경이 활성화 된 상태에서 `pip install nforge-migration` 실행


### 설치 완료 확인
- `npa --help` 명령어를 입력하셨을 때 터미널에 아래와 같은 화면이 보이면 설치가 완료된 것 입니다.

  ```sh
  Usage: npa [OPTIONS]

  Command line interface for parsing Nforge project.

  Options:
    --name TEXT  오픈 프로젝트 이름
    --private            오픈 프로젝트 비공개 저장소 여부
    --dev_code           DevCode 프로젝트인지
    --help               Show this message and exit.
  ```

## 모듈 사용 방법    
본 모듈은 아래 2가지 기능을 제공합니다.

1. 네이버 오픈프로젝트 백업: 로컬PC에 개인의 오픈 프로젝트 데이터 (이슈/게시판/첨부 파일 포함)를 백업
2. Github로 마이그레이션: 로컬PC에 백업한 데이터를 GitHub의 프로젝트로 마이그레이션

> 주의 !! 비공개 프로젝트의 경우는 아래 안내를 필독하세요.

### 비공개 프로젝트 준비 작업
- 네이버 오픈프로젝트가 `비공개` 상태이면 `공개`로 전환 후 진행하시거나, 프로젝트 관련 인증키값 데이터를 추출해 저장하신 다음 진행해야 합니다.
- 비공개 프로젝트 관련 인증 키값 추출 방법
  1. [오픈 프로젝트](http://dev.naver.com/projects)에 로그인 해주세요.
  2.  웹브라우저 주소창에 직접 `javascript:document.cookie` 라고 입력하세요. ( Ctrl C / V 하시면 안됩니다.)
  3. 웹브라우저에 보이는 값들 중 `NID_SES`와 `NID_AUT` 값을 복사해주세요.
  4. 작업 폴더에 `cookies.txt` 라는 파일을 만들어주세요.
  5. 아래와 같은 형식으로 `cookies.txt` 파일을 채워주시고 저장하세요. (쿠키 값의 맨마지막 세미콜론은 지울 것)
    ```
    NID_SES=키값
    NID_AUT=키값
    ```

## 네이버 오픈프로젝트 백업
* 터미널에서 설치 과정에서 만든 작업 폴더로 이동하셔서 아래 안내를 따라주세요.
* `npa` 명령어를 아래의 안내와 같이 터미널에 입력해주세요.
    * 공개 프로젝트: `$ npa --name 프로젝트이름`
    * 비공개 프로젝트: `$ npa --name 프로젝트이름 --private`

> **중요!!** `프로젝트이름`은 만약 프로젝트의 URL이 `http://dev.naver.com/projects/d2coding/` 이라면 `d2coding`이라고 입력해주시면 됩니다.

* 자동으로 프로젝트들이 다운로드되고 아무 메시지 없이 끝났다면 성공한 것입니다.

*  `npa` 명령어 동작 화면
  ```
  Now making 7267.xml and 7267.json of download: 100%|███| 2/2 [00:01<00:00,  1.04s/it]
  Now making 98439.xml and 98439.json of issue: 100%|███| 21/21 [00:09<00:00,  2.78it/s]
  Now making 98483.xml and 98483.json of forum: 100%|███| 11/11 [00:02<00:00,  3.17it/s]
  ```
* `작업 폴더/Nforge/open_project/프로젝트 이름` 에 프로젝트들이 다운로드 됩니다. 폴더는 아래와 같은 구조로 구성되어 있습니다. (예: `backup/Nforge/open_project/d2coding`)

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

## GitHub 마이그레이션
작업 폴더에서 아래 안내를 차례대로 따라해주세요. GitHub 회원가입을 먼저 해주셔야 합니다.

> 주의!! 코드 저장소가 없거나 아무 커밋도 하지 않은 프로젝트는 import를 수행하지 마시고 아래 안내를 참고하세요.

### 코드 저장소가 없는 프로젝트의 경우
- https://github.com/new 로 이동합니다.
- `Repository name` 에 저장소 이름을 입력하고 `Initialize this repository with a README` 체크박스에 체크합니다.
- `Create Repository`를 만들어서 저장소를 생성합니다.
- 아래 안내를 참고하셔서 저장소 Wiki 및 엑세스 토큰을 생성해주세요.

### 저장소 Wiki 생성 (반드시 생성해주세요!!)
위키를 생성하는 이유는 이슈,게시판,댓글의 첨부파일을 업로드하기 위한 것입니다.
1. https://github.com/사용자아이디/프로젝트명/wiki 로 접속해서 `Create the first page` 버튼 클릭
2. 페이지 우측 하단에 `Save Page` 버튼 클릭


### Personal Access Token 생성
1. https://github.com/settings/tokens 으로 이동
2. 우측 메뉴 상단에 `Generate new token` 버튼 클릭 후 비번 입력
3. 아래 항목들을 입력
    - `Token Description` (토큰 설명, 예: `openproject`)
    - 체크박스들 중에 `repo` 항목에 체크
4. 하단에 `Generate token` 버튼 클릭 후 나오는 코드값을 복사
5. 작업 폴더에 `token.txt` 라는 파일을 만들고 복사한 토큰을 넣어준 후 저장한다.
    - `echo 복사한토큰값 > token.txt`

#### 마이그레이션 명령어 수행
- 본인의 계정에 바로 마이그레이션 하는 경우
  - `ghm --name GitHub저장소이름 --project_name 오픈프로젝트이름`
- 특정 Organization의 저장소에 마이그레이션 하는 경우
  - `ghm -name GitHub저장소이름 --project_name 오픈프로젝트 이름 --org_name Organization이름`
- `오픈프로젝트이름` 은 위에서 다운로드한 오픈 프로젝트 이름과 일치해야 합니다.
- `GitHub저장소이름` 은 위에서 만드신 저장소 이름과 일치해야 합니다.

> 주의 !! 빠른 시간 내에 많은 마이그레이션을 수행하면 [Abuse Rate Limits](https://developer.github.com/v3/#abuse-rate-limits)가 발생해 일시적으로 GitHub API를 호출할 수 없게 됩니다. 몇 분 후에 다시 시도해주세요.

> 프로젝트의 이슈가 너무 많아서 마이그레이션 진행 중 위에서 말한 제한이 걸려 프로그램이 종료될 경우 GitHub 이슈로 알려주세요.

> 중요 !! Github에 위키를 만들지 않았다면 첨부파일 업로드 과정이 실패합니다. 위키 생성을 반드시 해주세요.

> 중요 !! Git 설치 후 최초 설정을 했는지 확인해주세요. 하지 않았다면 첨부파일이 업로드 되지 않습니다. 아래 명령어를 입력해주세요. [상세 설명](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%B5%9C%EC%B4%88-%EC%84%A4%EC%A0%95)
  - 자신의 이름 입력 `$ git config --global user.name "John Doe"`
  - 자신의 이메일 입력 `$ git config --global user.email johndoe@example.com`

- 아래의 명령어를 입력해서 이슈 및 게시판 마이그레이션을 시작합니다.
   - `$ ghm --name GitHub저장소이름 --project_name 프로젝트이름`
   - `프로젝트이름` 은 위에서 다운로드한 프로젝트 이름과 일치해야 합니다.
   - `GitHub저장소이름` 은 위에서 만드신 GitHub repository 이름과 일치해야 합니다.

-  `ghm` 명령어 동작 화면
  ```
   a8b9g3q9c... is valid token # 토큰 검증
   53%|█| 17/32 [00:17<00:16,  1.11s/it] # 이슈 업로드
   ... # Git 메시지 (이슈 첨부파일 업로드 과정)
   100%|███| 2/2 [00:08<00:00,  5.34s # 다운로드 마이그레이션
  ```
- 위 과정을 거친 후 아무 에러메시지 없이 끝났다면 성공한 것입니다.

## 마이그레이션 결과 확인 방법

### 게시판/이슈 마이그레이션 확인
* 모두 [GitHub Issue](https://guides.github.com/features/issues/)로 옮겨집니다.
  - 오픈 프로젝트 게시판 -> `forum` 라벨
  - 오픈 프로젝트 이슈 -> `issue` 라벨
  - 오픈 프로젝트 `foo` 게시판/이슈 목록 -> `foo` 라벨

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
* 이슈/게시판/댓글의 첨부파일은 각 이슈 본문에서 확인할 수 있습니다.

### 코드
* 프로젝트의 git/SVN 저장소가 GitHub로 옮겨집니다.
* GitHub는 SVN 방식의 디렉토리 구조를 따르지 않으므로 GitHub에서 저장소 구조가 조금 달라보일 수 있습니다.
* [GitHub에서 SVN 클라이언트 이용하기](https://help.github.com/articles/support-for-subversion-clients/)

### 다운로드
* [GitHub의 Releases](https://help.github.com/articles/about-releases/)로 옮겨집니다.
* 버전 라벨이 원래 프로젝트와 조금 다를 수 있지만 순서는 일치합니다.
* 다운로드의 첨부파일도 릴리즈에서 다운로드 가능합니다.

### 위키
* [GitHub의 Wiki](https://help.github.com/articles/about-github-wikis/)로 옮겨집니다.
* 원본 문서 형식 그대로 저장하기 때문에 렌더링이 제대로 되지 않았을 수 있습니다.
