# NAVER Open Project migration
## 개요
 [네이버 오픈 프로젝트](http://dev.naver.com/projects)를 Github로 migration 하는 모듈입니다.

 아래의 기능들을 구현 목표로 합니다.
 1. 게시판 & 이슈의 게시물들을 GitHub의 이슈로 migration.
 2. 프로젝트의 코드,커밋 로그등을 GitHub로 migration
 3. 다운로드를 GitHub releases로 migration

## 설계
* Dependencies
  * Python 3.5.1+
  * requests 2.10.0
  * [오픈 프로젝트 API](http://dev.naver.com/projects/nforge/wiki/APIGuide)
  * [GitHub API](https://developer.github.com/v3/)
* issue_migrate.py

  이슈 및 게시판의 게시물과 댓글들을 migration 하는 기능을 구현.
  사내 staging API 서버(http://staging.dev.naver.com)에 게시판(forum.xml), 이슈(issue.xml)을 요청해서 받아 온
  후 이 XML 파일들을 파싱해서 각 게시물&이슈의 id로 다시 각 게시물의 XML을 받아
  온 후 파싱하여 GitHub API(https://api.github.com) 로 보내서 새로운 이슈를 만들게 된다.

  * 주요 이슈
    1. 이슈, 게시물, 댓글의 작성자를 표시할 수 없음

      GitHub로 요청을 보내는 사용자로 작성자가 고정됨. 그래서 이슈 제목에
      이슈 작성자(assign)와 담당자(assignee) 을 명시함.
      ```
      [작성자->담당자] 제목
      ```
      댓글의 작성자 역시 댓글 본문 위에 작성자를 표시.
      ```
      작성자
      댓글 본문
      ```

* Git & SVN 저장소 migration
  1. GitHub 저장소를 먼저 만들어야 (이름은 필수)
  (https://developer.github.com/v3/repos/#create)

    ```python
    import requests

    url = "https://api.github.com/user/repos"

    querystring = {"access_token":"엑세스 토큰"}

    payload = "{
      "name" : "만들 저장소 이름",
      "description" : "설명"
    }"

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    print(response.text)
    ```
  2. Import API 를 써서 저장소 migration
  (https://developer.github.com/v3/migration/source_imports/#start-an-import)

    ```python
    import requests

    url = "https://api.github.com/repos/maxtortime/D2Coding/import"

    payload = "
      {
      "vcs" : "vcs 종류(Git, svn, Mercurial)",
      "vcs_url" : " https://dev.naver.com/svn/:프로젝트이름"
      "vcs_username" : "anonsvn",
      "vcs_password" : "anonsvn"
      }
      "
    headers = {
        'accept': "application/vnd.github.barred-rock-preview",
        'authorization': "token 엑세스토큰",
        'cache-control': "no-cache",
        'postman-token': "31f9c9e4-c443-717b-0aa4-51462df3905f"
        }

    response = requests.request("PUT", url, data=payload, headers=headers)

    print(response.text)
    ```
    
